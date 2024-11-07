"""Pydantic model implementations.

Note: Having no "from __future__ import annotations" here is wanted (pydantic compatibility).
"""

from typing import Any, Callable, Dict, List, Optional, Annotated

from arta.pydantic_binding import (
    field_validator,
    BaseModel,
    RootModel,
    StringConstraints
)

from arta.utils import ParsingErrorStrategy


# ----------------------------------
# For instantiation using rules_dict
class RuleRaw(BaseModel):
    """Pydantic model for validating a rule."""

    condition: Optional[Callable]
    condition_parameters: Optional[Dict[str, Any]]
    action: Callable
    action_parameters: Optional[Dict[str, Any]]

    model_config = {'extra': 'forbid'}


class RulesGroup(RootModel):
    """Pydantic model for validating a rules group."""

    root: Dict[str, RuleRaw]


class RulesDict(RootModel):
    """Pydantic model for validating rules dict instanciation."""

    root: Dict[str, RulesGroup]


# ----------------------------------
# For instantiation using config_path
class Condition(BaseModel):
    """Pydantic model for validating a condition."""

    description: str
    validation_function: str
    condition_parameters: Optional[Dict[str, Any]] = None


class RulesConfig(BaseModel):
    """Pydantic model for validating a rule group from config file."""

    condition: Optional[str] = None
    simple_condition: Optional[str] = None
    action: Annotated[str, StringConstraints(to_lower=True)]  # type: ignore
    action_parameters: Optional[Any] = None

    model_config = {'extra': 'allow'}

class Configuration(BaseModel):
    """Pydantic model for validating configuration files."""

    conditions: Optional[Dict[str, Condition]] = None
    conditions_source_modules: Optional[List[str]] = None
    actions_source_modules: List[str]
    custom_classes_source_modules: Optional[List[str]] = None
    condition_factory_mapping: Optional[Dict[str, str]] = None
    rules: Dict[str, Dict[str, Dict[str, RulesConfig]]]
    parsing_error_strategy: Optional[ParsingErrorStrategy] = None

    model_config = {'extra': 'ignore'}

    @field_validator('rules', mode='before')
    def upper_key(cls, vl): # noqa
        for k, v in vl.items():
            for kk, vv in v.items():
                for key, rules in [*vv.items()]:
                    if key != str(key).upper():
                        del vl[k][kk][key]
                        vl[k][kk][str(key).upper()] = rules
        return vl
