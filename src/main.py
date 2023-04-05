import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text

from src.application.ports.wine_repository import IWineRepository
from src.application.use_cases.view_wines_use_case import (
    ViewWinesCommand,
    ViewWinesUseCase,
)
from src.domain.price_range import PriceRange
from src.infrastructure.adapters.sqlalchemy_wine_repository import (
    SqlAlchemyWineRepository,
)
from src.infrastructure.session_factory import SessionFactory

app = FastAPI()


session = SessionFactory.build(exec_profile="local")


def get_repository():
    return SqlAlchemyWineRepository(session)


@app.get("/wines")
def list(
    sort: str = None,
    min_price: float = 0.0,
    max_price: float = None,
    wine_repository: IWineRepository = Depends(get_repository),
):
    try:
        price_range = PriceRange(min=min_price, max=max_price)
        if sort is not None and sort == "best_average_rating":
            view_wines_command = ViewWinesCommand(
                sort_by_best_average_rating=True, price_range=price_range
            )
        else:
            view_wines_command = ViewWinesCommand(price_range=price_range)
        view_wines_use_case = ViewWinesUseCase(wine_repository=wine_repository)
        wines = view_wines_use_case.handle(view_wines_command)
        return wines
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal error")


def init_bdd(session):
    session.execute(text("TRUNCATE TABLE wines"))
    session.commit()
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


if __name__ == "__main__":
    # Temporary hack : insert some data in db
    init_bdd(session)

    uvicorn.run(app, host="0.0.0.0", port=5005)
