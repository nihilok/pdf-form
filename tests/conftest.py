import os
import pytest
from pathlib import Path


@pytest.fixture
def tests_path():
    return Path(os.path.dirname(__file__))


@pytest.fixture
def test_data_path(tests_path):
    return tests_path / "test_data"


@pytest.fixture
def valid_pdf_path(test_data_path):
    return test_data_path / "test.pdf"


