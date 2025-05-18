from collections.abc import Sequence
from pathlib import Path
from typing import Final

from archlinux_package_synchronizer.path import get_path

DEFAULT_CONFIG_DIRECTORY: Final = Path("/etc/archlinux-package-synchronizer.d")
ARCHLINUX_PACKAGE_NAME: Final = "archlinux-package-synchronizer"
PATH: Final[Sequence[Path]] = get_path()
PACKAGE_LIST_DIRECTORY_NAME = "package_list"
