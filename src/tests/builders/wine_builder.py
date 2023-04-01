from dataclasses import dataclass, field
from typing import List

from src.domain.wine import Wine


@dataclass
class WineBuilder:
    name: str = "Château Jouvente 2018"
    type: str = "rouge"
    winery: str = "Château Jouvente"
    appellation: str = "Graves AOP"
    vintage: int = 2018
    ratings: List[int] = field(default_factory=lambda: [88, 90])
    price: float = 17.90

    def with_name(self, name: str):
        self.name = name
        return self

    def of_type(self, type: str):
        self.type = type
        return self

    def from_winery(self, winery: str):
        self.winery = winery
        return self

    def of_appelation(self, appellation: str):
        self.appellation = appellation
        return self

    def of_vintage(self, vintage: int):
        self.vintage = vintage
        return self

    def rated(self, ratings: List[int]):
        self.ratings = ratings.copy()
        return self

    def costing(self, price: float):
        self.price = price
        return self

    def build(self) -> Wine:
        return Wine.create_from_data(
            {
                "name": self.name,
                "type": self.type,
                "winery": self.winery,
                "appellation": self.appellation,
                "vintage": self.vintage,
                "ratings": self.ratings.copy(),
                "price": self.price,
            }
        )
