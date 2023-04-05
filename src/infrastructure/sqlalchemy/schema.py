from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import registry


from domain.wine import Wine

mapper_registry = registry()

wine_table = Table(
    "wines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("type", String(10), nullable=False),
    Column("winery", String(255), nullable=False),
    Column("appellation", String(255), nullable=False),
    Column("vintage", Integer, nullable=False),
    Column("ratings", ARRAY(Integer), nullable=False),
    Column("average_rating", Integer, nullable=False),
    Column("price", Float, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(Wine, wine_table, column_prefix="_")
