from __future__ import annotations

from abc import ABC, abstractmethod

from .utils import get_env_option


class ExtensionModules(ABC):
    def __init__(self, name: str, root: str, config: dict) -> None:
        self.__name = name
        self.__root = root
        self.__config = config

    @property
    def name(self) -> str:
        """
        The name used to register this extension module builder.
        """
        return self.__name

    @property
    def root(self) -> str:
        """
        The project's root directory.
        """
        return self.__root

    @property
    def config(self) -> dict:
        """
        The raw user-defined configuration.
        """
        return self.__config

    @abstractmethod
    def files(self) -> list[str]:
        """
        Returns:
            The complete list of files that are targeted for [generation][extension.interface.ExtensionModules.build].
                Each path must be relative to the [project root][extension.interface.ExtensionModules.root].
        """

    @abstractmethod
    def build(self, data: dict) -> None:
        """
        This method builds the extension modules. Any generated file that is not returned by the
        [`files`][extension.interface.ExtensionModules.files] method is in violation of the spec and will be ignored.

        Args:
            data: A mapping that will persist for the life of all extension module builders that may be mutated by
                  each one. The primary use case is to set builder-specific data e.g. a wheel builder may recognize
                  tag-related options.
        """

    def needs_build(self) -> bool:
        """
        Returns:
            A boolean indicating whether or not a build is necessary. For example, if no source files have changed
                implementations may return `False`.
        """
        return True

    def get_env_option(self, option: str) -> str:
        """
        Returns:
            The value of the upper-cased environment variable `PY_EXTENSION_BUILDER_<builder_name>_<option>`.
        """
        return get_env_option(self.name, option)
