from pathlib import Path

import tomllib

PYPROJECT_FILE = Path("pyproject.toml")


def read_package_version() -> str:
    data = tomllib.loads(PYPROJECT_FILE.read_text(encoding="utf-8"))
    version = data.get("project", {}).get("version")
    if version is None:
        raise SystemExit("Unable to find package version in pyproject.toml")
    return version


if __name__ == "__main__":
    print(read_package_version())
