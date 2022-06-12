import os

from .constants import ENV_OPTION_PREFIX


def normalize_relative_path(path: str) -> str:
    """
    Returns:
        The normalized relative path with platform-specific separators.
    """
    return os.path.normpath(path).strip(os.path.sep)


def get_env_option(builder_name: str, option: str) -> str:
    """
    Returns:
        The value of the upper-cased environment variable `PY_EXTENSION_BUILDER_<builder_name>_<option>`.
    """
    return os.environ.get(f'{ENV_OPTION_PREFIX}{builder_name}_{option}'.upper(), '')
