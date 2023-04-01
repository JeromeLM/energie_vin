import abc
from typing import List

from src.domain.wine import Wine


class IWineRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, wine: Wine):
        pass

    @abc.abstractmethod
    def list(self) -> List[Wine]:
        pass
