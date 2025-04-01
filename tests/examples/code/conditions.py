"""This module contains the validation function implementations
of the conditions in conditions.yaml.

N.B: They are only demo functions.
"""

from __future__ import annotations
import statistics
from typing import Any


def has_authorized_super_power(authorized_powers: list[str], candidate_powers: list[str]) -> bool:
    """Check candidate's powers and return True if OK."""
    auth_powers = [power for power in authorized_powers if candidate_powers is not None and power in candidate_powers]
    return len(auth_powers) > 0


def is_age_unknown(age: int | None) -> bool:
    """Check if age is unknown = return True if age is None."""
    return age is None


def is_speaking_language(value: str, spoken_language: str) -> bool:
    """Check if the candidate spoken language is the same as value."""
    return value == spoken_language


def has_favorite_meal(favorite_meal: str, **extra: Any) -> bool:
    """Check if candidate has a favorite meal."""
    return favorite_meal is not None


def is_median_above(values: list[int | float], limit: float, **kwargs: Any) -> bool:
    """Check if the median of some values is above limit."""
    median = statistics.median(values)
    # Store the value for later use by an action function
    kwargs["input_data"]["median"] = median
    kwargs["input_data"]["median_limit"] = limit
    return median > limit
