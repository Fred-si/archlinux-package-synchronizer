import subprocess

from pathlib import Path
from typing import Final

from .interfaces import ExecutableInterface
from .models import CapturedProcessResult, ProcessResult


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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False

        return self._path == other._path

    __hash__ = ExecutableInterface.__hash__
