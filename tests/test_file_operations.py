import os

import pypdf.errors
import pytest
from pypdf import PdfReader, PdfWriter

from pdf_form.file_operations import load_pdf, write_pdf_to_file, write_pdf_to_bytes

TEST_VALID_FILE = "test.pdf"
TEST_FILE_NOT_FOUND = "_test.pdf"
TEST_INVALID_FILE = "invalid.pdf_"
OUTPUT_FILE = "output.pdf"


@pytest.fixture
def output_path(test_data_path):
    return test_data_path / OUTPUT_FILE


@pytest.mark.parametrize(
    "filename", [TEST_VALID_FILE, TEST_FILE_NOT_FOUND, TEST_INVALID_FILE]
)
def test_load_file(test_data_path, filename):
    full_path = test_data_path / filename
    if filename == TEST_VALID_FILE:
        pdf = load_pdf(full_path)
    elif filename == TEST_FILE_NOT_FOUND:
        with pytest.raises(FileNotFoundError):
            pdf = load_pdf(full_path)
    elif filename == TEST_INVALID_FILE:
        with pytest.raises(pypdf.errors.EmptyFileError):
            pdf = load_pdf(full_path)


def test_write_pdf_reader_to_file(test_data_path, valid_pdf_path, output_path):
    pdf = PdfReader(valid_pdf_path)
    assert not os.path.exists(output_path)
    write_pdf_to_file(pdf, output_path)
    assert os.path.exists(output_path)
    os.remove(output_path)


def test_write_pdf_writer_to_file(test_data_path, valid_pdf_path, output_path):
    pdf = PdfWriter(valid_pdf_path)
    assert not os.path.exists(output_path)
    write_pdf_to_file(pdf, output_path)
    assert os.path.exists(output_path)
    os.remove(output_path)


def test_write_pdf_reader_to_bytes(valid_pdf_path):
    pdf = PdfReader(valid_pdf_path)
    pdf_b = write_pdf_to_bytes(pdf)
    assert isinstance(pdf_b, bytes)


def test_write_pdf_writer_to_bytes(valid_pdf_path):
    pdf = PdfWriter(valid_pdf_path)
    pdf_b = write_pdf_to_bytes(pdf)
    assert isinstance(pdf_b, bytes)
