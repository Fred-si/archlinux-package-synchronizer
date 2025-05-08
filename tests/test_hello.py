from pathlib import Path

from archlinux_package_synchronizer.config import DEFAULT_CONFIG_DIRECTORY


def test_hello() -> None:
    assert isinstance(DEFAULT_CONFIG_DIRECTORY, Path)
