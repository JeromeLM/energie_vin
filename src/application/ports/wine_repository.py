import abc
from typing import List

from src.domain.price_range import PriceRange
from src.domain.wine import Wine


class IWineRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, wine: Wine):
        pass

    @abc.abstractmethod
    def list(self) -> List[Wine]:
        pass

    @abc.abstractmethod
    def list_by_best_average_rating(self) -> List[Wine]:
        pass

    @abc.abstractmethod
    def list_wines_within_price_range(self, price_range: PriceRange) -> List[Wine]:
        pass
