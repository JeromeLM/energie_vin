from unittest import TestCase

from domain.price_range import PriceRange


class TestPriceRange(TestCase):
    """
    Feature : know whether a price is included in price range
    """

    def test_is_price_within_with_no_price_range_returns_true(
        self,
    ):
        price_range = PriceRange()
        actual = price_range.is_price_within(price=10.90)
        assert actual is True

    def test_is_price_within_with_only_min_price_and_price_is_cheaper_returns_false(
        self,
    ):
        price_range = PriceRange(min=11.0)
        actual = price_range.is_price_within(price=10.90)
        assert actual is False

    def test_is_price_within_with_only_min_price_and_price_is_more_expensive_returns_true(  # noqa
        self,
    ):
        price_range = PriceRange(min=10.0)
        actual = price_range.is_price_within(price=10.90)
        assert actual is True

    def test_is_price_within_with_only_min_price_and_price_is_min_price_returns_true(  # noqa
        self,
    ):
        price_range = PriceRange(min=10.90)
        actual = price_range.is_price_within(price=10.90)
        assert actual is True

    def test_is_price_within_with_only_max_price_and_price_is_more_expensive_returns_false(  # noqa
        self,
    ):
        price_range = PriceRange(max=10.0)
        actual = price_range.is_price_within(price=10.90)
        assert actual is False

    def test_is_price_within_with_only_max_price_and_price_is_cheaper_returns_true(
        self,
    ):
        price_range = PriceRange(max=11.0)
        actual = price_range.is_price_within(price=10.90)
        assert actual is True

    def test_is_price_within_with_only_max_price_and_price_is_max_price_returns_true(
        self,
    ):
        price_range = PriceRange(max=10.90)
        actual = price_range.is_price_within(price=10.90)
        assert actual is True

    def test_is_price_within_with_min_and_max_price_and_price_is_not_within_returns_false(  # noqa
        self,
    ):
        price_range = PriceRange(min=10.0, max=10.90)
        actual = price_range.is_price_within(price=11.0)
        assert actual is False

    def test_is_price_within_with_min_and_max_price_and_price_is_within_returns_true(
        self,
    ):
        price_range = PriceRange(min=10.0, max=11.0)
        actual = price_range.is_price_within(price=10.90)
        assert actual is True

    def test_is_price_within_with_min_and_max_price_and_price_is_min_price_returns_true(
        self,
    ):
        price_range = PriceRange(min=10.0, max=11.0)
        actual = price_range.is_price_within(price=10.0)
        assert actual is True

    def test_is_price_within_with_min_and_max_price_and_price_is_max_price_returns_true(
        self,
    ):
        price_range = PriceRange(min=10.0, max=11.0)
        actual = price_range.is_price_within(price=11.0)
        assert actual is True
