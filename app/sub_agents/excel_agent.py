from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from app.tools.excel_tools import validate_and_generate_excel

MODEL = "gemini-2.5-flash"

excel_agent = Agent(
    name="excel_agent",
    description="Validates product specification JSON data to ensure mandatory universal product identifiers exist, then generates a formatted Excel (.xlsx) file.",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are a Product Data Quality & Excel Generation Specialist. "
        "Take the product specification JSON document provided from research_agent.\n\n"
        "SAFETY & VALIDATION RULES:\n"
        "1. If the input indicates that reliable product information could not be found (or if confidence score is low <0.70, or if no valid JSON block is provided): "
        "   DO NOT call `validate_and_generate_excel`. Simply return the natural language message explaining that product data could not be validated or found.\n"
        "2. If valid product JSON IS provided: invoke `validate_and_generate_excel` directly.\n"
        "   - Pass the raw JSON string as `product_data_json`.\n"
        "   - Pass a clean, simple filename (e.g. `product_spec.xlsx`) as `output_filename`.\n"
        "   - DO NOT wrap function calls in `print()` or Python code blocks.\n\n"
        "Summarize the validation status, list any missing critical fields, and return the path to the generated Excel file."
    ),
    tools=[validate_and_generate_excel],
)
