from __future__ import annotations

import sys
from copy import deepcopy
from typing import TYPE_CHECKING, Optional, Type

from .constants import ENTRY_POINT_GROUP
from .utils import get_env_option

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
                elif entry_point.name != name:
                    self.__seen.setdefault(name, entry_point)
                elif builder is None:
                    builder = entry_point.load()

            if builder is not None:
                self.__builders[name] = builder
                return builder

        self.__search_exhausted = True


class Config:
    def __init__(self, builder_name: str, config: dict) -> None:
        config = deepcopy(config)

        # Extract runner configuration
        self.enable_by_default = config.pop('enable-by-default', True)
        self.force_rebuild = config.pop('force-rebuild', False)

        self.builder_name = builder_name
        self.builder_config = config

    def enabled(self) -> bool:
        return self.enable_by_default or (get_env_option(self.builder_name, 'enable') in ('true', '1'))


class BuildRunner:
    def __init__(self, root: str) -> None:
        """
        Args:
            root: The project's root directory.
        """
        self.__root = root
        self.__builders = BuilderCache()

    @property
    def root(self) -> str:
        return self.__root

    @property
    def builders(self) -> BuilderCache:
        return self.__builders

    def build(self, builder_name: str, config_entries: list[dict], data: dict) -> None:
        """
        Args:
            builder_name: The name of the registered [extension module builder][extension.interface.ExtensionModules]
                          with which to use.
            config_entries: A list of user defined configuration each intended for a distinct instance of
                            the chosen builder.
            data: A mapping that will persist for the life of all extension module builders that may be mutated by
                  each one. The primary use case is to set builder-specific data e.g. a wheel builder may recognize
                  tag-related options.
        """
        builder_class = self.builders.get(builder_name)
        if builder_class is None:
            raise ValueError(f'Unknown extension module builder: {builder_name}')

        for config_entry in config_entries:
            config = Config(builder_name, config_entry)
            if not config.enabled():
                continue

            builder = builder_class(builder_name, self.root, config.builder_config)
            if config.force_rebuild or builder.needs_build():
                builder.build(data)
