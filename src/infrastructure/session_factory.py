from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import get_postgres_test_url, get_postgres_url
from src.infrastructure.sqlalchemy.schema import mapper_registry, start_mappers


# This class allows to build a session depending on the context (test or real purpose)
# while reusing a session previously created if any (avoiding test failures if session
# already active).
# Mappers must also be started only once.
class SessionFactory:
    mappers_already_started = False
    real_session = None
    test_session = None

    @classmethod
    def build(cls, exec_profile: str) -> Session:
        if exec_profile == "local":
            if not cls.real_session is None:
                return cls.real_session
            db_url = get_postgres_url()
            cls.real_session = cls._build_session(db_url)
            return cls.real_session

        if exec_profile == "test":
            if not cls.test_session is None:
                return cls.test_session
            db_url = get_postgres_test_url()
            cls.test_session = cls._build_session(db_url)
            return cls.test_session

        raise RuntimeError(f"Unsupported exec_profile {exec_profile}")

    @classmethod
    def _build_session(cls, db_url: str) -> Session:
        engine = create_engine(db_url)
        mapper_registry.metadata.create_all(engine)
        if cls.mappers_already_started is False:
            start_mappers()
            cls.mappers_already_started = True
        session_maker = sessionmaker(bind=engine)
        return session_maker()
