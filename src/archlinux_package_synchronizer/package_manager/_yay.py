from collections.abc import Sequence

from .abstract_package_manager import AbstractPackageManager


class Yay(AbstractPackageManager):
    @property
    def _explicitly_installed_options(self) -> Sequence[str]:
        return ["--query", "--quiet", "--explicit"]

    @property
    def executable_name(self) -> str:
        return "yay"
