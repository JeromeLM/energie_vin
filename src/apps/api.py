from fastapi import FastAPI, HTTPException, Depends

from src.application.ports.wine_repository import IWineRepository
from src.application.use_cases.view_wines_use_case import (
    ViewWinesCommand,
    ViewWinesUseCase,
)
from src.bootstrap import session
from src.domain.price_range import PriceRange
from src.infrastructure.adapters.sqlalchemy_wine_repository import (
    SqlAlchemyWineRepository,
)


app = FastAPI()


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
