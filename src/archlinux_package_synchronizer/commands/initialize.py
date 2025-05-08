from collections.abc import Iterable
from pathlib import Path
from typing import Annotated

import typer

from archlinux_package_synchronizer.config import (
    ARCHLINUX_PACKAGE_NAME,
    DEFAULT_CONFIG_DIRECTORY,
    PACKAGE_LIST_DIRECTORY_NAME,
)
from archlinux_package_synchronizer.console import standard_output
from archlinux_package_synchronizer.package_manager import PackageManagerName

from .app import app


@app.command()
def initialize(
    config_dir: Annotated[
        Path,
        typer.Option(
            help="Path to the config directory",
            readable=True,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = DEFAULT_CONFIG_DIRECTORY,
    package_list_directory_name: Annotated[
        str, typer.Option(help="The name of the package list directory")
    ] = PACKAGE_LIST_DIRECTORY_NAME,
    package_manager_name: PackageManagerName = PackageManagerName.YAY,
) -> None:
    """
    Create configuration directory and initialize it with installed packages.

    The configuration directory MUST NOT exists.
    """
    from archlinux_package_synchronizer.package_manager import create_manager
    from archlinux_package_synchronizer.process_runner import ExecutableFinder

    config_dir = config_dir.resolve()
    if config_dir.exists() and not config_dir.is_dir():
        raise NotADirectoryError(config_dir)

    list_dir = config_dir / package_list_directory_name

    list_dir.mkdir(exist_ok=True, parents=True)
    if tuple(list_dir.iterdir()):
        raise NotAnEmptyDirectoryError(list_dir)

    package_manager = create_manager(ExecutableFinder(), package_manager_name)

    base_packages = ["base", ARCHLINUX_PACKAGE_NAME]
    base_file = list_dir / "00_base"
    create_file(base_file, "\n".join(base_packages))

    installed_packages = set(
        package_manager.get_explicitly_installed_packages()
    ) - set(base_packages)
    installed_file = list_dir / "01_explicitly_installed"
    create_file(installed_file, "\n".join(sorted(installed_packages)))

    standard_output.print(
        "\n"
        f"Initialization complete."
        f" You can check {installed_file} for list of installed packages,"
        f" feel free to reorder/split it, add or remove packages."
        "\n"
        f"[important]You should never[/important] manually edit or remove {base_file}."
    )


def create_file(
    file: Path, content: str | Iterable[str], *, end: str = "\n"
) -> None:
    if file.exists():
        raise FileExistsError(file)

    if isinstance(content, str):
        content = [content]

    file.write_text("\n".join(content) + end)
    standard_output.print(f"created file {file}")


class NotAnEmptyDirectoryError(OSError):
    pass
