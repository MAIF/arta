"""UT of the rule activation mode."""

import os

import pytest

from arta import RulesEngine


@pytest.mark.parametrize(
    "input_data, config_dir, good_results",
    [
        (
            {
                "age": 100,
                "language": "french",
                "power": "strength",
                "favorite_meal": "Spinach",
            },
            "rule_activation_mode",
            {
                "rg_1": "b",
                "rg_2": "be",
                "rg_3": "bef",
            },
        ),
        (
            {
                "age": None,
                "language": "english",
                "power": "strength",
                "favorite_meal": None,
            },
            "rule_activation_mode",
            {
                "rg_1": "b",
                "rg_2": "bd",
                "rg_3": None,
            },
        ),
        (
            {"key": "value"},
            "process_execution",
            {
                "gr_1": "ab",
                "gr_2": "abcde",
                "gr_3": "abcdef",
            },
        ),
    ],
)
def test_many_by_group(input_data, config_dir, good_results, base_config_path):
    """Unit test of the regular case"""
    config_path = os.path.join(base_config_path, config_dir)
    eng = RulesEngine(config_path=config_path)
    res = eng.apply_rules(input_data=input_data)
    assert res == good_results
