import abc
from typing import List, Dict

from src.domain.wine import Wine


class IWineRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, wine: Wine):
        pass

    @abc.abstractmethod
    def list(self, filters: Dict = None, sort: str = None) -> List[Wine]:
        pass
