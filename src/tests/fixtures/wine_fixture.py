from typing import List, Dict

from src.application.use_cases.view_wines_use_case import (
    ViewWinesUseCase,
    ViewWinesCommand,
)
from src.domain.price_range import PriceRange
from src.domain.wine import Wine
from src.tests.adapters.in_memory_wine_repository import InMemoryWineRepository


class WineFixture:
    def __init__(self):
        self.wine_repository = InMemoryWineRepository()
        self.viewed_wines = []

    # GIVEN
    # =====
    def given_following_wines_exist(self, wines: List[Wine]):
        self.wine_repository.given_existing_wines(wines)

    # WHEN
    # ====
    def when_user_wants_to_view_all_the_wines(self):
        view_wines_command = ViewWinesCommand()
        self._handle_use_case(view_wines_command)

    def when_user_wants_to_view_all_the_wines_sorted_by_best_average_rating(self):
        view_wines_command = ViewWinesCommand(sort_by_best_average_rating=True)
        self._handle_use_case(view_wines_command)

    def when_user_wants_to_view_all_the_wines_with_a_price_included_in_this_price_range(
        self, price_range: PriceRange
    ):
        view_wines_command = ViewWinesCommand(price_range=price_range)
        self._handle_use_case(view_wines_command)

    def when_user_wants_to_view_all_the_wines_with_a_price_included_in_this_price_range_and_sorted_by_best_average_rating(  # noqa
        self, price_range: PriceRange
    ):
        view_wines_command = ViewWinesCommand(
            price_range=price_range, sort_by_best_average_rating=True
        )
        self._handle_use_case(view_wines_command)

    def _handle_use_case(self, view_wines_command: ViewWinesCommand):
        view_wines_use_case = ViewWinesUseCase(wine_repository=self.wine_repository)
        self.viewed_wines = view_wines_use_case.handle(view_wines_command)

    # THEN
    # ====
    def then_displayed_wines_should_be(self, expected_wines: List[Dict]):
        assert self.viewed_wines == expected_wines

    # OTHERS
    # ======

    def clean_repository(self):
        self.wine_repository.clean_wines()
