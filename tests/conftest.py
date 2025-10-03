"""
Pytest configuration and shared fixtures for Model Train Protocol tests.
"""
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Import all individual fixtures so they're available to all tests
from tests.fixtures.tokensets import *
from tests.fixtures.samples import *
from tests.fixtures.instructions import *
from tests.fixtures.comprehensive_instructions import *
from tests.fixtures.protocol_workflow_instructions import *
from tests.fixtures.workflow_context_instructions import *
from tests.fixtures.tokens import *
from tests.fixtures.protocol_fixtures import *
from tests.fixtures.guardrails import *


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
