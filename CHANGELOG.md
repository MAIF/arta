# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.11.0 - October, 2025

#### Features

* Add logs.

### Maintenance

* Use [uv](https://docs.astral.sh/uv/) in CI/CD (`uv.lock` voluntarily in `.gitignore`).

## 0.10.3 - July, 2025

### Fixes

* User extra arguments in `.apply_rules()` were not given to action and condition function implementations (#49).

### Documentation

* Improve :
    * [Value sharing](https://maif.github.io/arta/value_sharing/) page.

## 0.10.2 - July, 2025

### Fixes

* `kwargs` were mandatory for action functions used inside a *dictionary of rules* (#47). They are now optional.

## 0.10.1 - April, 2025

### Fixes

* Unintentional breaking change on the action function parameter `input_data` (now deprecated).

## 0.10.0 - April, 2025

### Features

* Ability to share values between validation and action functions (#7).
* The `kwargs` parameter of action functions is now optional (only mandatory if you need to access `input_data`).

### Documentation

* How to get input or output data inside an action function.

### Maintenance

* Enable Dependabot.

## 0.9.0 - December, 2024

### Features

* Add a new configuration setting for rule execution: `rule_activation_mode` (#38).

### Maintenance

* Compatibility with Python 3.13.
* Use true Pydantic V2 (or Pydantic V1) models (`DeprecationWarning` added about Pydantic V1).

> [!IMPORTANT]
> **Arta** + **Pydantic V1** + **Python 3.13** is not supported because Pydantic V1 is not supported for Python > 3.12 ([issue 9663](https://github.com/pydantic/pydantic/issues/9663)).

### Documentation

* New pages:
    * *Use your business objects*
    * *Rule activation mode*

### Breaking changes

* Because of using `StringConstraints` (w/ Pydantic V2) rather than `constr()`, we can't use plain `YES` or `NO` (YAML booleans) as rule ids anymore. Use `"YES"` or `"NO"` instead in your YAML file.

## 0.8.1 - September, 2024

### Fixes

* *Simple condition:* an error occurs (#31) when the field is of type `camelCase` or `PascalCase` (e.g., `input.streetNumber`, `input.StreetNumber`).

### Documentation

* Fixes of code in the [A Simple Example](https://maif.github.io/arta/a_simple_example/) page.

## 0.8.0 - July, 2024

### Features

* Add a new parameter `config_dict` in the `RulesEngine`'s constructor. It can be used when you have already loaded the YAML configuration in a dictionary and want to use it straightforward.
* Add a new parameter `ignored_rules` in the `apply_rules()` method. It can be used to easily disable a rule by its id.
* Split a rule set in two (or more) files (keep the rules organized by their file names [alphabetically sorted]).

### Fixes

* *Simple condition:* an error occurs when the right operand is a uppercase string (e.g., `input.text=="LABEL"`).

### Refactoring

* Function `sanitize_regex()` is converted to an instance method `get_sanitized_id()` of `BaseCondition` class.

## 0.7.1 - June, 2024

### Features

* Configure your rules in a YAML file or use a straightforward python dictionary.
* Use "[standard conditions](https://maif.github.io/arta/how_to/#standard-condition)" (YAML defined conditions) for flexibility.
* Use "[simple conditions](https://maif.github.io/arta/how_to/#simple-condition)" (one-liner conditions) for simplicity (beta feature).
* Use *math expressions* in "[simple conditions](https://maif.github.io/arta/how_to/#simple-condition)" (#25).
* Implement your own "[custom conditions](https://maif.github.io/arta/special_conditions/#custom-condition)" (python classes) for adaptability.
* Define your own parameter's [parsing strategy](https://maif.github.io/arta/parameters/#parsing-error) (raise, ignore, default value).
* Use many [rule sets](https://maif.github.io/arta/rule_sets/) as you need.

### Fixes

* You can now use *whitespaces* in a string within a *simple condition* (e.g., `input.text=="super hero"`) (#23).


## 0.7.0b* - April, 2024

*Beta release*

### Features

* Configure your rules in a YAML file or use a straightforward python dictionary.
* Use "[standard conditions](https://maif.github.io/arta/how_to/#standard-condition)" (YAML defined conditions) for flexibility.
* Use "[simple conditions](https://maif.github.io/arta/how_to/#simple-condition)" (one-liner conditions) for simplicity (beta feature).
* Implement your own "[custom conditions](https://maif.github.io/arta/special_conditions/#custom-condition)" (python classes) for adaptability.
* Define your own parameter's [parsing strategy](https://maif.github.io/arta/parameters/#parsing-error) (raise, ignore, default value).
* Use many [rule sets](https://maif.github.io/arta/rule_sets/) as you need.
