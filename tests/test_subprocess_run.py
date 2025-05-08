import subprocess

import pytest


def test_subprocess_run_raise_file_not_found_error() -> None:
    """Verify that the fixture drop_path in conftest is used and prevent run command."""
    with pytest.raises(FileNotFoundError):
        subprocess.run(["echo", "foo"], check=True)  # noqa: S607
