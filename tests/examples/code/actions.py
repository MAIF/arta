"""This module holds the action function implementations used for
triggering an action (set in rules.yaml).

N.B: They are only demo functions.
"""

from __future__ import annotations

from typing import Any


def set_admission(value: bool, **kwargs: Any) -> dict[str, bool]:
    """Return a dictionary containing the admission result."""
    return {"admission": value}


def set_student_course(course_id: str, **kwargs: Any) -> dict[str, str]:
    """Return the course id as a dictionary."""
    return {"course_id": course_id}


def send_email(mail_to: str, mail_content: str, meal: str, **kwargs: Any) -> bool:
    """Send an email and return True if OK."""
    is_ok = False

    # API call mock
    if meal is not None:
        is_ok = True

    return is_ok

def set_family(number: int, **kwargs: Any)->bool:
    """"""
    family :bool =False
    if number>0 :
        family =True 
    return {"family": family}

def concatenate_str(list_str: list[Any], **kwargs: Any) -> str:
    """Demo function: return the concatenation of a list of string using input_data (two levels max)."""
    list_str = [str(element) for element in list_str]
    return "".join(list_str)


def do_nothing(**kwargs: Any) -> None:
    """Demo function: do nothing = return None."""
    pass


def compute_sum(value1: float, value2: float, **kwargs: Any) -> float:
    """Demo function: return sum of two values."""
    return value1 + value2
