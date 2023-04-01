from typing import List, Dict

from src.application.ports.wine_repository import IWineRepository


class ViewWinesUseCase:
    def __init__(self, wine_repository: IWineRepository):
        self.wine_repository = wine_repository

    def handle(self, sort_by_best_average_rating: bool = False) -> List[Dict]:
        if sort_by_best_average_rating is True:
            wines = self.wine_repository.list_by_best_average_rating()
        else:
            wines = self.wine_repository.list()
        return [wine.get_data() for wine in wines]
