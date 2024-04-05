"""Custom exceptions."""


class RuleExecutionError(Exception):
    """Rule fails during its execution."""

    pass


class ConditionExecutionError(Exception):
    """Condition fails during its execution."""

    pass
