from typing import List, Dict

from src.application.ports.wine_repository import IWineRepository


class ViewWinesUseCase:
    def __init__(self, wine_repository: IWineRepository):
        self.wine_repository = wine_repository

    def handle(self) -> List[Dict]:
        wines = self.wine_repository.list()
        return [wine.get_data() for wine in wines]
