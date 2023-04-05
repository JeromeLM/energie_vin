from unittest import TestCase

from domain.price_range import PriceRange
from tests.builders.wine_builder import WineBuilder
from tests.fixtures.wine_fixture import WineFixture


class TestViewingWinesUseCase(TestCase):
    def setUp(self) -> None:
        self.wine_fixture = WineFixture()
        self.wines = []
        self.existing_wines = [
            # average : 91
            WineBuilder()
            .with_name("Château Marjosse 2019")
            .of_type("rouge")
            .from_winery("Château Marjosse")
            .of_appelation("Bordeaux")
            .of_vintage(2019)
            .rated([90, 92])
            .costing(10.90)
            .build(),
            # average : 92
            WineBuilder()
            .with_name("Viña Zorzal Garnacha 2020")
            .of_type("rouge")
            .from_winery("Viña Zorzal")
            .of_appelation("Navarre")
            .of_vintage(2020)
            .rated([92, 94, 91, 92])
            .costing(6.90)
            .build(),
            # average : 90
            WineBuilder()
            .with_name("Marius By Chapoutier Vermentino 2021")
            .of_type("blanc")
            .from_winery("M. Chapoutier")
            .of_appelation("Payd'Oc")
            .of_vintage(2021)
            .rated([90])
            .costing(6.10)
            .build(),
            # average : 91
            WineBuilder()
            .with_name("Clos Uroulat la Petite Hours 2018")
            .of_type("blanc")
            .from_winery("Domaine Uroulat")
            .of_appelation("Jurançon")
            .of_vintage(2018)
            .rated([91, 90, 92])
            .costing(9.90)
            .build(),
            # average : 93
            WineBuilder()
            .with_name("Domaines Ott By Ott Rosé 2021")
            .of_type("rosé")
            .from_winery("Domaines Ott")
            .of_appelation("Côtes de Provence")
            .of_vintage(2021)
            .rated([92, 94])
            .costing(13.90)
            .build(),
        ]

    def test_user_can_view_wines(self):
        self.wine_fixture.given_following_wines_exist(self.existing_wines)
        self.wine_fixture.when_user_wants_to_view_all_the_wines()
        self.wine_fixture.then_displayed_wines_should_be(
            [
                {
                    "name": "Château Marjosse 2019",
                    "type": "rouge",
                    "winery": "Château Marjosse",
                    "appellation": "Bordeaux",
                    "vintage": 2019,
                    "ratings": [90, 92],
                    "average_rating": 91,
                    "price": 10.90,
                },
                {
                    "name": "Viña Zorzal Garnacha 2020",
                    "type": "rouge",
                    "winery": "Viña Zorzal",
                    "appellation": "Navarre",
                    "vintage": 2020,
                    "ratings": [92, 94, 91, 92],
                    "average_rating": 92,
                    "price": 6.90,
                },
                {
                    "name": "Marius By Chapoutier Vermentino 2021",
                    "type": "blanc",
                    "winery": "M. Chapoutier",
                    "appellation": "Payd'Oc",
                    "vintage": 2021,
                    "ratings": [90],
                    "average_rating": 90,
                    "price": 6.10,
                },
                {
                    "name": "Clos Uroulat la Petite Hours 2018",
                    "type": "blanc",
                    "winery": "Domaine Uroulat",
                    "appellation": "Jurançon",
                    "vintage": 2018,
                    "ratings": [91, 90, 92],
                    "average_rating": 91,
                    "price": 9.90,
                },
                {
                    "name": "Domaines Ott By Ott Rosé 2021",
                    "type": "rosé",
                    "winery": "Domaines Ott",
                    "appellation": "Côtes de Provence",
                    "vintage": 2021,
                    "ratings": [92, 94],
                    "average_rating": 93,
                    "price": 13.90,
                },
            ]
        )

    def test_user_can_view_wines_sorted_by_best_average_rating(self):
        self.wine_fixture.given_following_wines_exist(self.existing_wines)
        self.wine_fixture.when_user_wants_to_view_all_the_wines_sorted_by_best_average_rating()  # noqa
        self.wine_fixture.then_displayed_wines_should_be(
            [
                {
                    "name": "Domaines Ott By Ott Rosé 2021",
                    "type": "rosé",
                    "winery": "Domaines Ott",
                    "appellation": "Côtes de Provence",
                    "vintage": 2021,
                    "ratings": [92, 94],
                    "average_rating": 93,
                    "price": 13.90,
                },
                {
                    "name": "Viña Zorzal Garnacha 2020",
                    "type": "rouge",
                    "winery": "Viña Zorzal",
                    "appellation": "Navarre",
                    "vintage": 2020,
                    "ratings": [92, 94, 91, 92],
                    "average_rating": 92,
                    "price": 6.90,
                },
                {
                    "name": "Château Marjosse 2019",
                    "type": "rouge",
                    "winery": "Château Marjosse",
                    "appellation": "Bordeaux",
                    "vintage": 2019,
                    "ratings": [90, 92],
                    "average_rating": 91,
                    "price": 10.90,
                },
                {
                    "name": "Clos Uroulat la Petite Hours 2018",
                    "type": "blanc",
                    "winery": "Domaine Uroulat",
                    "appellation": "Jurançon",
                    "vintage": 2018,
                    "ratings": [91, 90, 92],
                    "average_rating": 91,
                    "price": 9.90,
                },
                {
                    "name": "Marius By Chapoutier Vermentino 2021",
                    "type": "blanc",
                    "winery": "M. Chapoutier",
                    "appellation": "Payd'Oc",
                    "vintage": 2021,
                    "ratings": [90],
                    "average_rating": 90,
                    "price": 6.10,
                },
            ]
        )

    def test_user_can_view_wines_whose_price_is_included_in_a_given_price_range(self):
        self.wine_fixture.given_following_wines_exist(self.existing_wines)
        self.wine_fixture.when_user_wants_to_view_all_the_wines_with_a_price_included_in_this_price_range(  # noqa
            price_range=PriceRange(min=6.90, max=10.90)
        )
        self.wine_fixture.then_displayed_wines_should_be(
            [
                {
                    "name": "Château Marjosse 2019",
                    "type": "rouge",
                    "winery": "Château Marjosse",
                    "appellation": "Bordeaux",
                    "vintage": 2019,
                    "ratings": [90, 92],
                    "average_rating": 91,
                    "price": 10.90,
                },
                {
                    "name": "Viña Zorzal Garnacha 2020",
                    "type": "rouge",
                    "winery": "Viña Zorzal",
                    "appellation": "Navarre",
                    "vintage": 2020,
                    "ratings": [92, 94, 91, 92],
                    "average_rating": 92,
                    "price": 6.90,
                },
                {
                    "name": "Clos Uroulat la Petite Hours 2018",
                    "type": "blanc",
                    "winery": "Domaine Uroulat",
                    "appellation": "Jurançon",
                    "vintage": 2018,
                    "ratings": [91, 90, 92],
                    "average_rating": 91,
                    "price": 9.90,
                },
            ]
        )

    def test_user_can_view_wines_whose_price_is_included_in_a_given_price_range_and_sorted_by_best_average_rating(  # noqa
        self,
    ):
        self.wine_fixture.given_following_wines_exist(self.existing_wines)
        self.wine_fixture.when_user_wants_to_view_all_the_wines_with_a_price_included_in_this_price_range_and_sorted_by_best_average_rating(  # noqa
            price_range=PriceRange(min=6.90, max=10.90)
        )
        self.wine_fixture.then_displayed_wines_should_be(
            [
                {
                    "name": "Viña Zorzal Garnacha 2020",
                    "type": "rouge",
                    "winery": "Viña Zorzal",
                    "appellation": "Navarre",
                    "vintage": 2020,
                    "ratings": [92, 94, 91, 92],
                    "average_rating": 92,
                    "price": 6.90,
                },
                {
                    "name": "Château Marjosse 2019",
                    "type": "rouge",
                    "winery": "Château Marjosse",
                    "appellation": "Bordeaux",
                    "vintage": 2019,
                    "ratings": [90, 92],
                    "average_rating": 91,
                    "price": 10.90,
                },
                {
                    "name": "Clos Uroulat la Petite Hours 2018",
                    "type": "blanc",
                    "winery": "Domaine Uroulat",
                    "appellation": "Jurançon",
                    "vintage": 2018,
                    "ratings": [91, 90, 92],
                    "average_rating": 91,
                    "price": 9.90,
                },
            ]
        )
