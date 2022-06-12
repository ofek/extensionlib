from __future__ import annotations

from abc import ABC, abstractmethod

from .utils import get_env_option


class ExtensionModules(ABC):
    def __init__(self, name: str, root: str, metadata: dict, config: dict) -> None:
        """
        Args:
            name: The name used to register this extension module builder.
            root: The project's root directory.
            metadata: The [PEP 621][] project metadata.
            config: The raw user-defined configuration.
        """
        self.__name = name
        self.__root = root
        self.__metadata = metadata
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
    def metadata(self) -> dict:
        """
        The [PEP 621][] project metadata.
        """
        return self.__metadata

    @property
    def config(self) -> dict:
        """
        The raw user-defined configuration.
        """
        return self.__config

    @abstractmethod
    def inputs(self) -> list[str]:
        """
        Returns:
            The complete list of files or directories that are targeted for generation by the
                [`generate_inputs`][extension.interface.ExtensionModules.generate_inputs] method.
                These are any intermediate artifacts that are required to generate the
                [`outputs`][extension.interface.ExtensionModules.outputs], ideally even without network access.


                Each path must be relative to the [project root][extension.interface.ExtensionModules.root].
        """

    @abstractmethod
    def outputs(self) -> list[str]:
        """
        Returns:
            The complete list of files or directories that are targeted for generation by the
                [`generate_outputs`][extension.interface.ExtensionModules.generate_outputs] method.
                These are the extension modules and anything else that is required in the built distribution.

                Each path must be relative to the [project root][extension.interface.ExtensionModules.root].
        """

    @abstractmethod
    def generate_inputs(self, data: dict) -> None:
        """
        This method generates the files or directories that are returned by the
        [`inputs`][extension.interface.ExtensionModules.inputs] method.

        Args:
            data: Options specific to source distributions.
        """

    @abstractmethod
    def generate_outputs(self, data: dict) -> None:
        """
        This method generates the files or directories that are returned by the
        [`outputs`][extension.interface.ExtensionModules.outputs] method.

        Args:
            data: Options specific to built distributions.
        """

    def get_env_option(self, option: str) -> str:
        """
        Returns:
            The value of the upper-cased environment variable `PY_EXTENSION_BUILDER_<builder_name>_<option>`.
        """
        return get_env_option(self.name, option)
