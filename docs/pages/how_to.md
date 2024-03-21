Ensure that you have correctly installed **Arta** before, check the [Installation](installation.md) page :wrench:

## Hello World

You want a simple code to play with? Here it comes:

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

!!! abstract "API Documentation"

    You can get details on the `RulesEngine` parameters in the [API Reference](api_reference.md).

Have you read the [Get Started](in_a_nutshell.md) section? If not, you probably should before going further :smiley:

## Concepts

Let's go deeper into the previous code:

### Rule sets and rule groups

A **rule set** is composed of **rule groups** which are themselves composed of **rules**. We can find this tree structure in the following dictionary:

```python
rules = {  # (1)
    "check_admission": {  # (2)
        "ADMITTED_RULE": {  # (3)
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

1. This dictionary contains a *rule set*.
2. This key define a *rule group*, we can have many groups (we have only one here for simplicity).
3. This key is a *rule id*, which identifies *rules* among others.

### Rules

**Rules** are identified by an id or key (e.g., `ADMITTED_RULE`) and defined by a dictionary:

```python hl_lines="2-5"
"ADMITTED_RULE": {
    "condition": lambda power: power in ["strength", "fly", "immortality"],
    "condition_parameters": {"power": "input.super_power"}, 
    "action": set_admission,
    "action_parameters": {"value": True},
}
```

!!! tip

    Rule **ids** are in capital letters for readability only: it is an advised best practice.

**Rules** are made of 2 different things:

* Condition:

```python hl_lines="2 3"
{
    "condition": lambda power: power in ["strength", "fly", "immortality"],
    "condition_parameters": {"power": "input.super_power"}, 
    "action": set_admission,
    "action_parameters": {"value": True},
}
```

* Action: 

```python hl_lines="4 5"
{
    "condition": lambda power: power in ["strength", "fly", "immortality"],
    "condition_parameters": {"power": "input.super_power"}, 
    "action": set_admission,
    "action_parameters": {"value": True},
}
```

### Conditions and Actions

**Conditions** and **actions** are quite similar in terms of implementation but their goal is different.

Both are made of a *callable object* and *parameters*:

* Condition keys:
    * `condition`: a callable python object that returns a `bool`, we called this function the **validation function** (or *condition function*).
    * `condition_parameters`: a dictionary mapping the validation function's parameters with their correponding values.
* Action keys:
    * `action`: a callable python object that returns what you want (or does what you want such as: requesting an api, sending an email, etc.), we called this function the **action function**.
    * `action_parameters`: a dictionary mapping the action function's parameters with their correponding values.

!!! question "Does a condition could be something else than a function?"

    Actually yes, a `condition` can be a python function but you will learn later that it can also be a **condition expression** (i.e., a boolean expression combining different individual conditions).

!!! tip "Parameter's special syntax"

    As you can see in the previous code, the action and condition parameters can have a special syntax: 

        {"power": "input.super_power"}
    
    The string `input.super_power` is evaluated by the rules engine and it means *"fetch the key `super_power` in the input data"*. Keep reading, you will find out later.

## Configuration

In the [Hello World](#hello-world) section of this user guide, you learnt how to instanciate and use the *rules engine* with a dictionary **rule set**. It's the reason why you used the correponding parameter `rules_dict` for the instancation:

    eng = RulesEngine(rules_dict=rules)

But there is another way to define your rules: using a **configuration** (i.e., some configuration files). 

For real use cases, using configuration is way much more convenient than using a dictionary :+1:

!!! info "YAML"

    The built-in file format used by Arta for configuration is YAML.

!!! example "Enhancement proposal"

    We are thinking on a design that will allow custom configuration backend which will allow user-implemented loading of the configuration (e.g., you prefer using a JSON format). Stay tuned.

### YAML file

!!! tip "Simple Conditions"
    
    The following **YAML** example illustrates how to configure usual *standard conditions* but there is another and simpler way to do it by using a special feature: the [simple condition](special_conditions.md#simple-condition).

Create a YAML file and define your rules almost like you did with the dictionary `rules`. There is few differences that we will focus on later:

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

    You can split your configuration in multiple YAML files seamlessly in order to keep things clear. Example:
    
    * global.yaml => source modules
    * rules.yaml => rule definitions
    * conditions.yaml => condition definitions

    It's very convenient when you have a lot of different rules and conditions in your app.

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

As it was previously mentionned, the key `condition:` can take one **condition id** but also a **condition expression** (i.e., a boolean expression of condition ids) combining several conditions:

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

    In that example, you must define the 3 condition ids in the configuration:

    * HAS_SCHOOL_AUTHORIZED_POWER
    * SPEAKS_FRENCH
    * IS_EVIL

!!! tip 

    Use the **condition expressions** to keep things simple. Put your conditions in one expression as you can rather than creating several rules :wink:

### Implementing functions

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

You should get the same result as [previously](#hello-world) (dictionary version):

    {'check_admission': {'is_admitted': True}}

## To sum up

At this point you have learnt the regular use of an **Arta** rules engine and you have seen the two major ways of defining rules: 

* [Using a dictionary of rules](#hello-world).
* [Using a configuration file](#configuration) (or many).

!!! tip

    **How to choose between dictionary and configuration?**

    In most cases, you must choose the configuration way of defining your rules. You will improve your rules' maintainability a lot.
    In some cases like proof-of-concepts or Jupyter notebook works, you will probably be happy to use straightforward dictionaries.

**Arta** has plenty more features to discover. If you want to learn more, go to the next chapter: [Advanced User Guide](parameters.md).