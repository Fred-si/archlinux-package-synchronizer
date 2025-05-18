class ExecutableNotFoundError(OSError):
    def __init__(self, name: str) -> None:
        super().__init__(f'Executable "{name}" not found in path.')


class NotCapturedProcessError(ValueError):
    pass
