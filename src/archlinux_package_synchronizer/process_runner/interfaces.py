from abc import ABC, abstractmethod

from .models import CapturedProcessResult, ProcessResult


class ExecutableFinderInterface(ABC):
    @abstractmethod
    def find_executable(self, command: str) -> "ExecutableInterface": ...


class ExecutableInterface(ABC):
    @abstractmethod
    def call(self, *args: str) -> ProcessResult: ...

    @abstractmethod
    def capture(self, *args: str) -> CapturedProcessResult: ...
