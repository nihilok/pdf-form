import os
import pytest
from pathlib import Path


@pytest.fixture
def tests_path():
    return Path(os.path.dirname(__file__))

