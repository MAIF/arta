"""Pydantic model implementations.

Note: Having no "from __future__ import annotations" here is wanted (pydantic compatibility).
"""

from typing import Any, Callable, Dict, List, Optional, Annotated

import pydantic
from pydantic.version import VERSION

from arta.utils import ParsingErrorStrategy


if not VERSION.startswith('1.'):
    # ----------------------------------
    # For instantiation using rules_dict
    class RuleRaw(pydantic.BaseModel):
        """Pydantic model for validating a rule."""

        condition: Optional[Callable]
        condition_parameters: Optional[Dict[str, Any]]
        action: Callable
        action_parameters: Optional[Dict[str, Any]]

        model_config = pydantic.ConfigDict(extra='forbid')


    class RulesGroup(pydantic.RootModel): # noqa
        """Pydantic model for validating a rules group."""

        root: Dict[str, RuleRaw]


    class RulesDict(pydantic.RootModel): # noqa
        """Pydantic model for validating rules dict instanciation."""

        root: Dict[str, RulesGroup]


    # ----------------------------------
    # For instantiation using config_path
    class Condition(pydantic.BaseModel):
        """Pydantic model for validating a condition."""

        description: str
        validation_function: str
        condition_parameters: Optional[Dict[str, Any]] = None


    class RulesConfig(pydantic.BaseModel):
        """Pydantic model for validating a rule group from config file."""

        condition: Optional[str] = None
        simple_condition: Optional[str] = None
        action: Annotated[str, pydantic.StringConstraints(to_lower=True)]  # type: ignore
        action_parameters: Optional[Any] = None

        model_config = pydantic.ConfigDict(extra='allow')

    class Configuration(pydantic.BaseModel):
        """Pydantic model for validating configuration files."""

        conditions: Optional[Dict[str, Condition]] = None
        conditions_source_modules: Optional[List[str]] = None
        actions_source_modules: List[str]
        custom_classes_source_modules: Optional[List[str]] = None
        condition_factory_mapping: Optional[Dict[str, str]] = None
        rules: Dict[str, Dict[str, Dict[str, RulesConfig]]]
        parsing_error_strategy: Optional[ParsingErrorStrategy] = None

        model_config = pydantic.ConfigDict(extra='ignore')

        @pydantic.field_validator('rules', mode='before') # noqa
        def upper_key(cls, vl): # noqa
            """ Validate and uppercase keys for RulesConfig """
            for k, v in vl.items():
                for kk, vv in v.items():
                    for key, rules in [*vv.items()]:
                        if key != str(key).upper():
                            del vl[k][kk][key]
                            vl[k][kk][str(key).upper()] = rules
            return vl

else:

    class BaseModelV2(pydantic.BaseModel):
        """Wrapper to expose missed methods used elsewhere in the code"""

        model_dump =  pydantic.BaseModel.dict  # noqa

        @classmethod
        def model_validate(cls, obj):  # noqa
            return cls.parse_obj(obj)  # noqa

    # ----------------------------------
    # For instantiation using rules_dict
    class RuleRaw(BaseModelV2):
        """Pydantic model for validating a rule."""

        condition: Optional[Callable]
        condition_parameters: Optional[Dict[str, Any]]
        action: Callable
        action_parameters: Optional[Dict[str, Any]]

        class Config:
            extra = "forbid"


    class RulesGroup(pydantic.BaseModel):  # noqa
        """Pydantic model for validating a rules group."""

        __root__: Dict[str, RuleRaw]  # noqa


    class RulesDict(BaseModelV2):  # noqa
        """Pydantic model for validating rules dict instanciation."""

        __root__: Dict[str, RulesGroup]  # noqa


    # ----------------------------------
    # For instantiation using config_path
    class Condition(BaseModelV2):
        """Pydantic model for validating a condition."""

        description: str
        validation_function: str
        condition_parameters: Optional[Dict[str, Any]]


    class RulesConfig(BaseModelV2):
        """Pydantic model for validating a rule group from config file."""

        condition: Optional[str]
        simple_condition: Optional[str]
        action: pydantic.constr(to_lower=True)  # type: ignore
        action_parameters: Optional[Any]

        class Config:
            extra = "allow"


    class Configuration(BaseModelV2):
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
