def initialize() -> None:
    import typer

    from .commands import initialize

    typer.run(initialize)
