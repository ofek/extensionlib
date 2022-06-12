# Configuration

-----

Users are expected to configure their extension modules in TOML as an [array of tables](https://toml.io/en/v1.0.0#array-of-tables) with the final sub-table name referring to a [plugin](builders.md#plugin-registration). For example:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [[project.extensions.spam]]
    ...
    [[project.extensions.example]]
    ...
    [[project.extensions.example]]
    ...
    [[project.extensions.foo]]
    ...
    ```
