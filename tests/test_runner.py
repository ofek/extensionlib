import os

import pytest

from extension.constants import ENV_OPTION_PREFIX
from extension.runner import BuildRunner

from .utils import load_toml


def get_default_build_data():
    return {'mock-a': False, 'mock-b': False, 'mock-c': False}


def assert_all(runner, tmp_path):
    # Inputs
    expected_inputs = [f'mock-b{os.path.sep}foo.h', f'mock-a{os.path.sep}bar.h', f'mock-c{os.path.sep}baz.h']
    assert runner.inputs() == expected_inputs

    build_data = get_default_build_data()
    runner.generate_inputs(build_data)
    assert all(build_data.values())

    for expected_input in expected_inputs:
        assert (tmp_path / expected_input).is_file()

    # Outputs
    expected_outputs = [f'mock-b{os.path.sep}foo.so', f'mock-a{os.path.sep}bar.so', f'mock-c{os.path.sep}baz.so']
    assert runner.outputs() == expected_outputs

    build_data = get_default_build_data()
    runner.generate_outputs(build_data)
    assert all(build_data.values())

    for expected_output in expected_outputs:
        assert (tmp_path / expected_output).is_file()


def test_unknown_builder(tmp_path):
    config = load_toml(
        """
[[project.extensions.mock-z]]
modules = ["foo"]
"""
    )
    runner = BuildRunner(str(tmp_path), config['project'])

    # Twice for code coverage
    for _ in range(2):
        with pytest.raises(ValueError, match='Unknown extension module builder: mock-z'):
            next(runner.get_builders())


def test_default(tmp_path):
    config = load_toml(
        """
[[project.extensions.mock-b]]
modules = ["foo"]
[[project.extensions.mock-a]]
modules = ["bar"]
[[project.extensions.mock-c]]
modules = ["baz"]
"""
    )
    runner = BuildRunner(str(tmp_path), config['project'])
    assert_all(runner, tmp_path)


def test_disabled(tmp_path):
    config = load_toml(
        """
[[project.extensions.mock-b]]
modules = ["foo"]
[[project.extensions.mock-a]]
enable-by-default = false
modules = ["bar"]
[[project.extensions.mock-c]]
modules = ["baz"]
"""
    )
    runner = BuildRunner(str(tmp_path), config['project'])

    # Inputs
    expected_inputs = [f'mock-b{os.path.sep}foo.h', f'mock-c{os.path.sep}baz.h']
    assert runner.inputs() == expected_inputs

    build_data = get_default_build_data()
    runner.generate_inputs(build_data)
    assert not build_data['mock-a']
    assert build_data['mock-b']
    assert build_data['mock-c']

    for expected_input in expected_inputs:
        assert (tmp_path / expected_input).is_file()

    # Outputs
    expected_outputs = [f'mock-b{os.path.sep}foo.so', f'mock-c{os.path.sep}baz.so']
    assert runner.outputs() == expected_outputs

    build_data = get_default_build_data()
    runner.generate_outputs(build_data)
    assert not build_data['mock-a']
    assert build_data['mock-b']
    assert build_data['mock-c']

    for expected_output in expected_outputs:
        assert (tmp_path / expected_output).is_file()


def test_enable(tmp_path):
    config = load_toml(
        """
[[project.extensions.mock-b]]
modules = ["foo"]
[[project.extensions.mock-a]]
enable-by-default = false
modules = ["bar"]
[[project.extensions.mock-c]]
modules = ["baz"]
"""
    )
    runner = BuildRunner(str(tmp_path), config['project'])

    env_var = f'{ENV_OPTION_PREFIX}MOCK-A_ENABLE'
    os.environ[env_var] = 'true'
    try:
        assert_all(runner, tmp_path)
    finally:
        del os.environ[env_var]
