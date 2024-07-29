"""RulesEngine class UT."""

import os

import pytest
from arta import RulesEngine
from arta.config import load_config


def test_instanciation(base_config_path):
    """Unit test of the class RulesEngine"""
    # Config. instanciation
    path = os.path.join(base_config_path, "good_conf")
    eng_1 = RulesEngine(config_path=path)
    assert isinstance(eng_1, RulesEngine)

    config_dict = load_config(path)
    eng_2 = RulesEngine(config_dict=config_dict)
    assert isinstance(eng_2, RulesEngine)

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
    eng_3 = RulesEngine(rules_dict=raw_rules)
    assert isinstance(eng_3, RulesEngine)


@pytest.mark.parametrize(
    "input_data, config_dir, rule_set, verbose, good_results",
    [
        (
            {
                "age": None,
                "language": "french",
                "powers": ["strength", "fly"],
                "favorite_meal": "Spinach",
            },
            "good_conf",
            "default_rule_set",
            False,
            {
                "admission": {"admission": True},
                "course": {"course_id": "senior"},
                "email": True,
            },
        ),
        (
            {
                "age": None,
                "language": "french",
                "powers": ["strength", "fly"],
                "favorite_meal": "Spinach",
            },
            "good_conf",
            "default_rule_set",
            True,
            {
                "verbosity": {
                    "rule_set": "default_rule_set",
                    "results": [
                        {
                            "rule_group": "admission",
                            "verified_conditions": {
                                "condition": {
                                    "expression": "HAS_SCHOOL_AUTHORIZED_POWER",
                                    "values": {"HAS_SCHOOL_AUTHORIZED_POWER": True},
                                },
                                "simple_condition": {"expression": None, "values": {}},
                            },
                            "activated_rule": "ADM_OK",
                            "action_result": {"admission": True},
                        },
                        {
                            "rule_group": "course",
                            "verified_conditions": {
                                "condition": {"expression": "IS_AGE_UNKNOWN", "values": {"IS_AGE_UNKNOWN": True}},
                                "simple_condition": {"expression": None, "values": {}},
                            },
                            "activated_rule": "COURSE_SENIOR",
                            "action_result": {"course_id": "senior"},
                        },
                        {
                            "rule_group": "email",
                            "verified_conditions": {
                                "condition": {
                                    "expression": "HAS_SCHOOL_AUTHORIZED_POWER",
                                    "values": {"HAS_SCHOOL_AUTHORIZED_POWER": True},
                                },
                                "simple_condition": {"expression": None, "values": {}},
                            },
                            "activated_rule": "EMAIL_COOK",
                            "action_result": True,
                        },
                    ],
                },
                "admission": {"admission": True},
                "course": {"course_id": "senior"},
                "email": True,
            },
        ),
        (
            {
                "age": None,
                "language": "spanich",
                "powers": ["strength", "fly"],
                "favorite_meal": "Spinach",
                "DUMMY_KEY": "foo",
            },
            "good_conf",
            "second_rule_set",
            False,
            {
                "admission": {"admission": True},
                "course": {"course_id": "international"},
                "email": True,
            },
        ),
        (
            {
                "age": None,
                "language": "french",
                "powers": ["strength", "fly"],
                "favorite_meal": "Spinach",
                "DUMMY_KEY": "foo",
            },
            "good_conf",
            "second_rule_set",
            True,
            {
                "verbosity": {
                    "rule_set": "second_rule_set",
                    "results": [
                        {
                            "rule_group": "admission",
                            "verified_conditions": {
                                "condition": {
                                    "expression": "HAS_SCHOOL_AUTHORIZED_POWER",
                                    "values": {"HAS_SCHOOL_AUTHORIZED_POWER": True},
                                },
                                "simple_condition": {"expression": None, "values": {}},
                                "custom_condition": {
                                    "expression": "DUMMY_KEY or DUMMY_KEY_2",
                                    "values": {"DUMMY_KEY_2": False, "DUMMY_KEY": True},
                                },
                            },
                            "activated_rule": "ADM_OK",
                            "action_result": {"admission": True},
                        },
                        {
                            "rule_group": "course",
                            "verified_conditions": {
                                "condition": {
                                    "expression": "IS_SPEAKING_FRENCH",
                                    "values": {"IS_SPEAKING_FRENCH": True},
                                },
                                "simple_condition": {"expression": None, "values": {}},
                                "custom_condition": {"expression": None, "values": {}},
                            },
                            "activated_rule": "COURSE_FRENCH",
                            "action_result": {"course_id": "french"},
                        },
                        {
                            "rule_group": "email",
                            "verified_conditions": {
                                "condition": {
                                    "expression": "HAS_SCHOOL_AUTHORIZED_POWER and HAS_FAVORITE_MEAL",
                                    "values": {"HAS_FAVORITE_MEAL": True, "HAS_SCHOOL_AUTHORIZED_POWER": True},
                                },
                                "simple_condition": {"expression": None, "values": {}},
                                "custom_condition": {"expression": None, "values": {}},
                            },
                            "activated_rule": "EMAIL_COOK",
                            "action_result": True,
                        },
                    ],
                },
                "admission": {"admission": True},
                "course": {"course_id": "french"},
                "email": True,
            },
        ),
        (
            {
                "age": 5000,
                "language": "english",
                "powers": ["strength", "greek_gods", "regeneration", "immortality"],
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
                "DUMMY_KEY_2": "bar",
            },
            "good_conf",
            "second_rule_set",
            False,
            {
                "admission": {"admission": True},
                "course": {"course_id": "english"},
                "email": None,
            },
        ),
        (
            {
                "age": 5000,
                "language": "spanish",
                "powers": ["strength", "greek_gods", "regeneration", "immortality"],
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
                "DUMMY_KEY_3": "bar",
            },
            "good_conf",
            "second_rule_set",
            False,
            {
                "admission": {"admission": False},
                "course": {"course_id": "dummy_course"},
                "email": None,
            },
        ),
        (
            {
                "age": 5000,
                "language": "english",
                "powers": ["strength", "greek_gods", "regeneration", "immortality"],
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
                "DUMMY_KEY_4": None,
            },
            "good_conf",
            "third_rule_set",
            False,
            {
                "admission": {"admission": True},
            },
        ),
        (
            {
                "age": 5000,
                "language": "english",
                "powers": ["strength", "greek_gods", "regeneration", "immortality"],
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
                "DUMMY_KEY": None,
            },
            "good_conf",
            "third_rule_set",
            False,
            {
                "admission": {"admission": False},
            },
        ),
        (
            {
                "age": None,
                "language": "french",
                "powers": ["strength", "fly"],
                "favorite_meal": "Spinach",
            },
            "splitted_rule_set",
            "default_rule_set",
            False,
            {
                "admission": {"admission": True},
                "course": {"course_id": "senior"},
                "email": True,
            },
        ),
    ],
)
def test_conf_apply_rules(input_data, config_dir, rule_set, verbose, good_results, base_config_path):
    """Unit test of the method RulesEngine.apply_rules()"""
    path = os.path.join(base_config_path, config_dir)
    eng_1 = RulesEngine(config_path=path)
    res_1 = eng_1.apply_rules(input_data=input_data, rule_set=rule_set, verbose=verbose)

    config_dict = load_config(path)
    eng_2 = RulesEngine(config_dict=config_dict)
    res_2 = eng_2.apply_rules(input_data=input_data, rule_set=rule_set, verbose=verbose)

    assert res_1 == res_2 == good_results


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
                "action": lambda x, **kwargs: x,
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


def test_ignore_global_strategy(base_config_path):
    """Unit test of the class RulesEngine"""
    # Config. instanciation
    engine = RulesEngine(config_path=os.path.join(base_config_path, "ignore_conf"))
    assert isinstance(engine, RulesEngine)

    # Dummy action function
    context_data = {"dummy": "dummy"}

    result = engine.apply_rules(context_data)

    assert result == {"test_action": "My name is None"}


@pytest.mark.parametrize(
    "input_data, good_results",
    [
        (
            {
                "age": 5000,
                "language": "english",
                "powers": ["greek_gods", "regeneration"],
                "favorite_meal": None,
                "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
            },
            {"admission_rules": {"admission": True}},
        ),
    ],
)
def test_kwargs_in_apply_rules(input_data, good_results, base_config_path):
    """Unit test of user extra arguments."""
    config_path = os.path.join(base_config_path, "good_conf")
    eng = RulesEngine(config_path=config_path)
    res = eng.apply_rules(input_data, rule_set="fourth_rule_set", my_parameter="super@connection")

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

    eng_2 = RulesEngine(rules_dict=rules_raw, ignored_rules=["ignored_1", "ignored_2"])
    res = eng_2.apply_rules(input_data, verbose=False)

    assert res == expected_results
