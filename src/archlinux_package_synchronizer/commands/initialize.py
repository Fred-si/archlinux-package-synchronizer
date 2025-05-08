from pathlib import Path
from typing import Annotated

import typer

from archlinux_package_synchronizer.config import DEFAULT_CONFIG_DIRECTORY
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
) -> None:
    raise NotImplementedError
