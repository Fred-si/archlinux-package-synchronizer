from subprocess import CompletedProcess
from typing import override

from archlinux_package_synchronizer.package_manager._yay import Yay
from archlinux_package_synchronizer.process_runner import (
    CapturedProcessResult,
    ExecutableInterface,
    ProcessResult,
)


class BaseExecutable(ExecutableInterface):
    def call(self, *args: str) -> ProcessResult:
        raise NotImplementedError

    def capture(self, *args: str) -> CapturedProcessResult:
        raise NotImplementedError


def test_list_packages() -> None:
    class Executable(BaseExecutable):
        @override
        def capture(self, *args: str) -> CapturedProcessResult:
            assert args == ("--query", "--quiet", "--explicit")

            return CapturedProcessResult(
                completed_process=CompletedProcess(
                    ("yay", *args), 0, b"foo\nbar", b""
                )
            )

    yay = Yay(Executable())

    assert list(yay.get_explicitly_installed_packages()) == ["foo", "bar"]
