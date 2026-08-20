import json
import os
import openpyxl
import pytest
from app.tools.excel_tools import _clean_json_string, validate_and_generate_excel


def test_clean_json_string():
    raw_json = '{"key": "value"}'
    markdown_json = '```json\n{"key": "value"}\n```'
    markdown_plain = '```\n{"key": "value"}\n```'
    
    assert _clean_json_string(raw_json) == raw_json
    assert _clean_json_string(markdown_json) == raw_json
    assert _clean_json_string(markdown_plain) == raw_json


def test_validate_and_generate_excel_valid(tmp_path):
    sample_data = {
        "product_info": {
            "title": "Test Smartphone Ultra",
            "brand": "TechCorp",
            "category": "Mobile Devices",
            "price": "999.99",
            "currency": "USD"
        },
        "universal_identifiers": {
            "gtin": "01234567890123",
            "upc": "123456789012",
            "ean": "1234567890123",
            "mpn": "TC-ULTRA-01",
            "vpn": "TC-ULTRA-01",
            "asin": "B00EXAMPLE",
            "unspsc": "43191501",
            "hs_code": "8517.12"
        },
        "specifications": {
            "display": "6.7 inch OLED",
            "ram": "12GB",
            "dimensions": {"width": 75, "height": 160}
        },
        "metadata": {
            "confidence_score": 0.95
        }
    }

    out_file = "test_output.xlsx"
    res = validate_and_generate_excel(json.dumps(sample_data), output_filename=out_file)

    assert res["status"] == "success"
    assert res["validation_passed"] is True
    assert len(res["missing_critical_fields"]) == 0
    assert "gtin" in res["verified_identifiers"]
    assert os.path.exists(res["output_file_path"])

    # Inspect created workbook
    wb = openpyxl.load_workbook(res["output_file_path"])
    assert "Product Overview & IDs" in wb.sheetnames
    assert "Full Specifications" in wb.sheetnames

    ws_summary = wb["Product Overview & IDs"]
    assert ws_summary["B3"].value == "Test Smartphone Ultra"
    assert ws_summary["B4"].value == "TechCorp"


def test_validate_and_generate_excel_missing_fields():
    sample_data = {
        "product_info": {
            "brand": "TechCorp"
        },
        "universal_identifiers": {
            "isbn": "978-3-16-148410-0"
        }
    }

    res = validate_and_generate_excel(json.dumps(sample_data))

    assert res["status"] == "success"
    assert res["validation_passed"] is False
    assert "product_title" in res["missing_critical_fields"]
    assert any("universal_identifiers" in field for field in res["missing_critical_fields"])


def test_validate_and_generate_excel_invalid_json():
    invalid_json_str = "{invalid json content"
    res = validate_and_generate_excel(invalid_json_str)

    assert res["status"] == "error"
    assert res["validation_passed"] is False
    assert "Failed to parse" in res["message"]
