import pytest

from pdf_form.file_operations import load_pdf, write_pdf

TEST_VALID_FILE = "test.pdf"
TEST_FILE_NOT_FOUND = "_test.pdf"
TEST_INVALID_FILE = "invalid.pdf"


@pytest.mark.parametrize(
    "filename", [TEST_VALID_FILE, TEST_FILE_NOT_FOUND, TEST_INVALID_FILE]
)
def test_load_file(tests_path, filename):
    full_path = tests_path / filename
    if filename == TEST_VALID_FILE:
        pdf = load_pdf(full_path)
    elif filename == TEST_FILE_NOT_FOUND:
        with pytest.raises(FileNotFoundError):
            pdf = load_pdf(full_path)
    else:
        with pytest.raises(Exception):
            pdf = load_pdf(full_path)
