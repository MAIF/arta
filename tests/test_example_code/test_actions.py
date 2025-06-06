"""Action function unit tests."""

import pytest

from tests.examples.code import actions


@pytest.mark.parametrize(
    "value, expected",
    [
        (True, {"admission": True}),
        (False, {"admission": False}),
    ],
)
def test_set_admission(value, expected):
    """Action function unit test."""
    result = actions.set_admission(value)
    assert result == expected


@pytest.mark.parametrize(
    "course_id, expected",
    [
        ("french", {"course_id": "french"}),
        ("international", {"course_id": "international"}),
    ],
)
def test_set_student_course(course_id, expected):
    """Action function unit test."""
    result = actions.set_student_course(course_id)
    assert result == expected


@pytest.mark.parametrize(
    "mail_to, mail_content, meal, expected",
    [
        (
            "cook@test.fr",
            "Thanks for preparing the following meal: ",
            "roast beef",
            True,
        ),
        ("supercook@dummy.fr", "Thanks for preparing the following meal: ", "pancakes", True),
    ],
)
def test_send_email(mail_to, mail_content, meal, expected):
    """Action function unit test."""
    result = actions.send_email(mail_to, mail_content, meal)
    assert result == expected


def test_concatenate_list():
    """Action function unit test."""
    result = actions.concatenate_list(["a", "b", "c"], {})
    assert result == "abc"


def test_do_nothing():
    """Action function unit test."""
    result = actions.do_nothing()
    assert result is None


def test_compute_sum():
    """Action function unit test."""
    result = actions.compute_sum(2, 3)
    assert result == 5


def test_concatenate():
    """Action function unit test."""
    result = actions.concatenate("a", "b")
    assert result == "ab"
