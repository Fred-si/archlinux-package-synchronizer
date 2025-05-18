from pathlib import Path

from .interfaces import ExecutableFinderInterface, ExecutableInterface


class ExecutableFinder(ExecutableFinderInterface):
    def find_executable(self, name: str) -> ExecutableInterface:
        from shutil import which

        from ._executable import _Executable
        from .exceptions import ExecutableNotFoundError

        executable_path = which(name)

        if executable_path is None:

            raise ExecutableNotFoundError(name)

        return _Executable(Path(executable_path))
