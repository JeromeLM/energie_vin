from sqlalchemy import text

from src.domain.wine import Wine
from src.tests.builders.wine_builder import WineBuilder


def test_mapper_can_load_wines(session):
    session.execute(
        text(
            "INSERT INTO wines (name, type, winery, appellation, vintage, ratings, average_rating, price) VALUES "  # noqa
            "('Château XXX 2020', 'rouge', 'Château XXX', 'Haut-Médoc', 2020, :ratings_1, 91, 11.90),"  # noqa
            "('Château YYY 2021', 'rosé', 'Château YYY', 'Côte de Provence', 2021, :ratings_2, 90, 9.90)"  # noqa
        ),
        {"ratings_1": "{90, 91, 92}", "ratings_2": "{89, 91}"},
    )
    expected = [
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
    assert session.query(Wine).all() == expected


def test_mapper_can_save_wines(session):
    new_wine = (
        WineBuilder()
        .with_name("Château ZZZ 2022")
        .of_type("blanc")
        .from_winery("Château ZZZ")
        .of_appelation("Entre-deux-mers")
        .of_vintage(2022)
        .rated([91, 89, 90])
        .costing(8.50)
        .build()
    )
    session.add(new_wine)
    session.commit()

    rows = list(
        session.execute(
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
            [91, 89, 90],
            8.50,
        )
    ]
