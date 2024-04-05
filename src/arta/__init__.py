"""Top-level __init__."""

from importlib.metadata import version

from arta._engine import RulesEngine

__all__ = ["RulesEngine"]

__version__ = version("arta")
