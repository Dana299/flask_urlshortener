from abc import ABC, abstractmethod
from typing import Optional


class AbstractClient(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def set(self, key: str, mapping: dict, ttl: Optional[int] = None):
        """Set mapping under the key with ttl if given."""
        pass

    @abstractmethod
    def get(self, key: str):
        pass