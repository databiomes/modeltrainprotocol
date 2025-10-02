"""
Pytest configuration and shared fixtures for Model Train Protocol tests.
"""
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """
    Create a temporary directory for testing file operations.

    Yields:
        Path: Path to the temporary directory

    The directory is automatically cleaned up after the test.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
