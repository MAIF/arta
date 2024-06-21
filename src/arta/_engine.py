"""Module implementing the rules engine.

Class: RulesEngine
"""

from __future__ import annotations

import copy
import importlib
import inspect
from inspect import getmembers, isclass, isfunction
from types import FunctionType, MethodType, ModuleType
from typing import Any, Callable

from arta.condition import BaseCondition, SimpleCondition, StandardCondition
from arta.config import load_config
from arta.models import Configuration, RulesDict
from arta.rule import Rule
from arta.utils import ParsingErrorStrategy


class RulesEngine:
    """The Rules Engine is in charge of executing different groups of rules of a given rule set on user input data.

    Attributes:
        rules:  A dictionary of rules with k: rule set, v: (k: rule group, v: list of rule instances).
    """

    # ==== Class constants ====

    # Rule related config keys
    CONST_RULE_SETS_CONF_KEY: str = "rules"
    CONST_DFLT_RULE_SET_ID: str = "default_rule_set"
    CONST_STD_RULE_CONDITION_CONF_KEY: str = "condition"
    CONST_ACTION_CONF_KEY: str = "action"
    CONST_ACTION_PARAMETERS_CONF_KEY: str = "action_parameters"

    # Condition related config keys
    CONST_STD_CONDITIONS_CONF_KEY: str = "conditions"
    CONST_CONDITION_VALIDATION_FUNCTION_CONF_KEY: str = "validation_function"
    CONST_CONDITION_DESCRIPTION_CONF_KEY: str = "description"
    CONST_CONDITION_VALIDATION_PARAMETERS_CONF_KEY: str = "condition_parameters"
    CONST_USER_CONDITION_STRING: str = "USER_CONDITION"

    # Built-in factory mapping
    BUILTIN_FACTORY_MAPPING: dict[str, type[BaseCondition]] = {
        "condition": StandardCondition,
        "simple_condition": SimpleCondition,
    }

    def __init__(
        self,
        *,
        rules_dict: dict[str, dict[str, Any]] | None = None,
        config_path: str | None = None,
    ) -> None:
        """Initialize the rules.

        2 possibilities: either 'rules_dict', or 'config_path', not both.

        Args:
            rules_dict: A dictionary containing the rules' definitions.
            config_path: Path of a directory containing the YAML files.

        Raises:
            KeyError: Key not found.
            TypeError: Wrong type.
            ValueError: Bad given parameters.
        """
        # Var init.
        factory_mapping_classes: dict[str, type[BaseCondition]] = {}
        std_condition_instances: dict[str, StandardCondition] = {}

        if config_path is not None and rules_dict is not None:
            raise ValueError("RulesEngine takes only one parameter: 'rules_dict' or 'config_path', not both.")

        # Init. default parsing_error_strategy (probably not needed because already defined elsewhere)
        self._parsing_error_strategy: ParsingErrorStrategy = ParsingErrorStrategy.RAISE

        # Initialize directly with a rules dict
        if rules_dict is not None:
            # Data validation
            RulesDict.parse_obj(rules_dict)

            # Edge cases data validation
            if not isinstance(rules_dict, dict):
                raise TypeError(f"'rules_dict' must be dict type, not '{type(rules_dict)}'")
            elif len(rules_dict) == 0:
                raise KeyError("'rules_dict' couldn't be empty.")

            # Attribute definition
            self.rules: dict[str, dict[str, list[Rule]]] = self._adapt_user_rules_dict(rules_dict)

        # Initialize with a config_path
        elif config_path is not None:
            # Load config in attribute
            config_dict: dict[str, Any] = load_config(config_path)

            # Data validation
            config: Configuration = Configuration(**config_dict)

            if config.parsing_error_strategy is not None:
                # Set parsing error handling strategy from config
                self._parsing_error_strategy = ParsingErrorStrategy(config.parsing_error_strategy)

            # dict of available action functions (k: function name, v: function object)
            action_modules: list[str] = config.actions_source_modules
            action_functions: dict[str, Callable] = self._get_object_from_source_modules(action_modules)

            # dict of available standard condition functions (k: function name, v: function object)
            condition_modules: list[str] = (
                config.conditions_source_modules if config.conditions_source_modules is not None else []
            )
            std_condition_functions: dict[str, Callable] = self._get_object_from_source_modules(condition_modules)

            # Dictionary of condition instances (k: condition id, v: instance), built from config data
            if len(std_condition_functions) > 0:
                std_condition_instances = self._build_std_conditions(
                    config=config.dict(), condition_functions_dict=std_condition_functions
                )

            # User-defined/custom conditions
            if config.condition_factory_mapping is not None and config.custom_classes_source_modules is not None:
                # dict of custom condition classes (k: classe name, v: class object)
                custom_condition_classes: dict[str, type[BaseCondition]] = self._get_object_from_source_modules(
                    config.custom_classes_source_modules
                )

                # Build a factory mapping dictionary (k: conf key, v:class object)
                factory_mapping_classes.update(
                    {
                        conf_key: custom_condition_classes[class_name]
                        for conf_key, class_name in config.condition_factory_mapping.items()
                    }
                )

            # Arta built-in conditions
            factory_mapping_classes.update(self.BUILTIN_FACTORY_MAPPING)

            # Attribute definition
            self.rules = self._build_rules(
                std_condition_instances=std_condition_instances,
                action_functions=action_functions,
                config=config.dict(),
                factory_mapping_classes=factory_mapping_classes,
            )
        else:
            raise ValueError("RulesEngine needs a parameter: 'rule_dict' or 'config_path'.")

    def apply_rules(
        self, input_data: dict[str, Any], *, rule_set: str | None = None, verbose: bool = False, **kwargs: Any
    ) -> dict[str, Any]:
        """Apply the rules and return results.

        For each rule group of a given rule set, rules are applied sequentially,
        The loop is broken when a rule is applied (an action is triggered).
        Then, the next rule group is evaluated.
        And so on...

        This means that the order of the rules in the configuration file
        (e.g., rules.yaml) is meaningful.

        Args:
            input_data: Input data to apply rules on.
            rule_set: Apply rules associated with the specified rule set.
            verbose: If True, add extra ids (group_id, rule_id) for result explicability.
            **kwargs: For user extra arguments.

        Returns:
            A dictionary containing the rule groups' results (k: group id, v: action result).

        Raises:
            TypeError: Wrong type (e.g., input_data is not a dictionary).
            KeyError: Key not found (e.g., input_data is an empty dictionary).
            RuleExecutionError: A rule fails during execution.
            ConditionExecutionError: A condition fails during execution.
        """
        # Input_data validation
        if not isinstance(input_data, dict):
            raise TypeError(f"'input_data' must be dict type, not '{type(input_data)}'")
        elif len(input_data) == 0:
            raise KeyError("'input_data' couldn't be empty.")

        # Var init.
        input_data_copy: dict[str, Any] = copy.deepcopy(input_data)

        # Prepare the result key
        input_data_copy["output"] = {}

        # If there is no given rule set param. and there is only one rule set in self.rules
        # and its value is 'default_rule_set', look for this one (rule_set='default_rule_set')
        if rule_set is None and len(self.rules) == 1 and self.rules.get(self.CONST_DFLT_RULE_SET_ID) is not None:
            rule_set = self.CONST_DFLT_RULE_SET_ID

        # Check if given rule set is in self.rules?
        if rule_set not in self.rules:
            raise KeyError(
                f"Rule set '{rule_set}' not found in the rules, available rule sets are : {list(self.rules.keys())}."
            )

        # Var init.
        results_dict: dict[str, Any] = {"verbosity": {"rule_set": rule_set, "results": []}}

        # Groups' loop
        for group_id, rules_list in self.rules[rule_set].items():
            # Initialize result of the rule group with None
            results_dict[group_id] = None

            # Rules' loop (inside a group)
            for rule in rules_list:
                # Apply rules
                action_result, rule_details = rule.apply(
                    input_data_copy, parsing_error_strategy=self._parsing_error_strategy, **kwargs
                )

                # Check if the rule has been applied (= action activated)
                if "action_result" in rule_details:
                    # Save result and details
                    results_dict[group_id] = action_result
                    results_dict["verbosity"]["results"].append(rule_details)

                    # Update input data with current result with key 'output' (can be used in next rules)
                    input_data_copy["output"][group_id] = copy.deepcopy(results_dict[group_id])

                    # We can only have one result per group => break when "action_result" in rule_details
                    break

        # Handling non-verbose mode
        if not verbose:
            results_dict.pop("verbosity")

        return results_dict

    @staticmethod
    def _get_object_from_source_modules(module_list: list[str]) -> dict[str, Any]:
        """(Protected)
        Collect all functions defined in the list of modules.

        Args:
            module_list: List of source module names.

        Returns:
            Dictionary with objects found in the modules.
        """
        object_dict: dict[str, Any] = {}

        for module_name in module_list:
            # Import module
            mod: ModuleType = importlib.import_module(module_name)

            # Collect functions
            module_functions: dict[str, Any] = {key: val for key, val in getmembers(mod, isfunction)}
            object_dict.update(module_functions)

            # Collect classes
            module_classes: dict[str, Any] = {key: val for key, val in getmembers(mod, isclass)}
            object_dict.update(module_classes)

        return object_dict

    def _build_rules(
        self,
        std_condition_instances: dict[str, StandardCondition],
        action_functions: dict[str, Callable],
        config: dict[str, Any],
        factory_mapping_classes: dict[str, type[BaseCondition]],
    ) -> dict[str, dict[str, list[Any]]]:
        """(Protected)
        Return a dictionary of Rule instances built from the configuration.

        Args:
            rule_sets: Sets of rules to be loaded in the Rules Engine (as needed by further uses).
            std_condition_instances: Dictionary of condition instances (k: condition id, v: StandardCondition instance)
            actions_dict: Dictionary of action functions (k: action name, v: Callable)
            config: Dictionary of the imported configuration from yaml files.
            factory_mapping_classes: A mapping dictionary (k: condition conf. key, v: custom class object)

        Returns:
            A dictionary of rules.
        """
        # Var init.
        rules_dict: dict[str, dict[str, list[Any]]] = {}

        # Retrieve rule set ids from config
        rule_set_ids: list[str] = list(config[self.CONST_RULE_SETS_CONF_KEY].keys())

        # Going all way down to the rules (rule set > rule group > rule)
        for set_id in rule_set_ids:
            rules_conf: dict[str, Any] = config[self.CONST_RULE_SETS_CONF_KEY][set_id]
            rules_dict[set_id] = {}
            rule_set_dict: dict[str, list[Any]] = rules_dict[set_id]

            # Looping throught groups
            for group_id, group_rules in rules_conf.items():
                # Initialize list or rules in the group
                rule_set_dict[group_id] = []

                # Looping through rules (inside a group)
                for rule_id, rule_dict in group_rules.items():
                    # Get action function
                    action_function_name: str = rule_dict[self.CONST_ACTION_CONF_KEY]

                    if action_function_name not in action_functions:
                        raise KeyError(f"Unknwown action function : {action_function_name}")

                    action: Callable = action_functions[action_function_name]

                    # Look for condition conf. keys inside the rule
                    condition_conf_keys: set[str] = set(rule_dict.keys()) - {
                        self.CONST_ACTION_CONF_KEY,
                        self.CONST_ACTION_PARAMETERS_CONF_KEY,
                    }

                    # Store the cond. expressions with the same order as in the configuration file (very important)
                    condition_exprs: dict[str, str | None] = {
                        key: value for key, value in rule_dict.items() if key in condition_conf_keys
                    }

                    # Create the corresponding Rule instance
                    rule: Rule = Rule(
                        set_id=set_id,
                        group_id=group_id,
                        rule_id=rule_id,
                        action=action,
                        action_parameters=rule_dict[self.CONST_ACTION_PARAMETERS_CONF_KEY],
                        condition_exprs=condition_exprs,
                        std_condition_instances=std_condition_instances,
                        condition_factory_mapping=factory_mapping_classes,
                    )
                    rule_set_dict[group_id].append(rule)

        return rules_dict

    def _build_std_conditions(
        self, config: dict[str, Any], condition_functions_dict: dict[str, Callable]
    ) -> dict[str, StandardCondition]:
        """(Protected)
        Return a dictionary of Condition instances built from the configuration file.

        Args:
            config: Dictionary of the imported configuration from yaml files.
            condition_functions_dict: A dictionary where k:condition id, v:Callable (validation function).

        Returns:
            A dictionary of StandardCondition instances (k: condition id, v: StandardCondition instance).
        """
        # Var init.
        conditions_dict: dict[str, StandardCondition] = {}

        # Condition configuration (under conditions' key)
        conditions_conf: dict[str, dict[str, Any]] = config[self.CONST_STD_CONDITIONS_CONF_KEY]

        # Looping through conditions (inside a group)
        for condition_id, condition_params in conditions_conf.items():
            # Get condition validation function
            validation_function_name: str = condition_params[self.CONST_CONDITION_VALIDATION_FUNCTION_CONF_KEY]

            if validation_function_name not in condition_functions_dict:
                raise KeyError(f"Unknwown validation function : {validation_function_name}")

            # Get Callable from function name
            validation_function: Callable = condition_functions_dict[validation_function_name]

            # Create Condition instance
            condition_instance: StandardCondition = StandardCondition(
                condition_id=condition_id,
                description=condition_params[self.CONST_CONDITION_DESCRIPTION_CONF_KEY],
                validation_function=validation_function,
                validation_function_parameters=condition_params[self.CONST_CONDITION_VALIDATION_PARAMETERS_CONF_KEY],
            )
            conditions_dict[condition_id] = condition_instance

        return conditions_dict

    def _adapt_user_rules_dict(self, rules_dict: dict[str, dict[str, Any]]) -> dict[str, dict[str, list[Any]]]:
        """(Protected)
        Return a dictionary of Rule's instances built from user's rules dictionary.

        Args:
            rules_dict: User raw rules dictionary.

        Returns:
            A rules dictionary made from the user input rules.
        """
        # Var init.
        rules_dict_formatted: dict[str, list[Any]] = {}

        # Looping throught groups
        for group_id, group_rules in rules_dict.items():
            # Initialize list or rules in the group
            rules_dict_formatted[group_id] = []

            # Looping through rules (inside a group)
            for rule_id, rule_dict in group_rules.items():
                # Get action function
                action = rule_dict["action"]

                # Trigger if not **kwargs
                if "kwargs" not in inspect.signature(action).parameters:
                    raise KeyError(f"The action function {action} must have a '**kwargs' parameter.")

                # Create Rule instance
                rule = Rule(
                    set_id=self.CONST_DFLT_RULE_SET_ID,
                    group_id=group_id,
                    rule_id=rule_id,
                    action=action,
                    action_parameters=rule_dict.get(self.CONST_ACTION_PARAMETERS_CONF_KEY),
                    condition_exprs={self.CONST_STD_RULE_CONDITION_CONF_KEY: self.CONST_USER_CONDITION_STRING}
                    if self.CONST_STD_RULE_CONDITION_CONF_KEY in rule_dict
                    and rule_dict.get(self.CONST_STD_RULE_CONDITION_CONF_KEY) is not None
                    else {self.CONST_STD_RULE_CONDITION_CONF_KEY: None},
                    std_condition_instances={
                        self.CONST_USER_CONDITION_STRING: StandardCondition(
                            condition_id=self.CONST_USER_CONDITION_STRING,
                            description="Automatic description",
                            validation_function=rule_dict.get(self.CONST_STD_RULE_CONDITION_CONF_KEY),
                            validation_function_parameters=rule_dict.get(
                                self.CONST_CONDITION_VALIDATION_PARAMETERS_CONF_KEY
                            ),
                        )
                    },
                    condition_factory_mapping=self.BUILTIN_FACTORY_MAPPING,
                )
                rules_dict_formatted[group_id].append(rule)

        return {self.CONST_DFLT_RULE_SET_ID: rules_dict_formatted}

    def __str__(self) -> str:
        """Object human string representation (called by str()).

        Returns:
            A string representation of the instance.
        """
        # Vars init.
        attrs_str: str = ""

        # Get some instance attributes infos
        class_name: str = self.__class__.__name__
        attrs: list[tuple[str, Any]] = [
            attr
            for attr in inspect.getmembers(self)
            if not (
                attr[0].startswith("_")
                or attr[0].startswith("CONST_")
                or isinstance(attr[1], (FunctionType, MethodType))
            )
        ]

        # Build string representation
        for attr, val in attrs:
            attrs_str += f"{attr}={str(val)}, "

        return f"{class_name}({attrs_str})"
