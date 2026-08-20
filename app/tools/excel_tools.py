import json
import os
import re
from typing import Any, Dict, List, Optional
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from google.adk.tools import ToolContext

MANDATORY_IDENTIFIERS = ["gtin", "upc", "ean", "mpn", "vpn", "asin"]

def _clean_json_string(json_str: str) -> str:
    """Extracts raw JSON content if wrapped in markdown code blocks."""
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", json_str, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return json_str.strip()


def validate_and_generate_excel(
    product_data_json: str,
    output_filename: str = "product_spec.xlsx",
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Validates product specification JSON data and generates a styled Excel (.xlsx) file.

    Args:
        product_data_json: JSON string containing the product specifications and universal IDs.
        output_filename: Name of the output Excel file.

    Returns:
        A dictionary with validation status, missing fields, and generated file path.
    """
    cleaned_json = _clean_json_string(product_data_json)
    try:
        data = json.loads(cleaned_json)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to parse product JSON: {str(e)}",
            "validation_passed": False,
        }

    # Extract sections
    product_info = data.get("product_info", data.get("product", data))
    identifiers = data.get("universal_identifiers", data.get("identifiers", {}))
    specifications = data.get("specifications", data.get("attributes", {}))
    metadata = data.get("metadata", {})

    # Validation check
    found_ids = {k.lower(): v for k, v in identifiers.items() if v and str(v).strip()}
    has_at_least_one_id = any(k in found_ids for k in MANDATORY_IDENTIFIERS)
    
    missing_critical = []
    if not product_info.get("title") and not product_info.get("name"):
        missing_critical.append("product_title")
    if not has_at_least_one_id:
        missing_critical.append("universal_identifiers (at least one of GTIN, UPC, EAN, MPN, VPN, ASIN required)")

    validation_passed = len(missing_critical) == 0

    # Create Excel Workbook
    wb = openpyxl.Workbook()
    ws_summary = wb.active
    ws_summary.title = "Product Overview & IDs"
    ws_specs = wb.create_sheet(title="Full Specifications")

    # Styling Palette
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    sub_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    accent_fill = PatternFill(start_color="F2F2F2", fill_type="solid")
    white_bold = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    navy_bold = Font(name="Calibri", size=11, bold=True, color="1F4E79")
    title_font = Font(name="Calibri", size=14, bold=True, color="1F4E79")
    regular_font = Font(name="Calibri", size=11)
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    # --- Sheet 1: Product Overview & Universal Identifiers ---
    ws_summary["A1"] = "UNIVERSAL PRODUCT SPECIFICATION SHEET"
    ws_summary["A1"].font = title_font
    
    # Section 1: Core Info
    ws_summary["A3"] = "Product Title:"
    ws_summary["A3"].font = navy_bold
    ws_summary["B3"] = product_info.get("title") or product_info.get("name") or "N/A"
    ws_summary["B3"].font = regular_font

    ws_summary["A4"] = "Brand:"
    ws_summary["A4"].font = navy_bold
    ws_summary["B4"] = product_info.get("brand") or "N/A"
    ws_summary["B4"].font = regular_font

    ws_summary["A5"] = "Category:"
    ws_summary["A5"].font = navy_bold
    ws_summary["B5"] = product_info.get("category") or "N/A"
    ws_summary["B5"].font = regular_font

    ws_summary["A6"] = "Price / Currency:"
    ws_summary["A6"].font = navy_bold
    ws_summary["B6"] = f"{product_info.get('price', 'N/A')} {product_info.get('currency', 'USD')}"
    ws_summary["B6"].font = regular_font

    # Section 2: Universal Identifiers Table
    ws_summary["A8"] = "Identifier Type"
    ws_summary["B8"] = "Value"
    ws_summary["C8"] = "Status"

    for col in ["A8", "B8", "C8"]:
        ws_summary[col].fill = header_fill
        ws_summary[col].font = white_bold
        ws_summary[col].alignment = Alignment(horizontal="center")

    id_types = [
        ("GTIN-14", identifiers.get("gtin") or identifiers.get("gtin14")),
        ("UPC-12", identifiers.get("upc")),
        ("EAN-13", identifiers.get("ean")),
        ("MPN / VPN", identifiers.get("mpn") or identifiers.get("vpn")),
        ("ASIN", identifiers.get("asin")),
        ("UNSPSC Code", identifiers.get("unspsc")),
        ("HS Code", identifiers.get("hs_code")),
        ("ISBN", identifiers.get("isbn")),
    ]

    row_idx = 9
    for id_name, val in id_types:
        status = "VERIFIED" if val else "MISSING"
        ws_summary[f"A{row_idx}"] = id_name
        ws_summary[f"B{row_idx}"] = str(val) if val else "N/A"
        ws_summary[f"C{row_idx}"] = status

        ws_summary[f"A{row_idx}"].font = navy_bold
        ws_summary[f"B{row_idx}"].font = regular_font
        ws_summary[f"C{row_idx}"].font = Font(name="Calibri", size=11, bold=True, color="008000" if val else "C00000")

        for col_letter in ["A", "B", "C"]:
            ws_summary[f"{col_letter}{row_idx}"].border = thin_border
        row_idx += 1

    # --- Sheet 2: Technical Specifications ---
    ws_specs["A1"] = "Attribute Name"
    ws_specs["B1"] = "Attribute Value"
    ws_specs["A1"].fill = header_fill
    ws_specs["B1"].fill = header_fill
    ws_specs["A1"].font = white_bold
    ws_specs["B1"].font = white_bold

    spec_row = 2
    if isinstance(specifications, dict):
        for k, v in specifications.items():
            ws_specs[f"A{spec_row}"] = str(k).replace("_", " ").title()
            ws_specs[f"B{spec_row}"] = str(v) if not isinstance(v, (dict, list)) else json.dumps(v)
            ws_specs[f"A{spec_row}"].font = navy_bold
            ws_specs[f"B{spec_row}"].font = regular_font
            ws_specs[f"A{spec_row}"].border = thin_border
            ws_specs[f"B{spec_row}"].border = thin_border
            spec_row += 1

    # Auto-adjust column widths
    for ws in [ws_summary, ws_specs]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 18)

    # Save Excel file
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, output_filename)
    wb.save(file_path)

    return {
        "status": "success",
        "validation_passed": validation_passed,
        "missing_critical_fields": missing_critical,
        "verified_identifiers": list(found_ids.keys()),
        "output_file_path": file_path,
        "message": f"Excel file successfully generated at {file_path}",
    }
