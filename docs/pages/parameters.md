## Parsing prefix keywords

There is 2 allowed parsing **prefix keywords**:

* `input`: corresponding to the `input_data`.
* `output` : corresponding to the result output data (returned by the `apply_rules()` method).

Here are examples:

1. `input.name`: maps to `input_data["name"]`.
2. `output.check_admission.is_admitted`: maps to `result["check_admission"]["is_admitted"]`.

They both can be used in **condition and action parameters**.

!!! info

    A value without any prefix keyword is a constant.

## Parsing error

### Raise by default

By default, errors during *condition* and *action parameters* parsing are **raised**.

If we refer to the [dictionary](how_to.md#dictionary-rules) example:

```python hl_lines="5"
rules = {
    "check_admission": {
        "ADMITTED_RULE": {
            "condition": lambda power: power in ["strength", "fly", "immortality"],
            "condition_parameters": {"power": "input.super_power"}, 
            "action": set_admission,
            "action_parameters": {"value": True},
        },
        "DEFAULT_RULE": {
            "condition": None,
            "condition_parameters": None, 
            "action": set_admission,
            "action_parameters": {"value": False},
        },
    }
}
```

With modified data like:

```python hl_lines="8"
input_data = {
    "id": 1,
    "name": "Superman",
    "civilian_name": "Clark Kent",
    "age": None,
    "city": "Metropolis",
    "language": "french",
    "power": "fly",
    "favorite_meal": "Spinach",
    "secret_weakness": "Kryptonite",
    "weapons": [],
}
```

By default we will get a `KeyError` exception during the execution of the `apply_rules()` method because of `power` vs `super_power`.

### Ignore

You can change the by default raising behavior of the parameter's parsing.

Two ways are possible:

* At the configuration level: impacts all the **parameters**.
* At the **parameter**'s level. 


#### Configuration level

You just have to add the following key somewhere in your configuration:

```yaml hl_lines="28"
---
rules:
  default_rule_set:
    check_admission:
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
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

parsing_error_strategy: ignore  # (1)
```

1. `parsing_error_strategy` has two possible values: `raise` and `ignore`.

It will affect all the parameters.

#### Parameter level

!!! tip "Quick Sum Up"

    * `input.super_power?`: set the value to `None`
    * `input.super_power?no_power`: set the value to `no_power`
    * `input.super_power!`: force raise exception (case when ignore is set by default)

You can also handle more precisely that aspect at parameter's level:

```yaml  hl_lines="21"
---
rules:
  default_rule_set:
    check_admission:
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
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
      power: input.super_power?  # (1)

conditions_source_modules:
  - my_folder.conditions
actions_source_modules: 
  - my_folder.actions
```

1. Have you noticed the **'?'** ? If there is a `KeyError` when reading, `power` will be set to `None` rather than raising the exception.

!!! info

    You can enforce raising exceptions at parameter's level with `!`.
        
        power: input.super_power!

### Default value (parameter level)

Finally, you can set a default value at **parameter's level**. This value will be used if there is an exception during parsing:

```yaml  hl_lines="21"
---
rules:
  default_rule_set:
    check_admission:
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
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
      power: input.super_power?no_power  # (1)

conditions_source_modules:
  - my_folder.conditions
actions_source_modules: 
  - my_folder.actions
```

1. If there is an exception during parsing, `power` will be set to `"no_power"`.

!!! tip "Good to know"

    Parameter's level is overriding configuration level.
