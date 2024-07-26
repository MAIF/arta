Ensure that you have correctly installed **Arta** before, check the [Installation](installation.md) page :wrench:

## Simple condition

!!! beta "Beta feature"

    **Simple condition** is still a *beta feature*, some cases could not work as designed.

**Simple conditions** are a new and straightforward way of configuring your *conditions*.

It simplifies your rules a lot by:

* Removing the use of a `conditions.py` module (no validation functions needed).
* Removing the `conditions`: configuration key in your YAML files.

!!! note

    With the **simple conditions** you use straight *boolean expressions* directly in your configuration.
    
    It is easier to read and maintain :+1:

The *configuration key* here is:

> `simple_condition:`

Example :

```yaml hl_lines="6 11 16"
---
rules:
  default_rule_set:
    admission:
      ADM_OK:
        simple_condition: input.power=="strength" or input.power=="fly"
        action: set_admission
        action_parameters:
          value: OK 
      ADM_TO_BE_CHECKED:
        simple_condition: input.age>=150 and input.age!=None
        action: set_admission
        action_parameters:
          value: TO_CHECK     
      ADM_KO:
        simple_condition: null
        action: set_admission
        action_parameters:
          value: KO

actions_source_modules:
  - my_folder.actions  # (1)
```

1. Contains *action function* implementations, no need of the key `conditions_source_modules` here.

How to write a simple condition like:

    input.power=="strength" or input.power=="fly"

