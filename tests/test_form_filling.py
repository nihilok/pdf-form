import pytest

from pdf_form.file_operations import load_pdf
from pdf_form.form_filling import extract_field_names, extract_checkbox_values


@pytest.fixture
def simple_form_field_keys():
    return ['Given Name Text Box', 'Family Name Text Box', 'House nr Text Box', 'Address 2 Text Box', 'Postcode Text Box', 'Country Combo Box', 'Height Formatted Field', 'City Text Box', 'Driving License Check Box', 'Favourite Colour List Box', 'Language 1 Check Box', 'Language 2 Check Box', 'Language 3 Check Box', 'Language 4 Check Box', 'Language 5 Check Box', 'Gender List Box', 'Address 1 Text Box']



@pytest.fixture
def complex_form_field_keys():
    return ['topmostSubform[0].Page1[0].Last_Name_Family_Name[0]', 'topmostSubform[0].Page1[0].First_Name_Given_Name[0]', 'topmostSubform[0].Page1[0].Middle_Initial[0]', 'topmostSubform[0].Page1[0].Other_Last_Names_Used_if_any[0]', 'topmostSubform[0].Page1[0].Address_Street_Number_and_Name[0]', 'topmostSubform[0].Page1[0].Apt_Number[0]', 'topmostSubform[0].Page1[0].City_or_Town[0]', 'topmostSubform[0].Page1[0].ZIP_Code[0]', 'topmostSubform[0].Page1[0].Date_of_Birth_mmddyyyy[0]', 'topmostSubform[0].Page1[0].U\\.S\\._Social_Security_Number__First_3_Numbers_[0]', 'topmostSubform[0].Page1[0].U\\.S\\._Social_Security_Number__Next_2_numbers_[0]', 'topmostSubform[0].Page1[0].U\\.S\\._Social_Security_Number__Last_4_numbers_[0]', 'topmostSubform[0].Page1[0].U\\.S\\', 'topmostSubform[0].Page1[0].U\\', 'topmostSubform[0].Page1[0].Employees_Email_Address[0]', 'topmostSubform[0].Page1[0].Employees_Telephone_Number[0]', 'topmostSubform[0].Page1[0]._1\\._A_citizen_of_the_United_States[0]', 'topmostSubform[0].Page1[0]._1\\', 'topmostSubform[0].Page1[0]._2\\._A_noncitizen_national_of_the_United_States__See_instructions_[0]', 'topmostSubform[0].Page1[0]._2\\', 'topmostSubform[0].Page1[0]._3\\._A_lawful_permanent_resident__Alien_Registration_Number_USCIS_Number__[0]', 'topmostSubform[0].Page1[0]._3\\', 'topmostSubform[0].Page1[0].Alien_Registration_NumberUSCIS_Number_1[0]', 'topmostSubform[0].Page1[0]._4\\._An_alien_authorized_to_work_until__expiration_date__if_applicable__mmd_dd_yyyy__[0]', 'topmostSubform[0].Page1[0]._4\\', 'topmostSubform[0].Page1[0].expiration_date__if_applicable__mm_dd_yyyy[0]', 'topmostSubform[0].Page1[0]._1_Alien_Registration_NumberUSCIS_Number[0]', 'topmostSubform[0].Page1[0]._2_Form_I94_Admission_Number[0]', 'topmostSubform[0].Page1[0]._3_Foreign_Passport_Number[0]', 'topmostSubform[0].Page1[0].Country_of_Issuance[0]', 'topmostSubform[0].Page1[0].I_did_not_use_a_preparer_or_translator[0]', 'topmostSubform[0].Page1[0].A_preparer_s__and_or_translator_s__assisted_the_employee_in_completing_Section_1[0]', 'topmostSubform[0].Page1[0].Last_Name_Family_Name_2[0]', 'topmostSubform[0].Page1[0].First_Name_Given_Name_2[0]', 'topmostSubform[0].Page1[0].Address_Street_Number_and_Name_2[0]', 'topmostSubform[0].Page1[0].City_or_Town_2[0]', 'topmostSubform[0].Page1[0].Zip_Code[0]', 'topmostSubform[0].Page1[0].State[0]', 'topmostSubform[0].Page1[0].State[1]', 'topmostSubform[0].Page1[0]', 'topmostSubform[0].Page2[0].Last_Name_Family_Name_3[0]', 'topmostSubform[0].Page2[0].First_Name_Given_Name_3[0]', 'topmostSubform[0].Page2[0].MI[0]', 'topmostSubform[0].Page2[0].CitizenshipImmigration_Status[0]', 'topmostSubform[0].Page2[0].List_A_-_Document_Title_1[0]', 'topmostSubform[0].Page2[0].List_B_-_Document_Title[0]', 'topmostSubform[0].Page2[0].List_C_-_Document_Title[0]', 'topmostSubform[0].Page2[0].List_A_-_Issuing_Authority_1[0]', 'topmostSubform[0].Page2[0].List_B_-_Issuing_Authority[0]', 'topmostSubform[0].Page2[0].List_C_-_Issuing_Authority[0]', 'topmostSubform[0].Page2[0].List_A_-_Document_Number_1[0]', 'topmostSubform[0].Page2[0].List_B_-_Document_Number[0]', 'topmostSubform[0].Page2[0].List_C_-_Document_Number[0]', 'topmostSubform[0].Page2[0].List_A_-_Expiration_Date__if_any___mm_dd_yyyy__1[0]', 'topmostSubform[0].Page2[0].List_B_-_Expiration_Date__if_any___mm_dd_yyyy_[0]', 'topmostSubform[0].Page2[0].List_C_-_Expiration_Date__if_any___mm_dd_yyyy_[0]', 'topmostSubform[0].Page2[0].List_A_-_Document_Title_2[0]', 'topmostSubform[0].Page2[0].List_A_-_Issuing_Authority_2[0]', 'topmostSubform[0].Page2[0].List_A_-_Document_Number_2[0]', 'topmostSubform[0].Page2[0].List_A_-_Expiration_Date__if_any___mm_dd_yyyy__2[0]', 'topmostSubform[0].Page2[0].List_A_-_Document_Title_3[0]', 'topmostSubform[0].Page2[0].List_A_-_Issuing_Authority_3[0]', 'topmostSubform[0].Page2[0].List_A_-_Document_Number_3[0]', 'topmostSubform[0].Page2[0].List_A_-_Expiration_Date__if_any___mm_dd_yyyy__3[0]', 'topmostSubform[0].Page2[0].Additional_Information[0]', 'topmostSubform[0].Page2[0].Last_Name_of_Employer_or_Authorized_Representative[0]', 'topmostSubform[0].Page2[0].First_Name_of_Employer_or_Authorized_Representative[0]', 'topmostSubform[0].Page2[0].Employers_Business_or_Organization_Name[0]', 'topmostSubform[0].Page2[0].Employers_Business_or_Organization_Address_Street_Number_and_Name[0]', 'topmostSubform[0].Page2[0].City_or_Town_of_Employers_Business_or_Organization[0]', 'topmostSubform[0].Page2[0].Last_Name_Family_Name_4[0]', 'topmostSubform[0].Page2[0].First_Name_Given_Name_4[0]', 'topmostSubform[0].Page2[0].Middle_Initial_2[0]', 'topmostSubform[0].Page2[0].Date_mmddyyyy[0]', 'topmostSubform[0].Page2[0].Document_Title_4[0]', 'topmostSubform[0].Page2[0].Document_Number_6[0]', 'topmostSubform[0].Page2[0].Expiration_Date_if_any_mmddyyyy_6[0]', 'topmostSubform[0].Page2[0].Zip_Code_of_Employers_Business_or_Organization[0]', 'topmostSubform[0].Page2[0].textFieldEmployerTitle[0]', 'topmostSubform[0].Page2[0].textFieldEmployerName[0]', 'topmostSubform[0].Page2[0].State[0]', 'topmostSubform[0].Page2[0].The_employee_s_first_day_of_employment__mm_dd_yyyy_[0]', 'topmostSubform[0].Page2[0]', 'topmostSubform[0]']


