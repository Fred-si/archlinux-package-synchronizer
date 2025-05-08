from pathlib import Path

from archlinux_package_synchronizer.config import DEFAULT_CONFIG_DIRECTORY


def test_hello():
    assert isinstance(DEFAULT_CONFIG_DIRECTORY, Path)
