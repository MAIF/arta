"""This module holds the action function implementations used for
triggering an action (set in rules.yaml).

N.B: They are only demo functions.
"""

from __future__ import annotations

from typing import Any


def set_admission(value: bool) -> dict[str, bool]:
    """Return a dictionary containing the admission result."""
    return {"admission": value}


def set_student_course(course_id: str, **kwargs: Any) -> dict[str, str]:
    """Return the course id as a dictionary."""
    return {"course_id": course_id}


def send_email(mail_to: str, mail_content: str, meal: str) -> bool:
    """Send an email and return True if OK."""
    is_ok = False

    # API call mock
    if meal is not None:
        is_ok = True

    return is_ok


def concatenate_list(list_str: list[Any], input_data: dict[str, Any]) -> str:
    """Demo function: return the concatenation of a list of string using input_data (two levels max)."""
    list_str = [str(element) for element in list_str]
    return "".join(list_str)


def do_nothing(**kwargs: Any) -> None:
    """Demo function: do nothing = return None."""
    pass


def compute_sum(value1: float, value2: float, **extra: Any) -> float:
    """Demo function: return sum of two values."""
    return value1 + value2


def concatenate(value1: str, value2: str) -> str:
    """Demo function: return the concatenation of two strings."""
    return value1 + value2


def alert_on_median(**kwargs: Any) -> str:
    """Alert: "Median is too high: 13, limit is: 10."""
    return f"Median is too high: {kwargs['input_data']['median']}, limit is: {kwargs['input_data']['median_limit']}."


def set_admission_custom(value: bool, **kwargs: Any) -> dict[str, bool]:
    """Return a dictionary containing the admission result and use a user defined argument."""
    # Pseudo edge case
    value = value if kwargs["my_parameter"] is True else False

    return {"admission": value}
