There is one main reason for using **Arta** and it was the main goal behind its development: 

> Increase business rules maintainability.

In other words, facilitate rules handling in a python app.


## Before Arta :spaghetti:

Rules in code can rapidly become a headache for developpers by their evolving into a hellish spaghetti of `if`, `elif` and `else` (or even `match/case` since Python 3.10).

## After Arta :sparkles:

**Arta** increases rules maintainability:

* By *standardizing* the definition of a rule. All rules are configured or defined the same way in a single place (or few).
* Rules are released from the code base, which is *less error-prone* and increases clarity.

!!! example "Improve collaboration"

    Reading python code vs reading YAML.
