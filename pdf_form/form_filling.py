import io
import re
import logging
import urllib.parse
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject, TextStringObject
from reportlab.lib.pagesizes import letter   # type: ignore
from reportlab.pdfgen import canvas  # type: ignore

from pdf_form.file_operations import load_pdf
from pdf_form.constants import Markers, PdfDictKeys


int_or_float = Union[int, float]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@dataclass
class DefaultSettings:
    font_name: str = "Helvetica"
    font_size: int = 8
    font_rgb: tuple[int_or_float, int_or_float, int_or_float] = (0, 0, 0.75)


DEFAULT_SETTINGS = DefaultSettings()


def manual_add_annotations(
    original_writer: PdfWriter,
    data_dict: dict[tuple[float, float, int], Optional[str]],
    page_size: tuple[float, float] = letter,
) -> PdfWriter:
    """
    Add text manually to a PDF at the given coordinates (bottom right coordinate of annotation rect).
    :param original_writer: PdfWriter object already containing pages from original PDF
    :param data_dict: dict of annotations to add to the PDF, key is tuple of coordinates: ``(x, y, page_index)``
    :param page_size: page size of original file
    :return: PdfWriter made from original, with annotations added to page(s) specified in data_dict
    """

    if not data_dict:
        return original_writer

    font_name = DEFAULT_SETTINGS.font_name
    font_size = DEFAULT_SETTINGS.font_size
    font_rgb = DEFAULT_SETTINGS.font_rgb

    pages = {x[2] for x in data_dict.keys()}
    page_map = {}
    for p in pages:
        packet = io.BytesIO()
        new_page = canvas.Canvas(packet, pagesize=page_size)
        for annotation_coords, annotation_text in data_dict.items():
            x, y, page_number = annotation_coords
            if page_number != p:
                continue
            if annotation_text is None:
                continue
            new_page.setFont(font_name, font_size)
            new_page.setFillColorRGB(*font_rgb)
            new_line_offset = font_size
            annotation_lines = annotation_text.split("\n")
            for i, line in enumerate(reversed(annotation_lines)):
                y = y + new_line_offset * i
                new_page.drawString(x, y, line)
        new_page.save()
        packet.seek(0)
        new_page_pdf_reader = PdfReader(packet)

        # get page from existing pdf object and merge appropriate page with pdf page created above
        page = original_writer.pages[p]
        try:
            page.merge_page(new_page_pdf_reader.pages[p])
        except IndexError:
            # no annotations were added, skip merge
            pass
        page_map[p] = page

    # add all pages including merged page(s) to output pdf
    output = PdfWriter()
    for i, looped_page in enumerate(original_writer.pages):
        if merged_page := page_map.get(i):
            output.add_page(merged_page)
            continue
        output.add_page(looped_page)
    output.set_need_appearances_writer()

    return output


def pdf_reader_to_writer(pdf_reader: PdfReader) -> PdfWriter:
    """Adds pages from a PdfReader object to a PdfWriter object."""
    pdf_writer = PdfWriter()
    pdf_writer.clone_document_from_reader(pdf_reader)
    return pdf_writer


def is_checkbox(annotation):
    """Returns True if the annotation type is a checkbox/radio button"""
    ft = annotation.get(PdfDictKeys.ANNOT_TYPE_KEY)
    if ft == "/Btn" or (annotation.get(PdfDictKeys.CHECKBOX_VALUE_KEY) is not None):
        return True


def is_text_field(annotation):
    ft = annotation.get(PdfDictKeys.ANNOT_TYPE_KEY)
    if ft == "/Tx":
        return True


def annotation_iter(writer):
    """Generator that returns only viable PDF annotations from PdfWriter object, and their /T key value (or 'key')"""
    for page_number, page in enumerate(writer.pages):
        logger.debug("PAGE: " + str(page_number))
        annotations = page.get(PdfDictKeys.ANNOTATION_KEY)
        if not annotations:
            logger.debug("No annotations")
            continue
        for annot in annotations.get_object() or []:
            annot = annot.get_object() or {}
            if not annot.get(PdfDictKeys.SUBTYPE_KEY) == PdfDictKeys.WIDGET_SUBTYPE:
                logger.debug("Annotation is not a Widget")
                continue

            key = annot.get(PdfDictKeys.FIELD_KEY)
            parent = annot.get(PdfDictKeys.PARENT_KEY)

            logger.debug(f"{key=}")

            if parent is not None and key is None:
                logger.debug("Getting parent key")
                parent = parent.get_object()
                key = parent.get(PdfDictKeys.FIELD_KEY)
                logger.debug(f"{key=}")
            yield annot, key, page_number


