from pathlib import Path
from typing import Protocol

import pytest

from archlinux_package_synchronizer.os_path import OsPath, get_path


class SetPath(Protocol):
    def __call__(self, *path: Path) -> None: ...


@pytest.fixture
def set_path(monkeypatch: pytest.MonkeyPatch) -> SetPath:
    def ret(*path: Path) -> None:
        monkeypatch.setenv("PATH", ":".join(map(str, path)))

    return ret


def test_get_path_should_be_an_empty_sequence_when_path_env_is_empty(
    set_path: SetPath,
) -> None:
    set_path()

    path = get_path()

    assert path == OsPath()


def test_get_path_should_contain_one_element_when_path_env_contain_only_one_element(
    tmp_path: Path, set_path: SetPath
) -> None:
    set_path(tmp_path)

    path = get_path()

    assert path == OsPath([tmp_path])


def test_get_path_should_contain_two_elements_when_path_env_contain_two_elements(
    tmp_path: Path, set_path: SetPath
) -> None:

    set_path(tmp_path / "foo", tmp_path / "bar")

    path = get_path()

    assert path == OsPath((tmp_path / "foo", tmp_path / "bar"))
