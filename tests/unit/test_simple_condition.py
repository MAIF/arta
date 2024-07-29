"""UT of the simple conditions."""

import os

import pytest
from arta import RulesEngine
from arta.exceptions import ConditionExecutionError, RuleExecutionError


@pytest.mark.parametrize(
    "input_data, config_dir, ignored_rules, good_results",
    [
        (
            {
                "age": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "simple_cond_conf/default",
            None,
            {"admission": {"admission": True}, "course": {"course_id": "senior"}, "email": True},
        ),
        (
            {
                "age": 30,
                "language": "english",
                "power": "fly",
                "favorite_meal": None,
            },
            "simple_cond_conf/default",
            None,
            {"admission": {"admission": True}, "course": {"course_id": "english"}, "email": None},
        ),
        (
            {
                "age": None,
                "language": "german",
                "power": "invisibility",
                "favorite_meal": "French Fries",
            },
            "simple_cond_conf/default",
            None,
            {"admission": {"admission": False}, "course": {"course_id": "senior"}, "email": None},
        ),
        (
            {
                "dummy": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "simple_cond_conf/ignore",
            None,
            {"admission": {"admission": True}, "course": {"course_id": "senior"}, "email": True},
        ),
        (
            {
                "age": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "simple_cond_conf/wrong/ignore",
            None,
            {"admission": {"admission": True}, "course": {"course_id": "senior"}, "email": True},
        ),
        (
            {
                "text": "super hero super hero",
            },
            "simple_cond_conf/whitespace",
            None,
            {"whitespace": "OK"},
        ),
        (
            {
                "text": "SUPER HERO",
            },
            "simple_cond_conf/uppercase",
            None,
            {"uppercase": "OK"},
        ),
        (
            {
                "text": "SUPER HERO",
            },
            "simple_cond_conf/uppercase",
            set(),
            {"uppercase": "OK"},
        ),
        (
            {"age": 100, "power": "strength"},
            "simple_cond_conf/ignored_rules",
            {"IGNORED_RULE_1", "IGNORED_RULE_2"},
            {"admission": {"admission": False}},
        ),
    ],
)
def test_simple_condition(input_data, config_dir, ignored_rules, good_results, base_config_path):
    """Unit test of the method RulesEngine.apply_rules()"""
    config_path = os.path.join(base_config_path, config_dir)
    eng = RulesEngine(config_path=config_path)
    res = eng.apply_rules(input_data=input_data, ignored_rules=ignored_rules)

    assert res == good_results


@pytest.mark.parametrize(
    "input_data, good_results",
    [
        (
            {
                "age": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            {
                "verbosity": {
                    "rule_set": "default_rule_set",
                    "results": [
                        {
                            "rule_group": "admission",
                            "verified_conditions": {
                                "condition": {"expression": None, "values": {}},
                                "simple_condition": {
                                    "expression": (
                                        'input.power=="strength" or input.power=="fly" or input.'
                                        'power=="time-manipulation"'
                                    ),
                                    "values": {
                                        'input.power=="strength"': True,
                                        'input.power=="fly"': False,
                                        'input.power=="time-manipulation"': False,
                                    },
                                },
                            },
                            "activated_rule": "ADM_OK",
                            "action_result": {"admission": True},
                        },
                        {
                            "rule_group": "course",
                            "verified_conditions": {
                                "condition": {"expression": None, "values": {}},
                                "simple_condition": {
                                    "expression": "input.age>=100 or input.age==None",
                                    "values": {"input.age==None": False, "input.age>=100": True},
                                },
                            },
                            "activated_rule": "COURSE_SENIOR",
                            "action_result": {"course_id": "senior"},
                        },
                        {
                            "rule_group": "email",
                            "verified_conditions": {
                                "condition": {"expression": None, "values": {}},
                                "simple_condition": {
                                    "expression": "input.favorite_meal!=None and not output.admission.admission==False",
                                    "values": {
                                        "input.favorite_meal!=None": True,
                                        "output.admission.admission==False": False,
                                    },
                                },
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
    ],
)
def test_simple_condition_verbose(input_data, good_results, base_config_path):
    """Unit test of the method RulesEngine.apply_rules()"""
    config_path = os.path.join(base_config_path, "simple_cond_conf/default")
    eng = RulesEngine(config_path=config_path)
    res = eng.apply_rules(input_data=input_data, verbose=True)

    assert res == good_results


@pytest.mark.parametrize(
    "input_data, config_dir, expected_error",
    [
        (
            {
                "dummy": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "simple_cond_conf/default",
            ConditionExecutionError,
        ),
        (
            {
                "dummy": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "simple_cond_conf/raise",
            ConditionExecutionError,
        ),
        (
            {
                "age": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "simple_cond_conf/wrong/dummy",
            RuleExecutionError,
        ),
        (
            {
                "age": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "simple_cond_conf/wrong/raise",
            ConditionExecutionError,
        ),
    ],
)
def test_error_apply_rules_missing_input_key(input_data, config_dir, expected_error, base_config_path):
    """Unit test of RulesEngine.apply_process with config_path instance."""
    config_path = os.path.join(base_config_path, config_dir)
    eng = RulesEngine(config_path=config_path)

    with pytest.raises(expected_error):
        _ = eng.apply_rules(input_data=input_data, verbose=False)


# @pytest.mark.skip(reason="Not yet implemented, coming soon")
@pytest.mark.parametrize(
    "input_data, config_dir, good_results",
    [
        (
            {
                "a": 1.3,
                "b": 0.7,
                "threshold": 0.89,
            },
            "simple_cond_conf/math",
            {
                "add": "greater than threshold",
                "sub": "less or equal than threshold",
                "mul": "greater than threshold",
                "div": "greater than threshold",
                "equal_1": "no",
                "equal_2": "yes",
            },
        ),
    ],
)
def test_math(input_data, config_dir, good_results, base_config_path):
    """Unit test of the method RulesEngine.apply_rules()"""
    config_path = os.path.join(base_config_path, config_dir)
    eng = RulesEngine(config_path=config_path)
    res = eng.apply_rules(input_data=input_data)

    assert res == good_results
