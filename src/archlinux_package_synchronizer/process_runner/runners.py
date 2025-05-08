import subprocess

from pathlib import Path

from .interfaces import ExecutableFinderInterface, ExecutableInterface
from .models import CapturedProcessResult, ProcessResult


class ExecutableFinder(ExecutableFinderInterface):
    def __init__(self) -> None:
        self._which = Executable(Path("which"))

    def find_executable(self, name: str) -> ExecutableInterface:
        result = self._which.capture(name)

        if not result.is_success:
            raise ExecutableNotExistsError(name)

        return Executable(Path(result.standard_output.strip()))


class Executable(ExecutableInterface):
    def __init__(self, executable: Path) -> None:
        self._executable = executable

    def call(self, *args: str) -> ProcessResult:
        return ProcessResult(self._run(*args, capture_output=False))

    def capture(self, *args: str) -> CapturedProcessResult:
        return CapturedProcessResult(self._run(*args, capture_output=True))

    def _run(
        self, *args: str, capture_output: bool
    ) -> subprocess.CompletedProcess[bytes]:

        return subprocess.run(  # noqa: S603
            (self._executable, *args),
            capture_output=capture_output,
            check=False,
        )

    def __repr__(self) -> str:
        return f"Executable({self._executable!r})"


class ExecutableNotExistsError(OSError):
    def __init__(self, name: str) -> None:
        super().__init__(f'Executable "{name}" not found in path.')
