import logging
from pathlib import Path


from arta import RulesEngine


def test_info_logs(base_config_path, caplog):
    """Only logs at INFO level are tested."""
    caplog.set_level(logging.INFO, logger="arta")

    config_dir = Path(base_config_path) / "good_conf"

    eng = RulesEngine(config_path=config_dir)

    assert (
        caplog.messages[-1]
        == "Rules engine correctly instanciated with 'ParsingErrorStrategy.RAISE' and 'RuleActivationMode.ONE_BY_GROUP'"
    )

    input_data = {
        "age": None,
        "language": "french",
        "powers": ["strength", "fly"],
        "favorite_meal": "Spinach",
    }

    eng.apply_rules(input_data, rule_set="default_rule_set")

    assert caplog.messages[-1] == "'4' rules were correctly evaluated against input data."
