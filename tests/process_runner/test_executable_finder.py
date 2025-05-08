from pathlib import Path

import pytest

from archlinux_package_synchronizer.process_runner import (
    ExecutableFinder,
    ExecutableNotFoundError,
)
from archlinux_package_synchronizer.process_runner._executable import (
    _Executable,
)

from tests.conftest import SetPath


class TestExecutableFinder:
    def test_find_should_raise_when_executable_not_exists(self) -> None:
        name = "this-executable-does-not-exist"

        with pytest.raises(ExecutableNotFoundError, match=name):
            ExecutableFinder().find_executable(name)

    def test_find_should_return_executable_when_executable_exists(
        self, tmp_path: Path, set_path: SetPath
    ) -> None:
        executable_path = tmp_path / "this-executable-exist"
        executable_path.touch(mode=0o755)
        set_path(executable_path.parent)

        executable = ExecutableFinder().find_executable(executable_path.name)

        assert executable == _Executable(executable_path)
