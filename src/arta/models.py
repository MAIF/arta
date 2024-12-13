"""Pydantic model implementations."""

from __future__ import annotations

from typing import Annotated, Any, Callable, Optional
from warnings import warn

import pydantic
from pydantic.version import VERSION

from arta.utils import ParsingErrorStrategy, RuleActivationMode

PYDANTIC_V1: bool = VERSION.startswith("1.")

if not PYDANTIC_V1:
    # Pydantic V2

    # ----------------------------------
    # For instantiation using rules_dict
    class RuleRaw(pydantic.BaseModel):
        """Pydantic model for validating a rule."""

        condition: Optional[Callable] = None
        condition_parameters: Optional[dict[str, Any]] = None
        action: Callable
        action_parameters: Optional[dict[str, Any]] = None

        model_config = pydantic.ConfigDict(extra="forbid")

    class RulesGroup(pydantic.RootModel):
        """Pydantic model for validating a rules group."""

        root: dict[str, RuleRaw]

    class RulesDict(pydantic.RootModel):
        """Pydantic model for validating rules dict instanciation."""

        root: dict[str, RulesGroup]

    # ----------------------------------
    # For instantiation using config_path
    class Condition(pydantic.BaseModel):
        """Pydantic model for validating a condition."""

        description: str
        validation_function: str
        condition_parameters: Optional[dict[str, Any]] = None

    class RulesConfig(pydantic.BaseModel):
        """Pydantic model for validating a rule group from config file."""

        condition: Optional[str] = None
        simple_condition: Optional[str] = None
        action: Annotated[str, pydantic.StringConstraints(to_lower=True)]
        action_parameters: Optional[Any] = None

        model_config = pydantic.ConfigDict(extra="allow")

    class Configuration(pydantic.BaseModel):
        """Pydantic model for validating configuration files."""

        conditions: Optional[dict[str, Condition]] = None
        conditions_source_modules: Optional[list[str]] = None
        actions_source_modules: list[str]
        custom_classes_source_modules: Optional[list[str]] = None
        condition_factory_mapping: Optional[dict[str, str]] = None
        rules: dict[str, dict[str, dict[Annotated[str, pydantic.StringConstraints(to_upper=True)], RulesConfig]]]
        parsing_error_strategy: Optional[ParsingErrorStrategy] = None
        rule_activation_mode: Optional[RuleActivationMode] = None

else:
    # Pydantic V1

    warn(
        (
            "Soon, Pydantic V1 will no longer be compatible with Arta. "
            "Please, migrate to Pydantic V2 (https://docs.pydantic.dev/latest/migration/)."
        ),
        DeprecationWarning,
        stacklevel=2,
    )

    class BaseModelV2(pydantic.BaseModel):
        """Wrapper to expose missed methods used elsewhere in the code"""

        model_dump: Callable = pydantic.BaseModel.dict

        @classmethod
        def model_validate(cls, obj):
            """Method mapping between V1 to V2."""
            return cls.parse_obj(obj)

    # ----------------------------------
    # For instantiation using rules_dict
    class RuleRaw(BaseModelV2):  # type: ignore[no-redef]
        """Pydantic model for validating a rule."""

        condition: Optional[Callable]
        condition_parameters: Optional[dict[str, Any]]
        action: Callable
        action_parameters: Optional[dict[str, Any]]

        class Config:
            extra = "forbid"

    class RulesGroup(pydantic.BaseModel):  # type: ignore[no-redef]
        """Pydantic model for validating a rules group."""

        __root__: dict[str, RuleRaw]

    class RulesDict(BaseModelV2):  # type: ignore[no-redef]
        """Pydantic model for validating rules dict instanciation."""

        __root__: dict[str, RulesGroup]

    # ----------------------------------
    # For instantiation using config_path
    class Condition(BaseModelV2):  # type: ignore[no-redef]
        """Pydantic model for validating a condition."""

        description: str
        validation_function: str
        condition_parameters: Optional[dict[str, Any]]

    class RulesConfig(BaseModelV2):  # type: ignore[no-redef]
        """Pydantic model for validating a rule group from config file."""

        condition: Optional[str]
        simple_condition: Optional[str]
        action: pydantic.constr(to_lower=True)  # type: ignore
        action_parameters: Optional[Any]

        class Config:
            extra = "allow"

    class Configuration(BaseModelV2):  # type: ignore[no-redef]
        """Pydantic model for validating configuration files."""

        conditions: Optional[dict[str, Condition]]
        conditions_source_modules: Optional[list[str]]
        actions_source_modules: list[str]
        custom_classes_source_modules: Optional[list[str]]
        condition_factory_mapping: Optional[dict[str, str]]
        rules: dict[str, dict[str, dict[pydantic.constr(to_upper=True), RulesConfig]]]  # type: ignore
        parsing_error_strategy: Optional[ParsingErrorStrategy] = None
        rule_activation_mode: Optional[RuleActivationMode] = None
