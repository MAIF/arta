"""Configuration handling module."""

from pathlib import Path
from typing import Any, Dict, List, Union, cast

from omegaconf import DictConfig, ListConfig, OmegaConf


def load_config(config_dir_path: str) -> Dict[str, Any]:
    """Load a configuration dictionary from all the yaml files in a given directory (and its subdirectories).

    Args:
        config_dir_path: Path to a directory containing YML files.
        prefix: Prefix for the rglob pattern.
        exclude_pattern: Regex pattern to exclude files.

    Returns:
        config: Loaded config dictionary.
    """
    conf_files: List[Path] = [f for patt in ["*.yml", "*.yaml"] for f in Path(config_dir_path).rglob(patt)]
    omega_config: Union[DictConfig, ListConfig] = OmegaConf.unsafe_merge(*[OmegaConf.load(file) for file in conf_files])

    config: Dict[str, Any] = cast(Dict[str, Any], OmegaConf.to_object(omega_config))

    return config
