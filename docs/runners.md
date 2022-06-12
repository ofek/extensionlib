# Runners

-----

Managing the building of extension modules is done using an instance of [`BuildRunner`][extension.runner.BuildRunner].

```python
from extension.runner import BuildRunner

...
runner = BuildRunner('.', user_config['project'])
...
```

## Usage

### Generation

[Inputs][extension.interface.ExtensionModules.generate_inputs]:

```python
build_data = {}
runner.generate_inputs(build_data)
```

[Outputs][extension.interface.ExtensionModules.generate_outputs]:

```python
build_data = {}
runner.generate_outputs(build_data)
```

### Artifact inspection

[Inputs][extension.interface.ExtensionModules.inputs]:

```python
inputs = runner.inputs()
```

[Outputs][extension.interface.ExtensionModules.outputs]:

```python
outputs = runner.outputs()
```

## Options

Some options affect the behavior of builds and are stripped out from the [final configuration][extension.interface.ExtensionModules.config].

### Enabling

Users may set `enable-by-default` to `false` for any entry which will prevent it from being built. To enable it again users must set the upper-cased environment variable `PY_EXTENSION_BUILDER_<builder_name>_ENABLE` to `true` or `1`.

To illustrate, users can enable the following:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [[project.extensions.spam]]
    enable-by-default = false
    ...
    ```

with the environment variable `PY_EXTENSION_BUILDER_SPAM_ENABLE`.
