from typing import List

from src.application.ports.wine_repository import IWineRepository
from src.domain.wine import Wine


class InMemoryWineRepository(IWineRepository):
    def __init__(self):
        self.wines = []

    def save(self, wine: Wine):
        self.wines.append(wine)

    def list(self) -> List[Wine]:
        return self.wines.copy()

    def list_by_best_average_rating(self) -> List[Wine]:
        return sorted(
            self.list(), key=lambda wine: wine.get_average_rating(), reverse=True
        )
