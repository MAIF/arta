"""RulesEngine class UT."""

import pytest
from arta import RulesEngine


def test_instanciation(base_config_path):
    """Unit test of the class RulesEngine"""
    # Dummy action function
    set_value = lambda value, **kwargs: {"value": value}

    raw_rules = {
        "type": {
            "rule_str": {
                "condition": lambda x: isinstance(x, str),
                "condition_parameters": {"x": "input.to_check"},
                "action": set_value,
                "action_parameters": {"value": "String"},
            },
            "rule_other": {
                "condition": None,
                "condition_parameters": None,
                "action": set_value,
                "action_parameters": {"value": "other type"},
            },
        }
    }
    # Dictionary instanciation
    eng = RulesEngine(rules_dict=raw_rules)
    assert isinstance(eng, RulesEngine)


@pytest.mark.parametrize(
    "input_data, verbose, good_results",
    [
        (
            {
                "age": 5000,
                "language": "english",
                "power": "immortality",
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
            },
            True,
            {
                "verbosity": {
                    "rule_set": "default_rule_set",
                    "results": [
                        {
                            "rule_group": "power_level",
                            "verified_conditions": {
                                "condition": {"expression": "USER_CONDITION", "values": {"USER_CONDITION": True}}
                            },
                            "activated_rule": "super_power",
                            "action_result": "super",
                        },
                        {
                            "rule_group": "admission",
                            "verified_conditions": {
                                "condition": {"expression": "USER_CONDITION", "values": {"USER_CONDITION": True}}
                            },
                            "activated_rule": "admitted",
                            "action_result": "Admitted!",
                        },
                    ],
                },
                "power_level": "super",
                "admission": "Admitted!",
            },
        ),
        (
            {
                "age": 5000,
                "language": "english",
                "power": "immortality",
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
            },
            False,
            {"power_level": "super", "admission": "Admitted!"},
        ),
    ],
)
def test_dict_apply_rules(input_data, verbose, good_results):
    """Unit test of the method RulesEngine.apply_rules() when init was done using rule_dict"""
    # Dummy action function

    def is_a_super_power(level, **kwargs):
        """Dummy validation function."""
        return level == "super"

    def admit(**kwargs):
        """Dummy action function."""
        return "Admitted!"

    def set_value(value, **kwargs):
        """Dummy action function."""
        return value

    rules_raw = {
        "power_level": {
            "super_power": {
                "condition": lambda p: p in ["immortality", "time_travelling", "invisibility"],
                "condition_parameters": {"p": "input.power"},
                "action": lambda x: x,
                "action_parameters": {"x": "super"},
            },
            "minor_power": {
                "condition": lambda p: p in ["juggle", "sing", "sleep"],
                "condition_parameters": {"p": "input.power"},
                "action": lambda x, **kwargs: x,
                "action_parameters": {"x": "minor"},
            },
            "no_power": {
                "condition": None,
                "condition_parameters": None,
                "action": lambda x, **kwargs: x,
                "action_parameters": {"x": "no_power"},
            },
        },
        "admission": {
            "admitted": {
                "condition": is_a_super_power,
                "condition_parameters": {"level": "output.power_level"},
                "action": admit,
                "action_parameters": None,
            },
            "not_admitted": {
                "condition": None,
                "condition_parameters": None,
                "action": set_value,
                "action_parameters": {"value": "Not admitted :-("},
            },
        },
    }

    eng_2 = RulesEngine(rules_dict=rules_raw)
    res = eng_2.apply_rules(input_data, verbose=verbose)
    assert res == good_results


def test_ignored_rules():
    """Unit test of the method RulesEngine.apply_rules() when there are rules to ignore"""
    rules_raw = {
        "power_level": {
            "ignored_1": {
                "condition": None,
                "condition_parameters": None,
                "action": lambda x, **kwargs: x,
                "action_parameters": {"x": "ignored_1"},
            },
            "ignored_2": {
                "condition": lambda p: p in ["juggle", "sing", "sleep"],
                "condition_parameters": {"p": "input.power"},
                "action": lambda x, **kwargs: x,
                "action_parameters": {"x": "ignored_2"},
            },
            "no_power": {
                "condition": None,
                "condition_parameters": None,
                "action": lambda x, **kwargs: x,
                "action_parameters": {"x": "no_power"},
            },
        },
    }

    input_data = {
        "age": 5000,
        "language": "english",
        "power": "juggle",
        "favorite_meal": None,
        "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
    }

    expected_results = {"power_level": "no_power"}

    eng_2 = RulesEngine(rules_dict=rules_raw)
    res = eng_2.apply_rules(input_data, ignored_rules={"ignored_1", "ignored_2"}, verbose=False)

    assert res == expected_results
