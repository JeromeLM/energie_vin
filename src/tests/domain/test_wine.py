from unittest import TestCase

from tests.builders.wine_builder import WineBuilder


class TestWine(TestCase):

    """
    Feature : get average rating
    """

    def test_get_average_rating_with_no_rating_returns_no_average_rating(self):
        wine = WineBuilder().rated([]).build()
        actual = wine._get_average_rating()
        assert actual is None

    def test_get_average_rating_with_1_rating_returns_this_1_rating(self):
        wine = WineBuilder().rated([90]).build()
        actual = wine._get_average_rating()
        assert actual == 90

    def test_get_average_rating_with_several_ratings_returns_average_rating(self):
        wine = WineBuilder().rated([90, 91, 92, 93, 89]).build()
        actual = wine._get_average_rating()
        assert actual == 91

    def test_get_average_rating_with_several_ratings_returns_average_rating_rounded_to_the_higher_integer(  # noqa
        self,
    ):
        wine = WineBuilder().rated([90, 92, 93]).build()
        actual = wine._get_average_rating()
        # 91.6666666 => 92
        assert actual == 92

    def test_get_average_rating_with_several_ratings_returns_average_rating_rounded_to_the_lower_integer(  # noqa
        self,
    ):
        wine = WineBuilder().rated([90, 91, 90]).build()
        actual = wine._get_average_rating()
        # 90.333333 => 90
        assert actual == 90

    # TODO jlm: test name is really much too long !!
    def test_get_average_rating_with_several_ratings_returns_average_rating_rounded_to_the_higher_integer_if_as_close_to_the_upper_integer_as_to_the_lower_integer(  # noqa
        self,
    ):
        wine = WineBuilder().rated([90, 91]).build()
        actual = wine._get_average_rating()
        # 90.5 => 91
        assert actual == 91
