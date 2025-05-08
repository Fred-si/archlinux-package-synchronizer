from functools import cached_property
from subprocess import CalledProcessError, CompletedProcess
from typing import Final, Self

from archlinux_package_synchronizer.process_runner.exceptions import (
    NotCapturedProcessError,
)


class ReturnCode:
    def __init__(self, value: int) -> None:
        self._value: Final = value

    @property
    def is_success(self) -> bool:
        return self._value == 0

    def __int__(self) -> int:
        return self._value


class ProcessResult:
    def __init__(self, completed_process: CompletedProcess[bytes]) -> None:
        self._completed_process: Final = completed_process

    @property
    def is_success(self) -> bool:
        return self.return_code.is_success

    @cached_property
    def return_code(self) -> ReturnCode:
        return ReturnCode(self._completed_process.returncode)

    def ensure_success(self) -> Self:
        if not self.is_success:

            raise CalledProcessError(
                int(self.return_code),
                " ".join(map(str, self._completed_process.args)),
                self._completed_process.stdout,
                self._completed_process.stderr,
            )

        return self


class CapturedProcessResult(ProcessResult):
    def __init__(self, completed_process: CompletedProcess[bytes]) -> None:
        if completed_process.stdout is None or completed_process.stderr is None:
            msg = "process outputs have not been captured"
            raise NotCapturedProcessError(msg)

        super().__init__(completed_process)

    @cached_property
    def standard_output(self) -> str:
        return self._completed_process.stdout.decode()

    @cached_property
    def standard_error(self) -> str:
        return self._completed_process.stderr.decode()
