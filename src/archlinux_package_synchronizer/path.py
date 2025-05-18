from collections.abc import Sequence
from os import environ
from pathlib import Path


def get_path() -> Sequence[Path]:
    path = environ.get("PATH")

    if not path:
        return ()

    return tuple(map(Path, path.split(":")))
