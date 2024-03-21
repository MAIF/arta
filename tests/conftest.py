"""Setup tests and fixtures"""

import os

import pytest


@pytest.fixture(scope="session")
def base_config_path() -> str:
    """Dynamic config path base for tests."""
    current_dir_path: str = os.path.dirname(__file__)
    return os.path.join(current_dir_path, "examples")
