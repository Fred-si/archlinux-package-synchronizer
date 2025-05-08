from pathlib import Path
from shutil import which

from ._executable import _Executable
from .exceptions import ExecutableNotFoundError
from .interfaces import ExecutableFinderInterface, ExecutableInterface


class ExecutableFinder(ExecutableFinderInterface):
    def find_executable(self, name: str) -> ExecutableInterface:
        executable_path = which(name)

        if executable_path is None:
            raise ExecutableNotFoundError(name)

        return _Executable(Path(executable_path))
