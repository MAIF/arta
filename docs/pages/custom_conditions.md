**Custom conditions** are user-defined conditions. 

A **custom condition** will impact the atomic evaluation of each **conditions** (i.e., condition ids).

!!! warning "Vocabulary"

    To be more precise, a **condition expression** is something like:

        CONDITION_1 and CONDITION_2
    
    In that example, the condition expression is made of 2 **conditions** whose **condition ids** are:

    * CONDITION_1
    * CONDITION_2
    
With the built-in condition (also named *standard condition*), **condition ids** map to **validation functions** and **condition parameters** but we can change that with a brand new custom condition.

A custom condition example:

    my_condition: NAME_JOHN and AGE_42

!!! note "Remember"

    *condition ids* have to be in CAPITAL LETTERS.

Imagine you want it to be interpreted as (pseudo-code):

```python
if input.name == "john" and input.age == "42":
    # Do something
    ...
```

With the **custom conditions** it's quite simple to implement.

!!! question "Why use a custom condition?"

    The main goal is to simplify handling of recurrent conditions (e.i., "recurrent" meaning very similar conditions).

## Class implementation

First, create a class inheriting from `BaseCondtion` and implement the `verify()` method as you want/need:

```python
from typing import Any

from arta.condition import BaseCondition
from arta.utils import ParsingErrorStrategy


class MyCondition(BaseCondition):
    def verify(
        self,
        input_data: dict[str, Any],
        parsing_error_strategy: ParsingErrorStrategy,
        **kwargs: Any
    ) -> bool:

        field, value = tuple(self.condition_id.split("_"))

        return input_data[field.lower()] == value.lower()
```

!!! example "self.condition_id"

    `self.condition_id` will be `NAME_JOHN` for the first condition and `AGE_42` for the second.

!!! info "Good to know"

    The `parsing_error_strategy` can be used by the developer to adapt exception handling behavior. Possible values:

        ParsingErrorStrategy.RAISE
        ParsingErrorStrategy.IGNORE
        ParsingErrorStrategy.DEFAULT_VALUE

## Configuration

Last thing to do is to add your new **custom condition** in the configuration:

```yaml hl_lines="7 29-32"
---
rules:
  default_rule_set:
    check_admission:
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
        my_condition: NAME_JOHN and AGE_42  # (1)
        action: set_admission
        action_parameters:
          value: true
      DEFAULT_RULE:
        condition: null
        action: set_admission
        action_parameters:
          value: false

conditions:
  HAS_SCHOOL_AUTHORIZED_POWER:
    description: "Does applicant have a school authorized power?"
    validation_function: has_authorized_super_power
    condition_parameters:
      power: input.super_power

conditions_source_modules:
  - my_folder.conditions
actions_source_modules: 
  - my_folder.actions

custom_classes_source_modules:
  - dir.to.my_module  # (2)
condition_factory_mapping:
  my_condition: MyCondition # (3)
```

1. Order is important, here it will evaluate `condition` then `my_condition`. Order is arbitrary.
2. List of the modules containing custom classes
3. Mapping between condition keys (`my_condition`) and custom classes (`MyCondition`)

## Class diagram

It is based on the following *strategy pattern*:

```mermaid
classDiagram
    note for MyCondition "This is a custom condition class"
    RulesEngine "1" -- "1..*" Rule
    Rule "1..*" -- "0..*" BaseCondition
    BaseCondition <|-- StandardCondition
    BaseCondition <|-- SimpleCondition
    BaseCondition <|-- MyCondition
    class RulesEngine{
        +rules
        +apply_rules()
    }
    class Rule {
        #set_id
        #group_id
        #rule_id
        #condition_exprs
        #action
        #action_parameters
        +apply()
    }
    class BaseCondition {
        <<abstract>>
        #condition_id
        #description
        #validation_function
        #validation_function_parameters
        +CONDITION_DATA_LABEL$
        +CONDITION_ID_PATTERN$
        +verify()*
        +get_sanitized_id()
        +extract_condition_ids_from_expression()$
    }
    class StandardCondition {
      +CONDITION_DATA_LABEL$
      +verify()
    }
    class SimpleCondition {
      +CONDITION_DATA_LABEL$
      +CONDITION_ID_PATTERN$
      +verify()
      +get_sanitized_id()
    }
    class MyCondition {
      +verify()
    }
```

!!! info "Good to know"

    The class `StandardCondition` is the built-in implementation of a condition.
