from pathlib import Path
from typing import Protocol

import pytest

from archlinux_package_synchronizer.path import get_path


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

    path = list(get_path())

    assert path == []


def test_get_path_should_contain_one_element_when_path_env_contain_only_one_element(
    tmp_path: Path, set_path: SetPath
) -> None:
    set_path(tmp_path)

    path = list(get_path())

    assert path == [tmp_path]


def test_get_path_should_contain_two_elements_when_path_env_contain_two_elements(
    tmp_path: Path, set_path: SetPath
) -> None:

    set_path(tmp_path / "foo", tmp_path / "bar")

    path = sorted(get_path())

    assert path == [tmp_path / "bar", tmp_path / "foo"]
