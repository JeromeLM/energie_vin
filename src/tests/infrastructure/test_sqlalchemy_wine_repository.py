from unittest import TestCase

from sqlalchemy import text

from src.domain.price_range import PriceRange
from src.infrastructure.adapters.sqlalchemy_wine_repository import (
    SqlAlchemyWineRepository,
)
from src.infrastructure.session_factory import SessionFactory
from src.tests.builders.wine_builder import WineBuilder


class TestSqlAlchemyWineRepository(TestCase):
    def setUp(self) -> None:
        self.session = SessionFactory.build(exec_profile="test")
        self.session.execute(text("TRUNCATE TABLE wines"))
        self.session.commit()

    def test_sqlalchemy_wine_repository_can_save_a_wine(self):
        new_wine = (
            WineBuilder()
            .with_name("Château ZZZ 2022")
            .of_type("blanc")
            .from_winery("Château ZZZ")
            .of_appelation("Entre-deux-mers")
            .of_vintage(2022)
            .rated([94, 90, 92])
            .costing(10.50)
            .build()
        )
        repository = SqlAlchemyWineRepository(self.session)

        repository.save(new_wine)

        rows = list(
            self.session.execute(
                text(
                    'SELECT name, type, winery, appellation, vintage, ratings, price FROM "wines"'  # noqa
                )
            )
        )
        assert rows == [
            (
                "Château ZZZ 2022",
                "blanc",
                "Château ZZZ",
                "Entre-deux-mers",
                2022,
                [94, 90, 92],
                10.50,
            )
        ]

    def test_sqlalchemy_wine_repository_can_list_wines(self):
        self._insert_wines()
        expected = [
            WineBuilder()
            .with_name("Château YYY 2021")
            .of_type("rosé")
            .from_winery("Château YYY")
            .of_appelation("Côte de Provence")
            .of_vintage(2021)
            .rated([89, 91])
            .costing(9.90)
            .build(),
            WineBuilder()
            .with_name("Château XXX 2020")
            .of_type("rouge")
            .from_winery("Château XXX")
            .of_appelation("Haut-Médoc")
            .of_vintage(2020)
            .rated([90, 91, 92])
            .costing(11.90)
            .build(),
            WineBuilder()
            .with_name("Château ZZZ 2022")
            .of_type("blanc")
            .from_winery("Château ZZZ")
            .of_appelation("Entre-deux-mers")
            .of_vintage(2022)
            .rated([94, 90, 92])
            .costing(10.50)
            .build(),
        ]
        repository = SqlAlchemyWineRepository(self.session)

        wines = repository.list()

        assert wines == expected

    def test_sqlalchemy_wine_repository_can_list_wines_filtered_by_price_range(self):
        self._insert_wines()
        expected = [
            WineBuilder()
            .with_name("Château YYY 2021")
            .of_type("rosé")
            .from_winery("Château YYY")
            .of_appelation("Côte de Provence")
            .of_vintage(2021)
            .rated([89, 91])
            .costing(9.90)
            .build(),
        ]
        repository = SqlAlchemyWineRepository(self.session)

        wines = repository.list(filters={"price_range": PriceRange(min=9.50, max=10)})

        assert wines == expected

    def test_sqlalchemy_wine_repository_can_list_wines_sorted_by_best_average_rating(
        self,
    ):
        self._insert_wines()
        expected = [
            WineBuilder()
            .with_name("Château ZZZ 2022")
            .of_type("blanc")
            .from_winery("Château ZZZ")
            .of_appelation("Entre-deux-mers")
            .of_vintage(2022)
            .rated([94, 90, 92])
            .costing(10.50)
            .build(),
            WineBuilder()
            .with_name("Château XXX 2020")
            .of_type("rouge")
            .from_winery("Château XXX")
            .of_appelation("Haut-Médoc")
            .of_vintage(2020)
            .rated([90, 91, 92])
            .costing(11.90)
            .build(),
            WineBuilder()
            .with_name("Château YYY 2021")
            .of_type("rosé")
            .from_winery("Château YYY")
            .of_appelation("Côte de Provence")
            .of_vintage(2021)
            .rated([89, 91])
            .costing(9.90)
            .build(),
        ]
        repository = SqlAlchemyWineRepository(self.session)

        wines = repository.list(sort="best_average_rating")

        assert wines == expected

    def test_sqlalchemy_wine_repository_can_list_wines_filtered_by_price_range_and_sorted_by_best_average_rating(  # noqa
        self,
    ):
        self._insert_wines()
        expected = [
            WineBuilder()
            .with_name("Château ZZZ 2022")
            .of_type("blanc")
            .from_winery("Château ZZZ")
            .of_appelation("Entre-deux-mers")
            .of_vintage(2022)
            .rated([94, 90, 92])
            .costing(10.50)
            .build(),
            WineBuilder()
            .with_name("Château YYY 2021")
            .of_type("rosé")
            .from_winery("Château YYY")
            .of_appelation("Côte de Provence")
            .of_vintage(2021)
            .rated([89, 91])
            .costing(9.90)
            .build(),
        ]
        repository = SqlAlchemyWineRepository(self.session)

        wines = repository.list(
            filters={"price_range": PriceRange(min=9.50, max=11)},
            sort="best_average_rating",
        )

        assert wines == expected

    def _insert_wines(self):
        self.session.execute(
            text(
                "INSERT INTO wines (name, type, winery, appellation, vintage, ratings, average_rating, price) VALUES "  # noqa
                "('Château YYY 2021', 'rosé', 'Château YYY', 'Côte de Provence', 2021, :ratings_1, 90, 9.90),"  # noqa
                "('Château XXX 2020', 'rouge', 'Château XXX', 'Haut-Médoc', 2020, :ratings_2, 91, 11.90),"  # noqa
                "('Château ZZZ 2022', 'blanc', 'Château ZZZ', 'Entre-deux-mers', 2022, :ratings_3, 92, 10.50)"  # noqa
            ),
            {
                "ratings_1": "{89, 91}",
                "ratings_2": "{90, 91, 92}",
                "ratings_3": "{94, 90, 92}",
            },
        )
