from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from _pytest.monkeypatch import MonkeyPatch

from archlinux_package_synchronizer import process_runner
from archlinux_package_synchronizer.commands import initialize
from archlinux_package_synchronizer.commands.initialize import (
    NotAnEmptyDirectoryError,
)
from archlinux_package_synchronizer.config import (
    ARCHLINUX_PACKAGE_NAME,
    PACKAGE_LIST_DIRECTORY_NAME,
)
from archlinux_package_synchronizer.package_manager import PackageManagerName
from archlinux_package_synchronizer.process_runner import (
    CapturedProcessResult,
    ExecutableFinderInterface,
    ExecutableInterface,
    ProcessResult,
)


@pytest.fixture(autouse=True)
def patch_executable_finder(monkeypatch: MonkeyPatch) -> None:
    class Executable(ExecutableInterface):
        def call(self, *args: str) -> ProcessResult:
            raise NotImplementedError

        def capture(self, *args: str) -> CapturedProcessResult:
            raise NotImplementedError

    class Finder(ExecutableFinderInterface):
        def find_executable(self, name: str) -> ExecutableInterface:
            if name != PackageManagerName.YAY:
                raise ValueError(name)

            return Executable()

    monkeypatch.setattr(process_runner, "ExecutableFinder", Finder)


@pytest.fixture(autouse=True)
def yay_mock(monkeypatch: MonkeyPatch) -> Mock:
    from archlinux_package_synchronizer.package_manager import _yay

    mock = Mock(spec=_yay.Yay)
    mock.get_explicitly_installed_packages.return_value = []

    monkeypatch.setattr(_yay, "Yay", MagicMock(return_value=mock))

    return mock


@pytest.fixture
def list_path(tmp_path: Path) -> Path:
    return tmp_path / PACKAGE_LIST_DIRECTORY_NAME


def test_initialize_should_raise_when_config_dir_is_file(
    tmp_path: Path,
) -> None:
    file = tmp_path / "foo"
    file.touch()

    with pytest.raises(NotADirectoryError, match=str(file)):
        initialize(file)


def test_initialize_should_raise_when_config_dir_is_symlink_to_file(
    tmp_path: Path,
) -> None:
    file = tmp_path / "file"
    file.touch()
    link = tmp_path / "link"
    link.symlink_to("file")

    with pytest.raises(NotADirectoryError, match=str(file)):
        initialize(link)


def test_initialize_should_not_raise_when_config_dir_is_symlink_to_directory(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "directory"
    directory.mkdir()
    assert directory.is_dir()
    link = tmp_path / "link"
    link.symlink_to("file")

    initialize(link)


def test_initialize_should_create_config_directory_when_not_exists(
    tmp_path: Path,
) -> None:
    config_dir = tmp_path / "config"

    initialize(config_dir)

    assert config_dir.is_dir()


def test_initialize_should_create_package_list_directory_when_not_exists(
    tmp_path: Path, list_path: Path
) -> None:
    initialize(tmp_path)

    assert list_path.is_dir()


def test_initialize_should_create_parent_directories(tmp_path: Path) -> None:
    config_dir = tmp_path / "a" / "b" / "c"
    initialize(config_dir)

    assert config_dir.is_dir()


def test_initialize_should_raise_when_config_package_list_directory_is_not_empty(
    tmp_path: Path, list_path: Path
) -> None:
    list_path.mkdir(parents=True, exist_ok=True)
    (list_path / "file").touch()

    with pytest.raises(NotAnEmptyDirectoryError, match=str(tmp_path)):
        initialize(tmp_path)


def test_initialize_should_create_base_file(
    tmp_path: Path, list_path: Path
) -> None:
    initialize(tmp_path)
    assert list_path.is_dir()

    base_file = list_path / "00_base"
    assert base_file.is_file()
    assert base_file.read_text() == f"base\n{ARCHLINUX_PACKAGE_NAME}\n"


def test_initialize_should_list_installed_packages(
    yay_mock: Mock, tmp_path: Path, list_path: Path
) -> None:
    yay_mock.get_explicitly_installed_packages.return_value = [
        "base",
        ARCHLINUX_PACKAGE_NAME,
        "foo",
        "bar",
    ]

    initialize(tmp_path)

    assert (list_path / "01_explicitly_installed").read_text() == "bar\nfoo\n"
