"""Module containing the class implementation of a rule.

Class: Rule
"""

from __future__ import annotations

import re
from typing import Any, Callable

from arta.condition import BaseCondition, StandardCondition
from arta.exceptions import ConditionExecutionError, RuleExecutionError
from arta.utils import (
    ParsingErrorStrategy,
    parse_dynamic_parameter,
)


class Rule:
    """A rule is the combination of some conditions and one action.

    Attributes:
        set_id: An id of a rule set.
        group_id: An id of a rule group.
        rule_id: The id of the rule.
        condition_exprs: A dictionary of condition expressions (k: condition conf. key, v: condition expression).
        condition_factory_mapping: A dictionary mapping between condition conf. keys and condition class objects
                                    (k: condition conf. key, v: condition class object).
        action: Function to perform when the conditions are valid (action function).
        action_parameters: Parameters of the action function.
    """

    def __init__(
        self,
        set_id: str,
        group_id: str,
        rule_id: str,
        condition_exprs: dict[str, str | None],
        condition_factory_mapping: dict[str, type[BaseCondition]],
        action: Callable,
        std_condition_instances: dict[str, StandardCondition],
        action_parameters: dict[str, Any] | None = None,
    ) -> None:
        """Initialize attributes.

        Args:
            std_condition_instances: Dictionary containing the BaseCondition instances required by the Rule
                (k: condition_id, v: StandardCondition instance).
        """
        # IDs
        self._set_id = set_id
        self._group_id = group_id
        self._rule_id = rule_id

        # Action
        self._action = action
        self._action_parameters = action_parameters or {}

        # Condition expressions
        self._condition_exprs = condition_exprs

        # Factory mapping
        self._condition_factory_mapping = condition_factory_mapping

        # Condition instances (k: condition id (not conf key), v: instances)
        self._condition_instances: dict[str, BaseCondition] = self._instantiate_conditions(std_condition_instances)

    def apply(
        self,
        input_data: dict[str, Any],
        *,
        parsing_error_strategy: ParsingErrorStrategy,
        **kwargs: Any,
    ) -> tuple[Any | None, dict[str, Any]]:
        """Apply the rule on the input data, return action output (optional).

        Args:
            input_data: Request or input data to apply rules on.
            parsing_error_strategy: Parsing error strategy.
            **kwargs: For user extra arguments.

        Returns:
            A tuple as: (action result, rule result details).

        Raises:
            RuleExecutionError: Error during the rule execution.
        """
        # If rule conditions are verified, the action is executed w/ the parameters' value
        is_conditions_ok: bool
        rule_results: dict[str, Any]

        is_conditions_ok, rule_results = self._check_conditions(
            input_data, parsing_error_strategy=parsing_error_strategy, **kwargs
        )

        if is_conditions_ok:
            try:
                # Parse dynamic parameters
                parameters: dict[str, Any] = {}
                for key, value in self._action_parameters.items():
                    parameters[key] = parse_dynamic_parameter(
                        parameter=value, input_data=input_data, parsing_error_strategy=parsing_error_strategy
                    )

                # Track the rule id
                rule_results["activated_rule"] = self._rule_id

                # Run action
                rule_results["action_result"] = self._action(**parameters, input_data=input_data)

                return rule_results["action_result"], rule_results
            except Exception as error:
                raise RuleExecutionError(f"Error while executing rule '{self._rule_id}': {str(error)}") from error

        else:
            return None, {}

    def _check_conditions(
        self, input_data: dict[str, Any], parsing_error_strategy: ParsingErrorStrategy, **kwargs: Any
    ) -> tuple[bool, dict[str, Any]]:
        """(Protected)
        Return True if all conditions are verified.

        Args:
            input_data: Request or input data to apply rules on.
            parsing_error_strategy: Error handling strategy for parameter's parsing.
            **kwargs: For user extra arguments.

        Returns:
            A tuple as: (True if all conditions are verified, otherwise False, condition results dictionary).
        """
        # Var init.
        all_conditions_res: bool = True
        condition_results: dict[str, Any] = {"rule_group": self._group_id, "verified_conditions": {}}

        # Loop among condition expressions
        for cond_conf_key, expr in self._condition_exprs.items():
            condition_class: type[BaseCondition] = self._condition_factory_mapping[cond_conf_key]

            # Evaluate the condition expression
            try:
                condition_res, unitary_res = self._evaluate_condition_expr(
                    input_data=input_data,
                    condition_class=condition_class,
                    condition_expr=expr,
                    parsing_error_strategy=parsing_error_strategy,
                    **kwargs,
                )
            except NameError as e:
                raise RuleExecutionError(f"Error during evaluation of '{cond_conf_key}: {expr}': {str(e)}") from e

            # Combine conditions (AND)
            all_conditions_res = all_conditions_res and condition_res

            # Store condition results
            condition_results["verified_conditions"].update(
                {cond_conf_key: {"expression": expr, "values": unitary_res}}
            )

            if not all_conditions_res:
                # If False, no need to go further
                break

        return all_conditions_res, condition_results

    def _evaluate_condition_expr(
        self,
        input_data: dict[str, Any],
        condition_class: type[BaseCondition],
        parsing_error_strategy: ParsingErrorStrategy,
        condition_expr: str | None = None,
        **kwargs: Any,
    ) -> tuple[bool, dict[str, bool]]:
        """(Protected)
        Evaluate the condition expr (a boolean expression) and
        return the result (a boolean).

        Args:
            input_data: Request or input data.
            condition_class: Class object of the analyzed condition (given by its conf. key).
            parsing_error_strategy: Error handling strategy for parameter's parsing.
            condition_expr: A boolean expression (string).
            **kwargs: For user extra arguments.

        Returns:
            A tuple as: (final result, unitary results (dictionary)).

        Raises:
            ConditionExecutionError: Error during condition execution.
        """
        # Var init.
        unitary_results: dict[str, bool] = {}

        # Case of null condition expressions => Always True
        if condition_expr is None:
            return True, unitary_results

        # The final boolean expression is formed by replacing condition IDs by their evaluated boolean values
        bool_expr: str = condition_expr

        # Extract condition ids from the expression
        condition_ids: set[str] = condition_class.extract_condition_ids_from_expression(condition_expr)

        # Loop among the conditions of the expression
        # Verify the unitary condition
        for cond_id in condition_ids:
            # Retrieve condition instance
            condition: BaseCondition = self._condition_instances[cond_id]

            # Check unitary condition
            try:
                bool_var: bool = condition.verify(input_data, parsing_error_strategy=parsing_error_strategy, **kwargs)

                # Store unitary result
                unitary_results[cond_id] = bool_var
            except Exception as error:
                raise ConditionExecutionError(f"Error while executing condition '{cond_id}': {str(error)}") from error

            # Replace the result in the boolean expression
            sanit_cond_id: str = condition.get_sanitized_id()
            bool_expr = re.sub(rf"{sanit_cond_id}", str(bool_var), bool_expr)

        # Evaluate the final boolean expressions = final result
        return eval(bool_expr), unitary_results  # noqa

    def _instantiate_conditions(
        self,
        std_conditions: dict[str, StandardCondition],
    ) -> dict[str, BaseCondition]:
        """Parse condition expressions and build corresponding instances.

        E.g., for one condition:
        - Input : "not(CONDITION_A) and CONDITION_B"
        - Output : {"CONDITION_A": condition_A_instance, "CONDITION_B": condition_B_instance}

        Args:
            std_conditions: A dictionary containing the StandardCondition instances
                (k: cond. id, v: StandardCondition instance)

        Returns:
            Condition instances which are in the condition expressions (k: condition id, v: BaseCondition instance).

        Raises:
            KeyError: Condition id is unknown.
        """
        # Var init.
        condition_ids: set[str] = set()
        cond_instances: dict[str, BaseCondition] = {}

        # Get all condition ids from the expressions (1 or many)
        for conf_key, expr in self._condition_exprs.items():
            # Expression parsing is condition class dependent
            condition_ids = self._condition_factory_mapping[conf_key].extract_condition_ids_from_expression(expr)

            # Is a custom condition or a simple condition?
            if self._condition_factory_mapping is not None and conf_key != "condition":
                # Yes
                for cond_id in condition_ids:
                    # Instanciate the custom (unknown) condition object
                    cond_instances[cond_id] = self._condition_factory_mapping[conf_key](
                        condition_id=cond_id,
                        description=self._condition_factory_mapping[conf_key].CONDITION_DATA_LABEL,
                    )
            else:
                # Should be a standard condition
                for cond_id in condition_ids:
                    # Retrieve the standard condition instance (already instantiated)
                    try:
                        cond_instances[cond_id] = std_conditions[cond_id]
                    except KeyError as error:
                        raise KeyError(
                            f"Following condition id is unknown '{cond_id}' in {conf_key}: {expr}"
                        ) from error

        return cond_instances
