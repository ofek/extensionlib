# Builders

-----

Extension module builders are expected to implement the [`ExtensionModules`][extension.interface.ExtensionModules] interface.

```python
from extension.interface import ExtensionModules

class ExampleExtensionModules(ExtensionModules):
    ...
```

## Plugin registration

Every builder your project implements must be defined under the `extension_modules` [entry point group](https://peps.python.org/pep-0621/#entry-points):

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.entry-points.extension_modules]
    example = "pkg:ExampleExtensionModules"
    ```

Users select builders with the name of their plugin (in this case `example`).

## Required methods

The required methods are [`files`][extension.interface.ExtensionModules.files] and [`build`][extension.interface.ExtensionModules.build].

The [`files`][extension.interface.ExtensionModules.files] method returns a list of relative file paths which build backends will (if present) include in wheels and other tools may use for cleaning purposes.

The [`build`][extension.interface.ExtensionModules.build] method MUST NOT generate any file that is not returned by the [`files`][extension.interface.ExtensionModules.files] method.
