from enum import StrEnum
from typing import assert_never

from archlinux_package_synchronizer.process_runner import ExecutableFinder

from .interfaces import PackageManagerInterface


class PackageManagerName(StrEnum):
    YAY = "yay"
    PACMAN = "pacman"


def create_manager(
    executable_finder: ExecutableFinder, name: PackageManagerName
) -> PackageManagerInterface:
    find_executable = executable_finder.find_executable

    match name:
        case PackageManagerName.YAY:
            from ._yay import Yay

            return Yay(find_executable("yay"))

        case PackageManagerName.PACMAN:
            raise NotImplementedError

        case _:
            assert_never(name)
