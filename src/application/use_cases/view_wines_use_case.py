from dataclasses import dataclass
from typing import List, Dict, Union

from application.ports.wine_repository import IWineRepository
from domain.price_range import PriceRange


@dataclass
class ViewWinesCommand:
    price_range: PriceRange = None
    sort_by_best_average_rating: bool = False


class ViewWinesUseCase:
    def __init__(self, wine_repository: IWineRepository):
        self.wine_repository = wine_repository

    def handle(self, view_wines_command: ViewWinesCommand) -> List[Dict]:
        filters = self._build_filters(view_wines_command)
        sort = self._build_sort(view_wines_command)
        wines = self.wine_repository.list(filters=filters, sort=sort)
        return [wine.get_data() for wine in wines]

    def _build_filters(self, view_wines_command: ViewWinesCommand) -> Union[Dict, None]:
        return (
            {"price_range": view_wines_command.price_range}
            if view_wines_command.price_range is not None
            else None
        )

    def _build_sort(self, view_wines_command: ViewWinesCommand) -> Union[str, None]:
        return (
            "best_average_rating"
            if view_wines_command.sort_by_best_average_rating is True
            else None
        )
