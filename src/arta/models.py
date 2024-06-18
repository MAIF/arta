"""Pydantic model implementations.

Note: Having no "from __future__ import annotations" here is wanted (pydantic compatibility).
"""

from typing import Any, Callable, Dict, List, Optional

try:
    from pydantic import v1 as pydantic
except ImportError:
    import pydantic  # type: ignore

from arta.utils import ParsingErrorStrategy


# ----------------------------------
# For instantiation using rules_dict
class RuleRaw(pydantic.BaseModel):
    """Pydantic model for validating a rule."""

    condition: Optional[Callable]
    condition_parameters: Optional[Dict[str, Any]]
    action: Callable
    action_parameters: Optional[Dict[str, Any]]

    class Config:
        extra = "forbid"


class RulesGroup(pydantic.BaseModel):
    """Pydantic model for validating a rules group."""

    __root__: Dict[str, RuleRaw]


class RulesDict(pydantic.BaseModel):
    """Pydantic model for validating rules dict instanciation."""

    __root__: Dict[str, RulesGroup]


# ----------------------------------
# For instantiation using config_path
class Condition(pydantic.BaseModel):
    """Pydantic model for validating a condition."""

    description: str
    validation_function: str
    condition_parameters: Optional[Dict[str, Any]]


class RulesConfig(pydantic.BaseModel):
    """Pydantic model for validating a rule group from config file."""

    condition: Optional[str]
    simple_condition: Optional[str]
    action: pydantic.constr(to_lower=True)  # type: ignore
    action_parameters: Optional[Any]

    class Config:
        extra = "allow"


class Configuration(pydantic.BaseModel):
    """Pydantic model for validating configuration files."""

    conditions: Optional[Dict[str, Condition]]
    conditions_source_modules: Optional[List[str]]
    actions_source_modules: List[str]
    custom_classes_source_modules: Optional[List[str]]
    condition_factory_mapping: Optional[Dict[str, str]]
    rules: Dict[str, Dict[str, Dict[pydantic.constr(to_upper=True), RulesConfig]]]  # type: ignore
    parsing_error_strategy: Optional[ParsingErrorStrategy]

    class Config:
        extra = "ignore"
