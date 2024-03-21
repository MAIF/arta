"""Utility functions UT."""

import pytest
from arta.utils import ParsingErrorStrategy, parse_dynamic_parameter


@pytest.mark.parametrize(
    "parameter, input_data, expected_value",
    [
        (
            "output.age",
            dict(output=dict(age=20, first_name="Joe")),
            20,
        ),
        (
            "output.sub_dict1.sub_dict2.key",
            dict(output=dict(sub_dict1=dict(sub_dict2=dict(key="abc")))),
            "abc",
        ),
        (
            ["output.foo", 32, "output.bar"],
            dict(output=dict(foo="foofoo", bar="barbar")),
            ["foofoo", 32, "barbar"],
        ),
    ],
)
def test_parse_dynamic_parameter(parameter, input_data, expected_value):
    """Utils function unit test."""
    result = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.RAISE)
    assert result == expected_value


def test_raise_error_handling_strategy():
    """Utils function unit test."""
    parameter = "output.unknown.path"
    input_data = dict(output=dict(age=20, first_name="Joe"))
    error_regex_match = "output.unknown.path"

    with pytest.raises(KeyError, match=error_regex_match):
        _ = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.RAISE)


def test_raise_error_handling_strategy_as_string():
    """Utils function unit test."""
    parameter = "output.unknown.path"
    input_data = dict(output=dict(age=20, first_name="Joe"))
    error_regex_match = "output.unknown.path"

    with pytest.raises(KeyError, match=error_regex_match):
        _ = parse_dynamic_parameter(
            parameter,
            input_data,
            parsing_error_strategy=ParsingErrorStrategy.RAISE,
        )


def test_raise_error_handling_strategy_override():
    """Utils function unit test."""
    # Arrange
    parameter = "output.unknown.path?"
    input_data = dict(output=dict(age=20, first_name="Joe"))
    expected_value = None

    # Act
    result = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.RAISE)

    # Assert
    assert result == expected_value


@pytest.mark.parametrize("parameter", ["output.age?", "output.age!"])
def test_raise_error_handling_strategy_override_on_existing_key(parameter):
    """Utils function unit test."""
    # Arrange
    parameter = "output.age?"
    input_data = dict(output=dict(age=20, first_name="Joe"))
    expected_value = 20

    # Act
    result = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.RAISE)

    # Assert
    assert result == expected_value


def test_ignore_error_handling_strategy():
    """Utils function unit test."""
    # Arrange
    parameter = "output.unknown.path"
    input_data = dict(output=dict(age=20, first_name="Joe"))
    expected_value = None

    # Act
    result = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.IGNORE)

    # Assert
    assert result == expected_value


def test_ignore_error_handling_strategy_as_string():
    """Utils function unit test."""
    # Arrange
    parameter = "output.unknown.path"
    input_data = dict(output=dict(age=20, first_name="Joe"))
    expected_value = None

    # Act
    result = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.IGNORE)

    # Assert
    assert result == expected_value


def test_ignore_error_handling_strategy_override():
    """Utils function unit test."""
    # Arrange
    parameter = "output.unknown.path!"
    input_data = dict(output=dict(age=20, first_name="Joe"))
    error_regex_match = "output.unknown.path"

    with pytest.raises(KeyError, match=error_regex_match):
        _ = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.RAISE)


@pytest.mark.parametrize(
    "parameter, expected_value",
    [
        ("output.unknown?None", "None"),
        ("output.unknown?True", "True"),
        ("output.unknown?hello", "hello"),
    ],
)
def test_raise_error_handling_strategy_with_default_value_override(parameter, expected_value):
    """Utils function unit test."""
    input_data = dict(output=dict(age=20, first_name="Joe"))

    # Act
    result = parse_dynamic_parameter(parameter, input_data, parsing_error_strategy=ParsingErrorStrategy.RAISE)

    # Assert
    assert result == expected_value
