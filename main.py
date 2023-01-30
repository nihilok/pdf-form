#!/usr/bin/env python3
import os
from pathlib import Path

from pypdf import PdfWriter

from pdf_form.file_operations import load_pdf, write_pdf_to_file
from pdf_form.form_filling import extract_checkbox_values, update_pdf_form_fields_from_dict, create_manual_dict

form_path = Path((os.path.dirname(__file__))) / "tests" / "test_data" / "i-9.pdf"


pdf = load_pdf(form_path)

fields = pdf.get_fields()
field_keys = fields.keys()
checkbox_values = extract_checkbox_values(form_path)
data = {}
for field in field_keys:
    data[field] = checkbox_values.get(field.split(".")[-1][0], "TEXT FIELD")
writer = PdfWriter()
writer.clone_document_from_reader(pdf)
for p in pdf.pages:
    writer.update_page_form_field_values(p, data)
# update_pdf_form_fields_from_dict(writer, data, True)
writer.set_need_appearances_writer()
write_pdf_to_file(writer, "output.pdf")
