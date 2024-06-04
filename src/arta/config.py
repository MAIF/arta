"""Configuration handling module."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from omegaconf import DictConfig, ListConfig, OmegaConf


def load_config(config_dir_path: str) -> dict[str, Any]:
    """Load a configuration dictionary from all the yaml files in a given directory (and its subdirectories).

    Args:
        config_dir_path: Path to a directory containing YML files.
        prefix: Prefix for the rglob pattern.
        exclude_pattern: Regex pattern to exclude files.

    Returns:
        config: Loaded config dictionary.
    """
    conf_files: list[Path] = [f for patt in ["*.yml", "*.yaml"] for f in Path(config_dir_path).rglob(patt)]
    omega_config: DictConfig | ListConfig = OmegaConf.unsafe_merge(*[OmegaConf.load(file) for file in conf_files])

    config: dict[str, Any] = cast(dict[str, Any], OmegaConf.to_object(omega_config))

    return config
