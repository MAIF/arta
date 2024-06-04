"""Module containing a custom class (example).

Custom classes are
"""

from __future__ import annotations

from typing import Any

from arta.condition import BaseCondition
from arta.utils import ParsingErrorStrategy


class CustomCondition(BaseCondition):
    """
    This class is not included in maif-rules-engine, it's a user developed class and its goal is to extend the original
    package.

    It implements a dummy condition as an example of custom condition.

    A condition class must inherit from BaseCondition.
    """

    def verify(self, input_data: dict[str, Any], parsing_error_strategy: ParsingErrorStrategy, **kwargs: Any) -> bool:
        """
        Return True if the condition is verified.

        Args:
            input_data: Request or input data to apply rules on.
            parsing_error_strategy: Error handling strategy for parameter parsing.
            **kwargs: For user extra arguments.

        Returns:
            True if the condition is verified, otherwise False.
        """

        if len(kwargs) == 0:
            # Dummy condition check: check presence of the condition id as a key in input data
            return self._condition_id in input_data
        else:
            # Only here for testing kwargs propagation
            return True
