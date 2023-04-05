import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.config import get_postgres_url
from src.infrastructure.sqlalchemy.schema import mapper_registry, start_mappers


@pytest.fixture
def postgres_db():
    db_url = get_postgres_url()
    engine = create_engine(db_url)
    mapper_registry.metadata.create_all(engine)
    yield engine
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def session(postgres_db):
    start_mappers()
    Session = sessionmaker(bind=postgres_db)
    session = Session()
    yield session
    session.close()
    clear_mappers()
