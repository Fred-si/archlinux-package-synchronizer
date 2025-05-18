from pathlib import Path
from typing import Protocol
from unittest.mock import MagicMock

import pytest

from _pytest.monkeypatch import MonkeyPatch

from archlinux_package_synchronizer.process_runner import (
    ExecutableInterface,
    runners,
)


class SetPath(Protocol):
    def __call__(self, *path: Path) -> None: ...


@pytest.fixture
def set_path(monkeypatch: pytest.MonkeyPatch) -> SetPath:

    def ret(*path: Path) -> None:
        monkeypatch.setenv("PATH", ":".join(map(str, path)))

    return ret


@pytest.fixture(autouse=True)
def drop_path(set_path: SetPath) -> None:
    """Drop PATH environment to prevent run command on local environment."""
    set_path()


@pytest.fixture(autouse=True)
def executable_mock(monkeypatch: MonkeyPatch) -> MagicMock:
    mock = MagicMock(spec=ExecutableInterface)
    monkeypatch.setattr(runners, "_Executable", mock)

    return mock
