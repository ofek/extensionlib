import sys

if sys.version_info >= (3, 11):
    import tomllib

    def load_toml(text: str) -> dict:
        return tomllib.loads(text)

else:
    import tomli

    def load_toml(text: str) -> dict:
        return tomli.loads(text)
