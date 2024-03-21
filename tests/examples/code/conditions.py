"""This module contains the validation function implementations
of the conditions in conditions.yaml.

N.B: They are only demo functions.
"""

from typing import List, Optional


def has_authorized_super_power(authorized_powers: List[str], candidate_powers: List[str]) -> bool:
    """Check candidate's powers and return True if OK."""
    auth_powers = [power for power in authorized_powers if candidate_powers is not None and power in candidate_powers]
    return len(auth_powers) > 0


def is_age_unknown(age: Optional[int]) -> bool:
    """Check if age is unknown = return True if age is None."""
    return age is None


def is_speaking_language(value: str, spoken_language: str) -> bool:
    """Check if the candidate spoken language is the same as value."""
    return value == spoken_language


def has_favorite_meal(favorite_meal: str) -> bool:
    """Check if candidate has a favorite meal."""
    return favorite_meal is not None
