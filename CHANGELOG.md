# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.2] - November, 2024

### Maintenance

* Use true Pydantic V2 (or Pydantic V1) models (`DeprecationWarning` added about Pydantic V1).

### Documentation

* New page: *"Use your business objects".*

### Breaking changes

* Because of using `StringConstraints` (w/ Pydantic V2) rather than `constr()`, we can't use plain `YES` or `NO` (YAML booleans) as rule ids anymore. Use `"YES"` or `"NO"` instead in your YAML file.

## [0.8.1] - September, 2024

### Fixes

* *Simple condition:* an error occurs (#31) when the field is of type `camelCase` or `PascalCase` (e.g., `input.streetNumber`, `input.StreetNumber`).

### Documentation

* Fixes of code in the [A Simple Example](https://maif.github.io/arta/a_simple_example/) page.

## [0.8.0] - July, 2024

### Features

* Add a new parameter `config_dict` in the `RulesEngine`'s constructor. It can be used when you have already loaded the YAML configuration in a dictionary and want to use it straightforward.
* Add a new parameter `ignored_rules` in the `apply_rules()` method. It can be used to easily disable a rule by its id.
* Split a rule set in two (or more) files (keep the rules organized by their file names [alphabetically sorted]).

### Fixes

* *Simple condition:* an error occurs when the right operand is a uppercase string (e.g., `input.text=="LABEL"`).

### Refactoring

* Function `sanitize_regex()` is converted to an instance method `get_sanitized_id()` of `BaseCondition` class.

## [0.7.1] - June, 2024

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


## [0.7.0b*] - April, 2024

*Beta release*

### Features

* Configure your rules in a YAML file or use a straightforward python dictionary.
* Use "[standard conditions](https://maif.github.io/arta/how_to/#standard-condition)" (YAML defined conditions) for flexibility.
* Use "[simple conditions](https://maif.github.io/arta/how_to/#simple-condition)" (one-liner conditions) for simplicity (beta feature).
* Implement your own "[custom conditions](https://maif.github.io/arta/special_conditions/#custom-condition)" (python classes) for adaptability.
* Define your own parameter's [parsing strategy](https://maif.github.io/arta/parameters/#parsing-error) (raise, ignore, default value).
* Use many [rule sets](https://maif.github.io/arta/rule_sets/) as you need.