def field_iter(writer, fields):
    for annot, key, page_number in annotation_iter(writer):
        for field in fields.keys():
            if key == field:
                yield annot, field, page_number


def _set_read_only(annot, read_only=False):
    if read_only:
        annot.update({NameObject("/Ff"): NumberObject(1)})


def _pdf_encode(value: str):
    """
    PDF encoding uses url encoding but instead of "%", "#" is used, and spaces are not escaped/encoded.
    This function encodes with url encoding and replaces "+" with "#20" and "%" with "#". Pdf values are also
    prefixed with a forward slash (not url encoded).
    """
    if not value:
        return
    if value.startswith("/"):
        value = value[1:]
    value = urllib.parse.quote_plus(value)
    value = re.sub(r"\+", "#20", value)
    value = re.sub(r"%[a-zA-Z0-9]{2}", lambda match: f"#{match.group(0)[1:]}", value)
    return f"/{value}"


def _update_checkbox_value(annot, value, read_only=False):
    """
    Standardise and fill PDF checkboxes by field name
    """
    if value is None:
        return

    # ascertain positive checkbox value from annotation dict
    positive_value = list(
        filter(
            lambda x: _pdf_encode(value) == x,
            annot[PdfDictKeys.CHECKBOX_VALUES_KEY][PdfDictKeys.POSITIVE_VALUES_KEY].keys(),
        )
    )
    value = positive_value[0] if len(positive_value) else PdfDictKeys.NEGATIVE_VALUE

    # update annotation object
    annot.update(
        {
            NameObject(PdfDictKeys.TEXT_VALUE_KEY): NameObject(value),
            NameObject(PdfDictKeys.CHECKBOX_VALUE_KEY): NameObject(value),
        }
    )

    _set_read_only(annot, read_only)


def _update_form_field(annot, value, read_only=False):
    """Updates single annotation IndirectObject in a PyPDF2.PdfWriter object."""
    annot.update(
        {
            NameObject(PdfDictKeys.TEXT_VALUE_KEY.value): TextStringObject(value),
            NameObject("/DA"): TextStringObject(PdfDictKeys.PDF_DEFAULT_ANNOTATION_FONT.value)
        }
    )
    _set_read_only(annot, read_only)


def update_pdf_form_fields_from_dict(writer, data, read_only=False):
    """Update PDF AcroForm fields from a data dict"""
    for annot, field, _ in field_iter(writer, data):
        value = data[field]

        # if value is None, just set read_only flag
        if value is None:
            _set_read_only(annot, read_only)
            continue

        # check if we need to remove this annotation from the PDF
        elif value == Markers.REMOVE:
            annot.pop("/Rect", None)
            # hacky but works, with no /Rect key the annotation won't appear
            continue

        # fill text fields and checkboxes respectively
        if is_text_field(annot):
            _update_form_field(annot, value, read_only)
        elif is_checkbox(annot):
            _update_checkbox_value(annot, value, read_only)


def create_manual_dict(writer, data):
    data_by_coords = {}
    for annot, field, page in field_iter(writer, data):
        if is_text_field(annot):
            rect = annot.pop("/Rect", None)
            coords = tuple([float(r) for r in rect[:2]] + [page]) if rect else None
            if coords:
                print(coords, field)
                data_by_coords[coords] = data[field]
    return data_by_coords


def extract_field_names(pdf_file: Union[str, BytesIO, Path]):
    """
    For PDF analysis for both mapping of PDFs and on-the-fly filling of unmapped PDF AcroForms.
    Returns a list of field names (keys) used in given PDF file
    """
    fields = []
    reader = load_pdf(pdf_file)
    for _, key in annotation_iter(pdf_reader_to_writer(reader)):
        fields.append(key)
    return fields


def extract_checkbox_values(
    pdf_file: Union[str, BytesIO, Path]
) -> dict[str, list[str]]:
    """
    For analysis of PDF files for the purposes of mapping widget values to checkbox values.
    """
    checkbox_values: dict[str, list[str]] = {}
    if not isinstance(pdf_file, PdfReader):
        reader = load_pdf(pdf_file)
    else:
        reader = pdf_file
    for annot, key, _ in annotation_iter(pdf_reader_to_writer(reader)):
        if is_checkbox(annot):
            values = list(annot[PdfDictKeys.CHECKBOX_VALUES_KEY][PdfDictKeys.POSITIVE_VALUES_KEY].keys())
            try:
                key = annot[PdfDictKeys.FIELD_KEY]
            except KeyError:
                parent = annot[PdfDictKeys.PARENT_KEY]
                parent = parent.get_object()
                key = parent[PdfDictKeys.FIELD_KEY]
            if checkbox_values.get(key):
                checkbox_values[key].extend(values)
            else:
                checkbox_values[key] = values

    return checkbox_values
