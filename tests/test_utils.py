import os

from extension.constants import ENV_OPTION_PREFIX
from extension.utils import get_env_option, normalize_relative_path


def test_normalize_relative_path():
    assert normalize_relative_path('/a/b/') == f'a{os.path.sep}b'


def test_get_env_option():
    builder_name = 'foo'
    option = os.urandom(4).hex()
    value = '9000'
    env_var = f'{ENV_OPTION_PREFIX}{builder_name}_{option}'.upper()

    assert get_env_option(builder_name, option) == ''

    os.environ[env_var] = value
    try:
        assert get_env_option(builder_name, option) == value
    finally:
        del os.environ[env_var]

    assert get_env_option(builder_name, option) == ''
