# Runners

-----

Managing the building of extension modules is done using an instance of [`BuildRunner`][extension.runner.BuildRunner].

```python
from extension.runner import BuildRunner

runner = BuildRunner('.')
...
```

## Usage

Users are expected to configure their extension modules in TOML as an [array of tables](https://toml.io/en/v1.0.0#array-of-tables) with the final sub-table name referring to a [plugin](builders.md#plugin-registration). For example:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [[tool.extensionlib.spam]]
    ...
    [[tool.extensionlib.example]]
    ...
    [[tool.extensionlib.example]]
    ...
    [[tool.extensionlib.foo]]
    ...
    ```

Runners must build each entry:

```python
build_data = {}
extensions = user_config['tool']['extensions']

for builder_name, config_entries in extensions.items():
    runner.build(builder_name, configs, build_data)
```

## Options

Some options affect the behavior of builds and are stripped out from the [final configuration][extension.interface.ExtensionModules.config].

### Enabling

Users may set `enable-by-default` to `false` for any entry which will prevent it from being built. To enable it again users must set the upper-cased environment variable `PY_EXTENSION_BUILDER_<builder_name>_ENABLE` to `true` or `1`.

To illustrate, users can enable the following:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [[tool.extensionlib.spam]]
    enable-by-default = false
    ...
    ```

with the environment variable `PY_EXTENSION_BUILDER_SPAM_ENABLE`.

### Forced builds

Builders can [indicate][extension.interface.ExtensionModules.needs_build] that config entries should be skipped, maybe because no files have changed. Users can override this behavior with the `force-rebuild` option:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [[tool.extensionlib.spam]]
    force-rebuild = true
    ...
    ```
