"""Condition implementation.

Classes: BaseCondition, StandardCondition, SimpleCondition
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any, Callable

from arta.exceptions import ConditionExecutionError
from arta.utils import UPPERCASE_WORD_PATTERN, ParsingErrorStrategy, parse_dynamic_parameter


class BaseCondition(ABC):
    """Base class of a Condition object (Strategy Pattern).

    Is an abstract class and can't be instantiated.

    Attributes:
        condition_id: Id of a condition.
        description: Description of a condition.
        validation_function: Validation function of a condition.
        validation_function_parameters: Arguments of the validation function.
    """

    # Class constants
    CONDITION_DATA_LABEL: str = "Custom condition data (not needed)"
    CONDITION_ID_PATTERN: str = UPPERCASE_WORD_PATTERN

    def __init__(
        self,
        condition_id: str,
        description: str,
        validation_function: Callable | None = None,
        validation_function_parameters: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize attributes.

        Args:
            condition_id: Id of a condition.
            description: Description of a condition.
            validation_function: Validation function of a condition.
            validation_function_parameters: Arguments of the validation function.
        """
        self._condition_id = condition_id
        self._description = description
        self._validation_function = validation_function
        self._validation_function_parameters = validation_function_parameters

    @classmethod
    def extract_condition_ids_from_expression(cls, condition_expr: str | None = None) -> set[str]:
        """Get the condition ids from a string (e.g., UPPERCASE words).

        E.g., CONDITION_1 and not CONDITION_2

        Warning: implementation is based on the current class constant CONDITION_SPLIT_PATTERN.

        Args:
            condition_expr: A boolean expression (string).

        Returns:
            A set of extracted condition ids.
        """
        cond_ids: set[str] = set()

        if condition_expr is not None:
            cond_ids = set(re.findall(cls.CONDITION_ID_PATTERN, condition_expr))

        return cond_ids

    @abstractmethod
    def verify(self, input_data: dict[str, Any], parsing_error_strategy: ParsingErrorStrategy, **kwargs: Any) -> bool:
        """(Abstract)
        Return True if the condition is verified.

        Args:
            input_data: Input data to apply rules on.
            parsing_error_strategy: Error handling strategy for parameter parsing.
            **kwargs: For user extra arguments.

        Returns:
            True if the condition is verified, otherwise False.
        """
        raise NotImplementedError


class StandardCondition(BaseCondition):
    """Class implementing a built-in condition, named standard condition.

    Attributes:
        condition_id: Id of a condition.
        description: Description of a condition.
        validation_function: Validation function of a condition.
        validation_function_parameters: Arguments of the validation function.
    """

    def verify(self, input_data: dict[str, Any], parsing_error_strategy: ParsingErrorStrategy, **kwargs: Any) -> bool:
        """Return True if the condition is verified.

        Example of a unitary standard condition: CONDITION_1

        Args:
            input_data: Request or input data to apply rules on.
            parsing_error_strategy: Error handling strategy for parameter parsing.
            **kwargs: For user extra arguments.

        Returns:
            True if the condition is verified, otherwise False.

        Raises:
            AttributeError: Check the validation function or its parameters.
        """
        if self._validation_function is None:
            raise AttributeError("Validation function should not be None")

        if self._validation_function_parameters is None:
            raise AttributeError("Validation function parameters should not be None")

        # Parse dynamic parameters
        parameters: dict[str, Any] = {}

        for key, value in self._validation_function_parameters.items():
            parameters[key] = parse_dynamic_parameter(
                parameter=value, input_data=input_data, parsing_error_strategy=parsing_error_strategy
            )

        # Run validation_function
        return self._validation_function(**parameters)


class SimpleCondition(BaseCondition):
    """Class implementing a built-in simple condition.

    Attributes:
        condition_id: Id of a condition.
        description: Description of a condition.
        validation_function: Validation function of a condition.
        validation_function_parameters: Arguments of the validation function.
    """

    # Class constants
    CUSTOM_CONDITION_DATA_LABEL: str = "Simple condition data (not needed)"
    CONDITION_ID_PATTERN: str = r"(?:input\.|output\.)(?:[a-z_0-9!=<>\"NTF\.\*\+\-/]*)(?:[a-z\s]*\"|)"

    def verify(self, input_data: dict[str, Any], parsing_error_strategy: ParsingErrorStrategy, **kwargs: Any) -> bool:
        """Return True if the condition is verified.

        Example of a unitary simple condition to be verified: 'input.age>=100'

        Args:
            input_data: Request or input data to apply rules on.
            parsing_error_strategy: Error handling strategy for parameter parsing.
            **kwargs: For user extra arguments.

        Returns:
            True if the condition is verified, otherwise False.

        Raises:
            AttributeError: Check the validation function or its parameters.
        """
        bool_var: bool = False
        unitary_expr: str = self._condition_id

        data_path_patt: str = r"(?:input\.|output\.)(?:[a-z_\.]*)"

        # Retrieve only the data path
        path_matches: list[str] = re.findall(data_path_patt, unitary_expr)

        if len(path_matches) > 0:
            # Regular case: we have a data paths
            for idx, path in enumerate(path_matches):
                # Read data from the path
                locals()[f"data_{idx}"] = parse_dynamic_parameter(  # noqa
                    parameter=path, input_data=input_data, parsing_error_strategy=parsing_error_strategy
                )

                # Replace with the variable name in the expression
                unitary_expr = unitary_expr.replace(path, f"data_{idx}")

            # Evaluate the expression
            try:
                bool_var = eval(unitary_expr)  # noqa
            except TypeError:
                # Ignore evaluation --> False
                pass

        elif parsing_error_strategy == ParsingErrorStrategy.RAISE:
            # Raise an error because of no match for a data path
            raise ConditionExecutionError(f"Error when verifying simple condition: '{unitary_expr}'")

        else:
            # Other case: ignore, default value => return False
            pass

        return bool_var
