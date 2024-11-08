"""UT of error handling."""

import os

import pytest
from arta import RulesEngine
from arta.exceptions import ConditionExecutionError, RuleExecutionError

import pydantic


@pytest.mark.parametrize(
    "rules_dict, config_dir, expected_error",
    [
        (
            None,
            None,
            ValueError,
        ),
        (
            {
                "type": {
                    "rule_str": {
                        "extra_condition": lambda x: isinstance(x, str),
                        "condition": lambda x: isinstance(x, str),
                        "condition_parameters": {"x": "input.to_check"},
                        "action": lambda value, **kwargs: {"value": value},
                        "action_parameters": {"value": "String"},
                    },
                }
            },
            None,
            pydantic.ValidationError,
        ),
        (
            "Something, doesn't matter",
            "Something, doesn't matter",
            ValueError,
        ),
        (
            "Not a dict",
            None,
            pydantic.ValidationError,
        ),
        (
            {},
            None,
            KeyError,
        ),
        (
            {
                "test": {
                    "rule_str": {
                        "condition": lambda x: isinstance(x, str),
                        "condition_parameters": {"x": "input.to_check"},
                        "action": lambda value: {"value": value},
                        "action_parameters": {"value": "Rules not only dict."},
                    },
                },
                "test2": "not good",
            },
            None,
            pydantic.ValidationError,
        ),
        (
            {
                "type": {
                    "rule_str": {
                        "condition": "need to be a callable",
                        "condition_parameters": {"x": "input.to_check"},
                        "action": lambda value: {"value": value},
                        "action_parameters": {"value": "Condition not None or Callable."},
                    },
                }
            },
            None,
            pydantic.ValidationError,
        ),
        (
            {
                "type": {
                    "rule_str": {
                        "action": "need to be a callable",
                    },
                }
            },
            None,
            pydantic.ValidationError,
        ),
        (
            {
                "type": {
                    "rule_str": {
                        "condition": lambda x: isinstance(x, str),
                        "condition_parameters": {"x": "input.to_check"},
                        "action": lambda value: {"value": value},
                        "action_parameters": {"value": "Missing **kwargs in action function."},
                    },
                }
            },
            None,
            KeyError,
        ),
        (
            {
                "type": {
                    "rule_str": {
                        "condition": lambda x: isinstance(x, str),
                        "condition_parameters": {"x": "input.to_check"},
                        "action_parameters": {"value": "Missing an action."},
                    },
                }
            },
            None,
            pydantic.ValidationError,
        ),
        (
            None,
            "failing_conf/missing_action_source_modules/",
            pydantic.ValidationError,
        ),
        (
            None,
            "failing_conf/missing_rules/",
            ValueError,
        ),
        (
            None,
            "failing_conf/wrong_condition/",
            KeyError,
        ),
        (
            None,
            "failing_conf/wrong_action/",
            KeyError,
        ),
        (
            None,
            "failing_conf/wrong_validation_function/",
            KeyError,
        ),
        (
            None,
            "failing_conf/wrong_rules_nested/",
            pydantic.ValidationError,
        ),
        (
            None,
            "failing_conf/wrong_parsing_error_strategy/",
            pydantic.ValidationError,
        ),
    ],
)
def test_instance_error(rules_dict, config_dir, expected_error, base_config_path):
    """Unit test of class instanciation and rules_dict loading."""
    config_path = None

    if config_dir is not None:
        config_path = os.path.join(base_config_path, config_dir)

    with pytest.raises(expected_error):
        _ = RulesEngine(rules_dict=rules_dict, config_path=config_path)


@pytest.mark.parametrize(
    "rules_dict, config_dir",
    [
        (
            {
                "type": {
                    "rule_str": {
                        "condition": lambda x: isinstance(x, str),
                        "condition_parameters": {"x": "input.to_check"},
                        "action": lambda value, **kwargs: value,
                        "action_parameters": {"value": "String"},
                    },
                }
            },
            None,
        ),
        (
            None,
            "failing_conf/without_parsing_error_strategy/",
        ),
    ],
)
def test_instance_error_without_expected_error(rules_dict, config_dir, base_config_path):
    """Unit test of class instanciation and rules_dict loading."""
    config_path = None

    if config_dir is not None:
        config_path = os.path.join(base_config_path, config_dir)

    engine = RulesEngine(rules_dict=rules_dict, config_path=config_path)
    assert isinstance(engine, RulesEngine)


@pytest.mark.parametrize(
    "input_data, expected_error",
    [
        (
            "Something, doesn't matter type",
            TypeError,
        ),
        (
            None,
            TypeError,
        ),
        (
            {},
            KeyError,
        ),
        (
            # Be carefull with the following case, not having condition param. or action param. in input_data
            # can be ok or not.It depends on the condition and action implementations.
            {
                "age": 5000,
                "powers": ["strength", "greek_gods", "regeneration", "immortality"],
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
            },
            ConditionExecutionError,
        ),
        (
            # Be carefull with the following case, not having condition param. or action param. in input_data
            # can be ok or not.It depends on the condition and action implementations.
            {
                "age": 5000,
                "language": "english",
                "powers": ["strength", "greek_gods", "regeneration", "immortality"],
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
            },
            RuleExecutionError,
        ),
    ],
)
def test_error_apply_rules_missing_input_key(input_data, expected_error, base_config_path):
    """Unit test of RulesEngine.apply_process with config_path instance."""
    eng = RulesEngine(config_path=os.path.join(base_config_path, "good_conf"))
    with pytest.raises(expected_error):
        _ = eng.apply_rules(input_data=input_data, rule_set="default_rule_set", verbose=False)
