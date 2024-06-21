"""Utility module."""

from __future__ import annotations

import copy
import re
from enum import Enum
from typing import Any

# Global constants
UPPERCASE_WORD_PATTERN: str = r"\b[A-Z_0-9]+\b"


class ParsingErrorStrategy(str, Enum):
    """Define authorized error handling strategies when a key is missing in the input data."""

    RAISE: str = "raise"
    IGNORE: str = "ignore"
    DEFAULT_VALUE: str = "default_value"


def get_value_in_nested_dict_from_path(path: str, nested_dict: dict[str, Any]) -> Any:
    """From a path, get a value in a nested dict.

    Ex:
        path : this.is.a.path
        result : nested_dict["this"]["is"]["a"]["path"]

    Args:
        path: A dictionary path.
        nested_dict: A nested dictionary.

    Returns:
        Found value.
    """
    keys: list[str] = path.split(".")

    # Initialize value with whole nested dict
    value: dict[str, Any] = nested_dict

    # Loop on path keys
    for key in keys:
        if value is None:
            raise KeyError(f"Key {value} of path {path} not found in input data.")
        value = value[key]

    return value


def parse_dynamic_parameter(
    parameter: Any,
    input_data: dict[str, Any],
    parsing_error_strategy: ParsingErrorStrategy,
) -> Any:
    """Parse the value of parameterized parameters.

    (e.g.1, input.age  -> 20, e.g.2, input.name.first -> "John")

    Args:
        parameter: The parameters configured in conditions.yaml.
        input_data: Request or input data to apply rules on.
        parsing_error_strategy: Strategy to adopt when confronted with a missing key.

    Returns:
        The list of the parameters' values.

    Raises:
        KeyError: Key not found.
    """
    # Copy parameters to not alterate original
    parameter = copy.deepcopy(parameter)

    if isinstance(parameter, list):
        parameter = [parse_dynamic_parameter(element, input_data, parsing_error_strategy) for element in parameter]

    elif isinstance(parameter, str):
        if not parameter.startswith(("input.", "output.")):
            # Keep parameter value unchanged
            return parameter

        # Remove the "input" prefix
        param_path: str = re.sub(r"^input\.", r"", parameter)

        # Check if a parsing error strategy flag is present
        default_value, param_path, parsing_error_strategy = check_parsing_error_strategy_override(
            param_path, parsing_error_strategy
        )

        # Get value from path
        try:
            parameter = get_value_in_nested_dict_from_path(path=param_path, nested_dict=input_data)
        except KeyError as error:
            if parsing_error_strategy is ParsingErrorStrategy.IGNORE:
                return None
            if parsing_error_strategy is ParsingErrorStrategy.DEFAULT_VALUE:
                return default_value
            else:
                raise KeyError(f"Could not find path '{param_path}' in the input data: {str(error)}") from error

    return parameter


def check_parsing_error_strategy_override(
    param_path: str, parsing_error_strategy: ParsingErrorStrategy
) -> tuple[Any, str, ParsingErrorStrategy]:
    """Check if the input parameter contains a flag to override the parsing error strategy.

    The following override syntaxes are accepted:
    - output.favorite_meal!             # raise an exception
    - output.favorite_meal?             # parameter = None
    - output.favorite_meal?default_str  # parameter = default_str (works on str only at first)

    Args:
        param_path: Path to a parameter in a nested dict.
        parsing_error_strategy: Strategy to adopt when a missing key occured.

    Returns:
        default_value: Default value to use if the DEFAULT_VALUE strategy is adopted.
        param_path: Clean path to the input parameter.
        parsing_error_strategy: Strategy adopted to handle parsing errors.
    """
    # Override default error handling strategy
    default_value: Any = None

    last_key: str = param_path.split(".")[-1]

    # Replace missing fields with None
    if last_key.endswith("?"):
        # Set strategy
        parsing_error_strategy = ParsingErrorStrategy.IGNORE
        # Cleanup path
        param_path = param_path.rstrip("?")

    # Raise error on missing fields
    elif last_key.endswith("!"):
        # Set strategy
        parsing_error_strategy = ParsingErrorStrategy.RAISE
        # Cleanup path
        param_path = param_path.rstrip("!")

    # Replace missing fields with default value
    elif "?" in last_key:
        default_value = last_key.split("?")[-1]
        # Set strategy
        parsing_error_strategy = ParsingErrorStrategy.DEFAULT_VALUE
        # Cleanup path
        param_path = "".join(param_path.split("?")[:-1])

    return default_value, param_path, parsing_error_strategy


def sanitize_regex(pattern: str) -> str:
    """Return a sanitized regex string.

    E.g., 'input.power=="fly"' --> 'input\\.power==\\"fly\\"'
           'CONDITION_2'       --> '\\bCONDITION_2\\b'

    Args:
        pattern: A regex pattern string.

    Returns:
        A sanitized regex pattern string.
    """
    if re.search(UPPERCASE_WORD_PATTERN, pattern) is None:
        # Pattern is not like 'CONDITION_2' but like 'input.power=="fly"'
        pattern = (
            pattern.replace('"', r"\"").replace(".", r"\.").replace("+", r"\+").replace("-", r"\-").replace("*", r"\*")
        )
    else:
        pattern = rf"\b{pattern}\b"

    return pattern
