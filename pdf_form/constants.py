from enum import Enum


class Markers(str, Enum):
    REMOVE = "__remove_annotation_from_pdf__"


class PdfDictKeys(str, Enum):
    ANNOTATION_KEY = "/Annot"
