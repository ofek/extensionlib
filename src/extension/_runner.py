from __future__ import annotations

import sys
from copy import deepcopy
from typing import TYPE_CHECKING, Generator, Optional, Type

from .constants import ENTRY_POINT_GROUP
from .utils import get_env_option, normalize_relative_path

if TYPE_CHECKING:
    from .interface import ExtensionModules

if sys.version_info >= (3, 8):
    from importlib.metadata import Distribution, EntryPoint
else:
    from importlib_metadata import Distribution, EntryPoint


class BuilderCache:
    def __init__(self):
        self.__resolver = Distribution.discover()
        self.__builders: dict[str, Type[ExtensionModules]] = {}
        self.__seen: dict[str, EntryPoint] = {}
        self.__search_exhausted = False

    def get(self, name: str) -> Optional[Type[ExtensionModules]]:
        if name in self.__builders:
            return self.__builders[name]
        elif name in self.__seen:
            builder = self.__seen.pop(name).load()
            self.__builders[name] = builder
            return builder
        elif self.__search_exhausted:
            return None

        for distribution in self.__resolver:
            builder = None
            for entry_point in distribution.entry_points:
                if entry_point.group != ENTRY_POINT_GROUP:
                    continue
                elif entry_point.name == name:
                    builder = entry_point.load()
                else:
                    self.__seen.setdefault(entry_point.name, entry_point)

            if builder is not None:
                self.__builders[name] = builder
                return builder

        self.__search_exhausted = True

    def __getitem__(self, item: str) -> Type[ExtensionModules]:
        self.get(item)
        return self.__builders[item]

    def __contains__(self, item: str) -> bool:
        return self.get(item) is not None


class Config:
    def __init__(self, builder_name: str, config: dict) -> None:
        config = deepcopy(config)

        # Extract runner configuration
        self.enable_by_default = config.pop('enable-by-default', True)

        self.builder_name = builder_name
        self.builder_config = config

    def enabled(self) -> bool:
        return self.enable_by_default or (get_env_option(self.builder_name, 'enable') in ('true', '1'))


class BuildRunner:
    def __init__(self, root: str, metadata: dict) -> None:
        """
        Args:
            root: The project's root directory.
            metadata: The [PEP 621][] project metadata.
        """
        self.__root = root
        self.__metadata = metadata
        self.__builders = BuilderCache()

    @property
    def root(self) -> str:
        return self.__root

    @property
    def metadata(self) -> dict:
        return self.__metadata

    @property
    def builders(self) -> BuilderCache:
        return self.__builders

    def inputs(self) -> list[str]:
        """
        Returns:
            The complete list of builder [`inputs`][extension.interface.ExtensionModules.inputs].
        """
        return [normalize_relative_path(path) for builder in self.get_builders() for path in builder.inputs()]

    def outputs(self) -> list[str]:
        """
        Returns:
            The complete list of builder [`outputs`][extension.interface.ExtensionModules.outputs].
        """
        return [normalize_relative_path(path) for builder in self.get_builders() for path in builder.outputs()]

    def generate_inputs(self, data: dict) -> None:
        """
        Args:
            data: Options specific to source distributions.
        """
        for builder in self.get_builders():
            builder.generate_inputs(data)

    def generate_outputs(self, data: dict) -> None:
        """
        Args:
            data: Options specific to built distributions.
        """
        for builder in self.get_builders():
            builder.generate_outputs(data)

    def get_builders(self) -> Generator[ExtensionModules, None, None]:
        extension_modules_config = self.metadata.get(ENTRY_POINT_GROUP, {})
        for builder_name in extension_modules_config:
            if builder_name not in self.builders:
                raise ValueError(f'Unknown extension module builder: {builder_name}')

        for builder_name, config_entries in extension_modules_config.items():
            for config_entry in config_entries:
                config = Config(builder_name, config_entry)
                if not config.enabled():
                    continue

                yield self.builders[builder_name](builder_name, self.root, self.metadata, config.builder_config)
