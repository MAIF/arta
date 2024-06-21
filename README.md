<p align="center">
  <a href="https://maif.github.io/arta/"><img src="https://raw.githubusercontent.com/MAIF/arta/main/docs/pages/assets/img/arta-fond-clair.svg" alt="Arta" width="50%"></a>
</p>
<p align="center">
    <em>Make rule handling simple</em>
</p>
<p align="center">
  <img src="https://github.com/MAIF/arta/actions/workflows/ci-cd.yml/badge.svg?branch=main" alt="CI">
  <img src="https://img.shields.io/badge/coverage-97%25-dark_green" alt="Coverage">
  <img src="https://img.shields.io/pypi/v/arta" alt="Versions">
  <img src="https://img.shields.io/pypi/pyversions/arta" alt="Python">
  <img src="https://img.shields.io/pypi/dm/arta" alt="Downloads">
</p>

---

**Documentation:** [https://maif.github.io/arta/home/](https://maif.github.io/arta/home/)

**Repository:** [https://github.com/MAIF/arta](https://github.com/MAIF/arta)

---

## Overview

**Arta** is a simple python rules engine designed for python developers.

### Goal

There is one main reason for using **Arta** and it was the main goal behind its development at *MAIF*: increase business rules maintainability.

In other words, facilitate rules handling in our python apps.

### Origins

The need of a python *rules engine* emerged when we were working on a new major release of our internal use of [Melusine](https://github.com/maif/melusine) (i.e., email qualification pipeline with ML capabilities).

We were looking for a python library to *centralize, manage and standardize* all the implemented **business rules** we had but didn't find the perfect fit. 

Therefore, we decided to create this package and by extension of the MAIF's values, we planned to share it to the community.

### Features

* Standardize the definition of a rule. All rules are defined the same way in a unique place.
* Rules are released from the code base, which is less error prone and increases clearness.
* Use **Arta** whatever your field is.
* Great combination with Machine Learning: groups all the deterministic rules of your ML projects.

### A Simple Example

Create the three following files and run the `main.py` script (`python main.py` or `python3 main.py`).

`rules.yaml` :

```yaml
---
rules:
  default_rule_set:
    admission:
      ADMITTED:
        simple_condition: input.power=="strength" or input.power=="fly"
        action: set_admission
        action_parameters:
          value: true  
      NOT_ADMITTED:
        simple_condition: null
        action: set_admission
        action_parameters:
          value: false

actions_source_modules:
  - actions
```

`actions.py` :

```python
from typing import Any


def set_admission(value: bool, **kwargs: Any) -> dict[str, bool]:
    """Return a dictionary containing the admission result."""
    return {"is_admitted": value}
```

`main.py` :

```python
from arta import RulesEngine

eng = RulesEngine(config_path=".")

data = {
        "id": 1,
        "name": "Superman",
        "civilian_name": "Clark Kent",
        "age": None,
        "city": "Metropolis",
        "language": "english",
        "power": "fly",
        "favorite_meal": "Spinach",
        "secret_weakness": "Kryptonite",
        }

result = eng.apply_rules(input_data=data)

print(result)
```

You should get: `{"admission": {"is_admitted": True}}`

Check the [A Simple Example](https://maif.github.io/arta/a_simple_example/) section for more details.

## Installation

Install using `pip install -U arta`. See the [Install](https://maif.github.io/arta/installation/) section in the documentation for more details.

## What's New

Want to see last updates, check the [Release Notes](https://github.com/MAIF/arta/releases) or the [Changelog](./CHANGELOG.md).

## Community

You can discuss and ask *Arta* related questions:

- Issue tracker: [![github: MAIF/arta/issues](https://img.shields.io/github/issues/MAIF/arta.svg)](https://github.com/MAIF/arta/issues)
- Pull request: [![github: MAIF/arta/pulls](https://img.shields.io/github/issues-pr/MAIF/arta.svg)](https://github.com/MAIF/arta/pulls)

## Contributing

Contributions are *very* welcome!

If you see an issue that you'd like to see fixed, the best way to make it happen is to help out by submitting a pull request implementing it.

Refer to the [CONTRIBUTING.md](./CONTRIBUTING.md) file for more details about the workflow,
and general hints on how to prepare your pull request. You can also ask for clarifications or guidance in GitHub issues directly.

## License

This project is Open Source and available under the Apache 2 License.

[![Alt MAIF Logo](https://static.maif.fr/resources/img/logo-maif.svg)](https://www.maif.fr/)

