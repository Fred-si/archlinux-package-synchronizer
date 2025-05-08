import typer


def main() -> typer.Typer:
    from .main import hello_world

    return typer.run(hello_world)
