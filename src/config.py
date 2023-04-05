import os


def get_postgres_url():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5435 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "root")
    user, db_name = "postgres", "energie_vin"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_test_url():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5435 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "root")
    user, db_name = "postgres", "energie_vin_test"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
