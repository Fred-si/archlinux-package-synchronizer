from os import environ
from pathlib import Path


class OsPath(tuple[Path]):
    __slots__ = ()


def get_path() -> OsPath:
    path = environ.get("PATH")

    if not path:
        return OsPath()

    return OsPath(map(Path, path.split(":")))