@pytest.fixture
def complex_pdf_checkbox_values_dict():
    return {'_A_citizen_of_the_United_States[0]': ['/Off', '/Yes'], '_A_noncitizen_national_of_the_United_States__See_instructions_[0]': ['/Off', '/Yes'], '_A_lawful_permanent_resident__Alien_Registration_Number_USCIS_Number__[0]': ['/Off', '/Yes'], '_An_alien_authorized_to_work_until__expiration_date__if_applicable__mmd_dd_yyyy__[0]': ['/Off', '/Yes'], 'I_did_not_use_a_preparer_or_translator[0]': ['/Off', '/Yes'], 'A_preparer_s__and_or_translator_s__assisted_the_employee_in_completing_Section_1[0]': ['/Off', '/Yes']}


def test_extract_field_names_empty_pdf(valid_pdf_path):
    fields = extract_field_names(valid_pdf_path)
    assert fields == []


def test_extract_checkbox_values_empty_pdf(complex_form_path, complex_pdf_checkbox_values_dict):
    values = extract_checkbox_values(complex_form_path)
    assert values == complex_pdf_checkbox_values_dict


def test_pdf_get_fields(simple_form_path, simple_form_field_keys):
    pdf = load_pdf(simple_form_path)
    values = list(pdf.get_fields().keys())
    assert values == simple_form_field_keys


def test_pdf_get_fields_complex_form(complex_form_path, complex_form_field_keys):
    pdf = load_pdf(complex_form_path)
    values = list(pdf.get_fields().keys())
    assert values == complex_form_field_keys