* **Left operand (data mapping):** 
    * You must use one of the following prefixes: 
        * `input` (for input data)
        * `output` (for the previous rule's result)
    * A *dot path* expression like `input.powers.main_power`.
    * Even a *math expression* like: `input.x*input.y>input.threshold` *(but without any whitespaces)*.
* **Operator:** you must use basic python *boolean operator* (i.e., `==, <, >, <=, >=, !=`)
* **Right operand:** basic python data types (e.i., `str, int, float, None`) or a *dot path* expression (e.g., `input.threshold`).

!!! tip

    You can use simple **math expressions** in a *simple condition*:
    
    `simple_condition: input.x+input.y>input.threshold and input.x*input.y<123.4`

!!! warning "Warnings"

    * You can only use `+`, `-`, `*`, `/` as **math operators**.
    * You can't use `is` neither `in`, as a **boolean operator**.
    * Don't forget the *double quotes* `"` for **strings**.

!!! danger "Security concern"

    **Python code injection:**

    Because **Arta** is using the `eval()` built-in function to evaluate *simple conditions*:
    
    * **You should never let the user** being able of dynamically define a *simple condition* (in `simple_condition:` conf. key).
    * You should verify that **write permissions on the YAML files** are not allowed when your app is deployed.
    * You should implement **data validation** of your input data (e.g., with Pydantic).

## Standard condition

It is the first implemented way of using **Arta** and probably the most powerful.

The *configuration key* here is:

> `condition:`

!!! info "YAML"

    The built-in file format used by Arta for configuration is **YAML**.

!!! note "You don't like YAML?"

    The `config_dict` constructor's parameter of `RulesEngine` lets you give a regular python **dictionary** containing the parsed configuration. 
    
    Thereby, you can use *any file format* to save your configuration, just parse them in a dictionary and use it as an argument.

### YAML file

!!! tip "Simple Conditions"
    
    The following **YAML** example illustrates how to configure usual *standard conditions* but there is another and simpler way to do it by using a special feature: the [simple condition](#simple-condition).

Create a YAML file and define your rules like this:

```yaml hl_lines="6 16-26"
---
rules:
  default_rule_set:  # (1)
    check_admission:
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER  # (2)
        action: set_admission
        action_parameters:
          value: true
      DEFAULT_RULE:
        condition: null
        action: set_admission
        action_parameters:
          value: false

conditions:  # (3)
  HAS_SCHOOL_AUTHORIZED_POWER:
    description: "Does applicant have a school authorized power?"
    validation_function: has_authorized_super_power
    condition_parameters:
      power: input.super_power

conditions_source_modules:  # (4)
  - my_folder.conditions
actions_source_modules:  # (5)
  - my_folder.actions
```

1. This is the name of your **rule set** (i.e., `default_rule_set` is by default).
2. You can't set a callable object here so we need to use a **condition id**.
3. The conditions are identified by an **id** and defined here. The **validation function** is defined in a user's python module.
4. This is the path of the module where the **validation functions** are implemented (you must change it).
5. This is the path of the module where the **action functions** are implemented (you must change it).

!!! warning 

    **Condition ids** must be in capital letters here, it is mandatory (e.g., `HAS_SCHOOL_AUTHORIZED_POWER`).

!!! tip

    You can split your configuration in **multiple YAML files** seamlessly in order to keep things clear. Example:
    
    * *global.yaml* => source modules
    * *rules.yaml* => rules' definition
    * *conditions.yaml* => conditions' definition

    It's very convenient when you have a lot of different **rules** and **conditions** in your app.

    !!! tip "A tip in a tip"

        You can also split one **rule set** in many different files. Just keep in mind that the aggregation order of your rules will be done following an **alphabetical order of the file names**.

### Condition expression

In the above YAML, the following **condition expression** is intentionally very simple:

```yaml hl_lines="6"
---
rules:
  default_rule_set:
    check_admission:
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
        action: set_admission
        action_parameters:
          value: true
```

The key `condition:` can take one **condition id** but also a **condition expression** (i.e., a boolean expression of condition ids) combining several conditions:

```yaml hl_lines="6"
---
rules:
  default_rule_set:
    check_admission:
      ADMITTED_RULE:
        condition: (HAS_SCHOOL_AUTHORIZED_POWER or SPEAKS_FRENCH) and not(IS_EVIL)
        action: set_admission
        action_parameters:
          value: true
```

!!! warning

    In that example, you must define the 3 conditions in the configuration:

    * HAS_SCHOOL_AUTHORIZED_POWER
    * SPEAKS_FRENCH
    * IS_EVIL

!!! tip 

    Use the **condition expressions** to keep things simple. Put your conditions in one expression as you can rather than creating several rules :wink:

### Functions

We must create 2 modules:

* `conditions.py` -> implements the needed **validation functions**.
* `actions.py` -> implements the needed **action functions**.

!!! note

    Module names are arbitrary, you can choose what you want.

And implement our 2 needed validation and action functions (the one defined in the configuration file): 

**conditions.py**:

```python
def has_authorized_super_power(power):
    return power in ["strength", "fly", "immortality"]
```

**actions.py**:

```python
def set_admission(value, **kwargs):  # (1)
    return {"is_admitted": value}
```

1. `**kwargs` is mandatory here.

!!! warning

    Function name and parameters must be the same as the one configured in the YAML file.

### Usage

Once your configuration file and your functions are ready, you can use it very simply:

```python
from arta import RulesEngine

input_data = {
    "id": 1,
    "name": "Superman",
    "civilian_name": "Clark Kent",
    "age": None,
    "city": "Metropolis",
    "language": "french",
    "super_power": "fly",
    "favorite_meal": "Spinach",
    "secret_weakness": "Kryptonite",
    "weapons": [],
}

eng = RulesEngine(config_path="path/to/conf/dir")

result = eng.apply_rules(input_data)

print(result)
```

You should get:

> `{'check_admission': {'is_admitted': True}}`

!!! abstract "API Documentation"

    You can get details on the `RulesEngine` parameters in the [API Reference](api_reference.md).

## Concepts

Let's go deeper into the concepts.

### Rule set and rule group

A **rule set** is composed of **rule groups** which are themselves composed of **rules**. We can find this tree structure in the following YAML:

```yaml
---
rules:
  default_rule_set:  # (1)
    check_admission:  # (2)
      ADMITTED_RULE:  # (3)
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
```

1. This is the id of the *rule set*.
2. This key define a *rule group*, we can have many groups (we have only one here for simplicity).
3. This key is a *rule id*, which identifies *rules* among others.

### Rule

**Rule** definitions are identified by an id (e.g., `ADMITTED_RULE`):

```yaml hl_lines="2-5"
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
        action: set_admission
        action_parameters:
          value: true
```

!!! tip

    Rule **ids** are in capital letters for readability only: it is an advised practice.

**Rules** are made of 2 different things:

* Condition:

```yaml hl_lines="2"
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
        action: set_admission
        action_parameters:
          value: true
```

* Action: 

```yaml hl_lines="3-5"
      ADMITTED_RULE:
        condition: HAS_SCHOOL_AUTHORIZED_POWER
        action: set_admission
        action_parameters:
          value: true
```

### Condition and Action

**Conditions** and **actions** are quite similar in terms of implementation but their goals are different.

Both are made of a *callable object* and some *parameters*:

* **Condition keys:**

    * *`validation_function`: name of a callable python object that returns a `bool`, we called this function the *validation function* (or *condition function*).

    * `condition_parameters`: the validation function's arguments.

* **Action keys:**

    * `action`: name of a callable python object that returns what you want (or does what you want such as: requesting an api, sending an email, etc.), we called this function the *action function*.

    * `action_parameters`: the action function's arguments.

!!! tip "Parameter's special syntax"

    The action and condition **arguments** can have a special syntax: 

        condition_parameters:
          power: input.super_power
    
    The string `input.super_power` is evaluated by the rules engine and it means *"fetch the key `super_power` in the input data"*.

## Dictionary rules

**Rules** can be configured in a YAML file but they can also be defined by a regular dictionary:

=== "Without type hints"
    
    ```python    
    from arta import RulesEngine

    set_admission = lambda value, **kwargs: {"is_admitted": value}

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

    input_data = {
        "id": 1,
        "name": "Superman",
        "civilian_name": "Clark Kent",
        "age": None,
        "city": "Metropolis",
        "language": "french",
        "super_power": "fly",
        "favorite_meal": "Spinach",
        "secret_weakness": "Kryptonite",
        "weapons": [],
    }

    eng = RulesEngine(rules_dict=rules)

    result = eng.apply_rules(input_data)

    print(result)
    ```

=== "With type hints (>=3.9)"

    ```python   
    from typing import Any, Callable

    from arta import RulesEngine

    set_admission: Callable = lambda value, **kwargs: {"is_admitted": value}

    rules: dict[str, Any] = {
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

    input_data: dict[str, Any] = {
        "id": 1,
        "name": "Superman",
        "civilian_name": "Clark Kent",
        "age": None,
        "city": "Metropolis",
        "language": "french",
        "super_power": "fly",
        "favorite_meal": "Spinach",
        "secret_weakness": "Kryptonite",
        "weapons": [],
    }

    eng = RulesEngine(rules_dict=rules)

    result: dict[str, Any] = eng.apply_rules(input_data)

    print(result)
    ```

You should get:

    {'check_admission': {'is_admitted': True}}
    
!!! success
    Superman is admitted to the superhero school!

Well done! By executing this code you have:

1. Defined an **action function** (`set_admission`)
2. Defined a **rule set** (`rules`)
3. Used some **input data** (`input_data`)
4. Instanciated a **rules engine** (`RulesEngine`)
5. Applied the rules on the data and get some results (`.apply_rules()`)

!!! note

    In the code example we used some anonymous/lambda function for simplicity but it could be regular python functions as well.

!!! tip "YAML vs Dictionary"

    **How to choose between dictionary and configuration?**

    *In most cases, you must choose the configuration way of defining your rules.*
    
    You will improve your rules' maintainability a lot.
    In some cases like proof-of-concepts or Jupyter notebook works, you will probably be happy with straightforward dictionaries.

**Arta** has plenty more features to discover. If you want to learn more, go to the next chapter: [Advanced User Guide](parameters.md).