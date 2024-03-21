"""Top-level __init__."""

from importlib.metadata import version

from arta._engine import RulesEngine
from arta.utils import ConditionExecutionError, RuleExecutionError

__all__ = ["RulesEngine", "ConditionExecutionError", "RuleExecutionError"]

__version__ = version("arta")
