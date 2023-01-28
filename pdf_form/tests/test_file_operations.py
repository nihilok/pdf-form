import os

import pypdf.errors
import pytest
from pypdf import PdfReader, PdfWriter

from pdf_form.file_operations import load_pdf, write_pdf_to_file, write_pdf_to_bytes

TEST_VALID_FILE = "test.pdf"
TEST_FILE_NOT_FOUND = "_test.pdf"
TEST_INVALID_FILE = "invalid.pdf_"
OUTPUT_FILE = "output.pdf"


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
    elif filename == TEST_INVALID_FILE:
        with pytest.raises(pypdf.errors.EmptyFileError):
            pdf = load_pdf(full_path)


def test_write_pdf_reader_to_file(tests_path):
    pdf = PdfReader(tests_path / TEST_VALID_FILE)
    assert not os.path.exists(tests_path / OUTPUT_FILE)
    write_pdf_to_file(pdf, tests_path / OUTPUT_FILE)
    assert os.path.exists(tests_path / OUTPUT_FILE)
    os.remove(tests_path / OUTPUT_FILE)


def test_write_pdf_writer_to_file(tests_path):
    pdf = PdfWriter(tests_path / TEST_VALID_FILE)
    pdf_b = write_pdf_to_bytes(pdf)
    assert isinstance(pdf_b, bytes)
