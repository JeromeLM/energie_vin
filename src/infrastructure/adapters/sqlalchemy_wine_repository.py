from typing import Dict, List, Union

from sqlalchemy import text, desc
from sqlalchemy.orm import Session, Query

from src.application.ports.wine_repository import IWineRepository
from src.domain.wine import Wine


class SqlAlchemyWineRepository(IWineRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, wine: Wine):
        self.session.add(wine)
        #  TODO jlm: must be done here or is this the responsibility of the caller ?
        self.session.commit()

    def list(self, filters: Dict = None, sort: str = None) -> List[Wine]:
        query = self._build_list_query(filters, sort)
        return query.all()

    def _build_list_query(
        self, filters: Union[Dict, None], sort: Union[str, None]
    ) -> Query:
        query = self.session.query(Wine)
        query = self._add_list_query_filters(query, filters)
        query = self._add_list_query_sort(query, sort)
        return query

    def _add_list_query_filters(
        self, query: Query, filters: Union[Dict, None]
    ) -> Query:
        if not self._has_price_range_filter(filters):
            return query

        query_filters = []
        min_price = filters["price_range"].min
        max_price = filters["price_range"].max
        query_filters.append(f"price >= {min_price}")
        if max_price is not None:
            query_filters.append(f"price <= {max_price}")
        for query_filter in query_filters:
            query = query.filter(text(query_filter))
        return query

    def _has_price_range_filter(self, filters: Union[Dict, None]) -> bool:
        return filters is not None and "price_range" in filters

    def _add_list_query_sort(self, query: Query, sort: Union[str, None]) -> Query:
        if self._has_best_average_rating_sort(sort):
            return query.order_by(desc(text("wines.average_rating")))
        return query

    def _has_best_average_rating_sort(self, sort: Union[str, None]) -> bool:
        return sort is not None and sort == "best_average_rating"
