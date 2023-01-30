from enum import Enum


class Markers(str, Enum):
    REMOVE = "__remove_annotation_from_pdf__"


class PdfDictKeys(str, Enum):
    ANNOTATION_KEY = "/Annots"
    FIELD_KEY = "/T"
    CHECKBOX_VALUES_KEY = "/AP"
    POSITIVE_VALUES_KEY = "/N"
    PARENT_KEY = "/Parent"
    NEGATIVE_VALUE = "/Off"
    SUBTYPE_KEY = "/Subtype"
    WIDGET_SUBTYPE = "/Widget"
    ANNOT_TYPE_KEY = "/FT"
    CHECKBOX_VALUE_KEY = "/AS"
    TEXT_VALUE_KEY = "/V"
    PDF_DEFAULT_ANNOTATION_FONT = "Helv 10 Tf 0 0 0.75 rg"
