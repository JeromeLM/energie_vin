from typing import List, Dict
from unittest import TestCase

from src.application.use_cases.view_wines_use_case import ViewWinesUseCase
from src.domain.wine import Wine
from src.tests.adapters.in_memory_wine_repository import InMemoryWineRepository
from src.tests.builders.wine_builder import WineBuilder


class TestViewingWinesUseCase(TestCase):
    def setUp(self) -> None:
        self.wine_repository = InMemoryWineRepository()
        self.wines = []

    def test_user_can_view_wines(self):
        self.given_following_wines_exist(
            [
                WineBuilder()
                .with_name("Château Marjosse 2019")
                .of_type("rouge")
                .from_winery("Château Marjosse")
                .of_appelation("Bordeaux")
                .of_vintage(2019)
                .rated([90])
                .costing(10.90)
                .build(),
                WineBuilder()
                .with_name("Viña Zorzal Garnacha 2020")
                .of_type("rouge")
                .from_winery("Viña Zorzal")
                .of_appelation("Navarre")
                .of_vintage(2020)
                .rated([92])
                .costing(6.90)
                .build(),
                WineBuilder()
                .with_name("Marius By Chapoutier Vermentino 2021")
                .of_type("blanc")
                .from_winery("M. Chapoutier")
                .of_appelation("Payd'Oc")
                .of_vintage(2021)
                .rated([90])
                .costing(6.10)
                .build(),
                WineBuilder()
                .with_name("Clos Uroulat la Petite Hours 2018")
                .of_type("blanc")
                .from_winery("Domaine Uroulat")
                .of_appelation("Jurançon")
                .of_vintage(2018)
                .rated([91])
                .costing(9.90)
                .build(),
                WineBuilder()
                .with_name("Domaines Ott By Ott Rosé 2021")
                .of_type("rosé")
                .from_winery("Domaines Ott")
                .of_appelation("Côtes de Provence")
                .of_vintage(2021)
                .rated([92])
                .costing(13.90)
                .build(),
            ]
        )
        self.when_user_wants_to_view_all_the_wines()
        self.then_displayed_wines_should_be(
            [
                {
                    "name": "Château Marjosse 2019",
                    "type": "rouge",
                    "winery": "Château Marjosse",
                    "appellation": "Bordeaux",
                    "vintage": 2019,
                    "ratings": [90],
                    "price": 10.90,
                },
                {
                    "name": "Viña Zorzal Garnacha 2020",
                    "type": "rouge",
                    "winery": "Viña Zorzal",
                    "appellation": "Navarre",
                    "vintage": 2020,
                    "ratings": [92],
                    "price": 6.90,
                },
                {
                    "name": "Marius By Chapoutier Vermentino 2021",
                    "type": "blanc",
                    "winery": "M. Chapoutier",
                    "appellation": "Payd'Oc",
                    "vintage": 2021,
                    "ratings": [90],
                    "price": 6.10,
                },
                {
                    "name": "Clos Uroulat la Petite Hours 2018",
                    "type": "blanc",
                    "winery": "Domaine Uroulat",
                    "appellation": "Jurançon",
                    "vintage": 2018,
                    "ratings": [91],
                    "price": 9.90,
                },
                {
                    "name": "Domaines Ott By Ott Rosé 2021",
                    "type": "rosé",
                    "winery": "Domaines Ott",
                    "appellation": "Côtes de Provence",
                    "vintage": 2021,
                    "ratings": [92],
                    "price": 13.90,
                },
            ]
        )

    def given_following_wines_exist(self, wines: List[Wine]):
        for wine in wines:
            self.wine_repository.save(wine)

    def when_user_wants_to_view_all_the_wines(self):
        view_wines_use_case = ViewWinesUseCase(wine_repository=self.wine_repository)
        self.wines = view_wines_use_case.handle()

    def then_displayed_wines_should_be(self, expected_wines: List[Dict]):
        assert self.wines == expected_wines
