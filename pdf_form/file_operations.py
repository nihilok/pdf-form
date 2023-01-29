import io
from pathlib import Path
from typing import Union

from pypdf import PdfReader, PdfWriter


GenericPdfType = Union[PdfReader, PdfWriter]


def load_pdf(filename: Union[str, Path]) -> PdfReader:
    return PdfReader(filename)


def _get_writer_from_pdf_object(pdf: GenericPdfType) -> PdfWriter:
    if isinstance(pdf, PdfReader):
        writer = PdfWriter()
        writer.clone_document_from_reader(pdf)
    elif isinstance(pdf, PdfWriter):
        writer = pdf
    else:
        raise TypeError("pdf must be a PdfReader or PdfWriter")
    return writer


def write_pdf_to_file(pdf: GenericPdfType, filename) -> None:
    writer = _get_writer_from_pdf_object(pdf)
    with open(filename, "wb") as f:
        writer.write(f)


def write_pdf_to_bytes(pdf: GenericPdfType) -> bytes:
    writer = _get_writer_from_pdf_object(pdf)
    with io.BytesIO() as buffer:
        writer.write(buffer)
        return buffer.getvalue()
