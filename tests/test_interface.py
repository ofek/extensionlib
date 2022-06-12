import os

from extension.constants import ENV_OPTION_PREFIX
from extension.interface import ExtensionModules


class MockExtensionModules(ExtensionModules):
    def inputs(self):
        return []

    def outputs(self):
        return []

    def generate_inputs(self, data):
        pass

    def generate_outputs(self, data):
        pass


def test_properties(tmp_path):
    name = 'foo'
    root = str(tmp_path)
    metadata = {}
    config = {}

    builder = MockExtensionModules(name, root, metadata, config)

    assert builder.name is name
    assert builder.root is root
    assert builder.metadata is metadata
    assert builder.config is config


def test_get_env_option(tmp_path):
    builder = MockExtensionModules('foo', str(tmp_path), {}, {})
    option = os.urandom(4).hex()
    value = '9000'
    env_var = f'{ENV_OPTION_PREFIX}{builder.name}_{option}'.upper()

    assert builder.get_env_option(option) == ''

    os.environ[env_var] = value
    try:
        assert builder.get_env_option(option) == value
    finally:
        del os.environ[env_var]

    assert builder.get_env_option(option) == ''


def test_required_methods(tmp_path):
    # This is just for code coverage
    builder = MockExtensionModules('foo', str(tmp_path), {}, {})

    builder.inputs()
    builder.outputs()
    builder.generate_inputs({})
    builder.generate_outputs({})
