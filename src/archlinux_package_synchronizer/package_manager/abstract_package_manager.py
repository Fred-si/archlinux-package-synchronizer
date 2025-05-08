from abc import abstractmethod
from collections.abc import Collection, Sequence

from archlinux_package_synchronizer.process_runner import ExecutableInterface

from .interfaces import PackageManagerInterface


class AbstractPackageManager(PackageManagerInterface):
    def __init__(self, executable: ExecutableInterface) -> None:
        self._executable = executable

    @property
    @abstractmethod
    def _explicitly_installed_options(self) -> Sequence[str]: ...

    def get_explicitly_installed_packages(self) -> Collection[str]:
        return (
            self._executable.capture(*self._explicitly_installed_options)
            .ensure_success()
            .standard_output.split()
        )
