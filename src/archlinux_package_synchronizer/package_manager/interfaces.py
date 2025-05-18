from abc import ABC, abstractmethod
from collections.abc import Collection


class PackageManagerInterface(ABC):
    @abstractmethod
    def get_explicitly_installed_packages(self) -> Collection[str]: ...
