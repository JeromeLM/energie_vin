from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.application.use_cases.view_wines_use_case import ViewWinesUseCase
from src.main import app, get_repository
from src.tests.builders.wine_builder import WineBuilder
from src.tests.fixtures.wine_fixture import WineFixture

client = TestClient(app)
wine_fixture = WineFixture()


def mock_repository():
    return wine_fixture.wine_repository


class TestApi(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
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
        # replace the default repository dependency with the mock repository
        app.dependency_overrides[get_repository] = lambda: mock_repository()

    def tearDown(self):
        wine_fixture.clean_repository()

    def test_list_api_endpoint_with_invalid_query_parameters_returns_422(self):
        wine_fixture.given_following_wines_exist(self.existing_wines)
        response = client.get("/wines/?min_price=abc&max_price=def")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["query", "min_price"],
                    "msg": "value is not a valid float",
                    "type": "type_error.float",
                },
                {
                    "loc": ["query", "max_price"],
                    "msg": "value is not a valid float",
                    "type": "type_error.float",
                },
            ]
        }

    def test_list_api_endpoint_returns_wines(self):
        wine_fixture.given_following_wines_exist(self.existing_wines)
        response = client.get("/wines")
        assert response.status_code == 200
        assert response.json() == [
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

    def test_list_api_endpoint_returns_wines_filtered_by_price_range(self):
        wine_fixture.given_following_wines_exist(self.existing_wines)
        response = client.get("/wines/?min_price=8&max_price=11")
        assert response.status_code == 200
        assert response.json() == [
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

    def test_list_api_endpoint_returns_wines_filtered_by_price_range_and_sorted_by_best_average_rating(  # noqa
        self,
    ):
        wine_fixture.given_following_wines_exist(self.existing_wines)
        response = client.get(
            "/wines/?min_price=10.50&max_price=13.90&sort=best_average_rating"
        )
        assert response.status_code == 200
        assert response.json() == [
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
                "name": "Château Marjosse 2019",
                "type": "rouge",
                "winery": "Château Marjosse",
                "appellation": "Bordeaux",
                "vintage": 2019,
                "ratings": [90, 92],
                "average_rating": 91,
                "price": 10.90,
            },
        ]

    def test_list_api_endpoint_with_internal_exception_raised_returns_500(self):
        wine_fixture.given_following_wines_exist(self.existing_wines)
        with patch.object(
            ViewWinesUseCase, "handle", side_effect=ValueError("a value error")
        ):
            response = client.get("/wines")
        assert response.status_code == 500
