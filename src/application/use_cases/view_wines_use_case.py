from typing import List, Dict

from src.application.ports.wine_repository import IWineRepository
from src.domain.price_range import PriceRange


class ViewWinesUseCase:
    def __init__(self, wine_repository: IWineRepository):
        self.wine_repository = wine_repository

    def handle(
        self, sort_by_best_average_rating: bool = False, price_range: PriceRange = None
    ) -> List[Dict]:
        if price_range is not None:
            wines = self.wine_repository.list_wines_within_price_range(price_range)
        elif sort_by_best_average_rating is True:
            wines = self.wine_repository.list_by_best_average_rating()
        else:
            wines = self.wine_repository.list()
        return [wine.get_data() for wine in wines]
