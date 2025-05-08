def hello_world() -> None:
    print(f"{hello()}, {world()}!".capitalize())


def hello() -> str:
    """Say hello.

    >>> hello()
    'hello'
    """
    return "hello"


def world() -> str:
    """Say world.

    >>> world()
    'world'
    """
    return "world"
