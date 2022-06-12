from pathlib import Path

from extension.interface import ExtensionModules


class MockCExtensionModules(ExtensionModules):
    def inputs(self):
        return [f'{self.name}/{module}.h' for module in self.config.get('modules', [])]

    def outputs(self):
        return [f'{self.name}/{module}.so' for module in self.config.get('modules', [])]

    def generate_inputs(self, data):
        data[self.name] = True
        for relative_path in self.inputs():
            path = Path(self.root, relative_path)
            path.parent.mkdir(exist_ok=True)
            path.touch()

    def generate_outputs(self, data):
        data[self.name] = True
        for relative_path in self.outputs():
            path = Path(self.root, relative_path)
            path.parent.mkdir(exist_ok=True)
            path.touch()
