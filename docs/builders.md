# Builders

-----

Extension module builders are expected to implement the [`ExtensionModules`][extension.interface.ExtensionModules] interface.

```python
from extension.interface import ExtensionModules

class ExampleExtensionModules(ExtensionModules):
    ...
```

## Plugin registration

Every builder a project implements must be defined under the `extensions` [entry point](https://peps.python.org/pep-0621/#entry-points) group:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.entry-points.extensions]
    example = "pkg:ExampleExtensionModules"
    ```

Users select builders with the name of their plugin (in this case `example`).

## Inputs

Inputs are any intermediate artifacts that are required to generate the [outputs](#outputs), ideally even without network access.

The required methods are [`inputs`][extension.interface.ExtensionModules.inputs] and [`generate_inputs`][extension.interface.ExtensionModules.generate_inputs].

## Outputs

Outputs are the extension modules and anything else that is required in the built distribution.

The required methods are [`outputs`][extension.interface.ExtensionModules.outputs] and [`generate_outputs`][extension.interface.ExtensionModules.generate_outputs].

## Build data

Both generation methods accept a `data` parameter that is a mapping that will persist for the life of all extension module builders that may be mutated by each one. The primary use case is to set target-specific data e.g. a wheel target may recognize tag-related options.
