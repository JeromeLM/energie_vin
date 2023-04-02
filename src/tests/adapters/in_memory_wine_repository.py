from typing import List, Dict

from src.application.ports.wine_repository import IWineRepository
from src.domain.price_range import PriceRange
from src.domain.wine import Wine


class InMemoryWineRepository(IWineRepository):
    def __init__(self):
        self.wines = []

    def save(self, wine: Wine):
        self.wines.append(wine)

    def list(self, filters: Dict = None, sort: str = None) -> List[Wine]:
        wines = self._list()
        if filters is not None and "price_range" in filters:
            wines = self._filter_by_price_range(wines, filters["price_range"])
        if sort is not None and sort == "best_average_rating":
            wines = self._sort_by_best_average_rating(wines)
        return wines

    def _list(self) -> List[Wine]:
        return self.wines.copy()

    def _filter_by_price_range(
        self, wines: List[Wine], price_range: PriceRange
    ) -> List[Wine]:
        return [wine for wine in wines if price_range.is_price_within(wine.price)]

    def _sort_by_best_average_rating(self, wines: List[Wine]) -> List[Wine]:
        return sorted(wines, key=lambda wine: wine.get_average_rating(), reverse=True)
