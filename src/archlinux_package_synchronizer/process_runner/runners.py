import subprocess

from pathlib import Path
from typing import Final

from .interfaces import ExecutableFinderInterface, ExecutableInterface
from .models import CapturedProcessResult, ProcessResult


class ExecutableFinder(ExecutableFinderInterface):
    def __init__(self):
        self._factory = _Executable

    def find_executable(self, name: str) -> ExecutableInterface:
        from shutil import which

        executable_path = which(name)

        if executable_path is None:
            raise ExecutableNotFoundError(name)

        return self._factory(Path(executable_path))


class _Executable(ExecutableInterface):
    def __init__(self, executable: Path) -> None:
        self._path: Final = executable

    @property
    def path(self) -> Path:
        return self._path

    def call(self, *args: str) -> ProcessResult:
        return ProcessResult(self._run(*args, capture_output=False))

    def capture(self, *args: str) -> CapturedProcessResult:
        return CapturedProcessResult(self._run(*args, capture_output=True))

    def _run(
        self, *args: str, capture_output: bool
    ) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(  # noqa: S603
            (self._path, *args), capture_output=capture_output, check=False
        )

    def __repr__(self) -> str:
        return f"{type(self)}({self._path!r})"


class ExecutableNotFoundError(OSError):
    def __init__(self, name: str) -> None:
        super().__init__(f'Executable "{name}" not found in path.')
