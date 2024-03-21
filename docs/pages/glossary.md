| Concept                | Definition                                                             |
| -----------            | ------------------------------------                                   |
| action                 | A task which is executed when conditions are verified.                 |
| action function        | A callable object called to execute the action.                        |
| action parameter       | Parameter of an action function.                                       |
| condition              | A condition to be verified before executing an action.                 |
| condition id           | Identifier of a single condition (must be in CAPITAL LETTER).          |
| condition expression   | A boolean expression combining several conditions (meaning several condition id).|
| condition function     | A callable object called to be verified therefore it returns a boolean.|
| condition parameter    | Parameter of a condition/validation function.                          |
| custom condition       | A user-defined condition.                                              |
| rule                   | A set of conditions combined to one action.                            |
| rule group             | A group of rules (usually sharing a common context).                   |
| rule id                | Identifier of a single rule.                                           |
| rule set               | A set of rule groups (mostly one: `default_rule_set`).                 |
| simple condition       | A built-in very simple condition.                                      |
| standard condition     | The regular built-in condition.                                        |
| validation function    | Same thing as a condition function.                                    |