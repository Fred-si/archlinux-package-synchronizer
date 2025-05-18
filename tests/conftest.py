from unittest.mock import MagicMock

import pytest

from _pytest.monkeypatch import MonkeyPatch

from archlinux_package_synchronizer.process_runner import (
    ExecutableInterface,
    runners,
)


@pytest.fixture(autouse=True)
def patch_run(monkeypatch: MonkeyPatch) -> None:
    """Auto-patch subprocess.run to prevent run command on local environment."""
    import subprocess

    monkeypatch.setattr(
        subprocess, "run", MagicMock(side_effect=NotImplementedError)
    )


@pytest.fixture(autouse=True)
def executable_mock(monkeypatch: MonkeyPatch) -> MagicMock:
    mock = MagicMock(spec=ExecutableInterface)
    monkeypatch.setattr(runners, "_Executable", mock)

    return mock
