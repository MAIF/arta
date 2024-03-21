"""
Unit tests of the conditions.py module.
"""

import pytest

from tests.examples.code import conditions


@pytest.mark.parametrize(
    "function, kwargs, expected",
    [
        (
            conditions.has_authorized_super_power,
            {"authorized_powers": ["strength", "fly", "immortality"], "candidate_powers": ["invisibility", "fly"]},
            True,
        ),
        (
            conditions.has_authorized_super_power,
            {"authorized_powers": ["strength", "fly", "immortality"], "candidate_powers": ["invisibility", "fast"]},
            False,
        ),
        (conditions.is_age_unknown, {"age": None}, True),
        (conditions.is_age_unknown, {"age": 100}, False),
        (conditions.is_speaking_language, {"value": "english", "spoken_language": "english"}, True),
        (conditions.is_speaking_language, {"value": "french", "spoken_language": "english"}, False),
        (conditions.has_favorite_meal, {"favorite_meal": "gratin"}, True),
        (conditions.has_favorite_meal, {"favorite_meal": None}, False),
    ],
)
def test_functions(function, kwargs, expected):
    """Validation funtion unit test."""
    assert function(**kwargs) == expected
