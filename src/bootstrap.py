import os

from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

from src.config import get_postgres_url
from src.infrastructure.sqlalchemy.schema import mapper_registry, start_mappers

# TODO jlm: this file is really really dirty...

if not os.environ.get("EXEC_PROFILE") == "test":

    def _insert_wines(session):
        session.execute(
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

    db_url = get_postgres_url()
    engine = create_engine(db_url)
    mapper_registry.metadata.create_all(engine)
    start_mappers()
    Session = sessionmaker(bind=engine)
    session = Session()
    _insert_wines(session)
else:
    session = None
