import os
import pytest
from pathlib import Path


@pytest.fixture
def tests_path():
    return Path(os.path.dirname(__file__))


@pytest.fixture
def test_data_path(tests_path):
    return tests_path / "test_data"

