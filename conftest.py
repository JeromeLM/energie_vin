import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.infrastructure.sqlalchemy.schema import mapper_registry, start_mappers


@pytest.fixture
def in_memory_db():
    db_url = "postgresql://postgres:root@localhost:5435/energie_vin"
    engine = create_engine(db_url)
    mapper_registry.metadata.create_all(engine)
    yield engine
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    Session = sessionmaker(bind=in_memory_db)
    session = Session()
    yield session
    session.close()
    clear_mappers()
