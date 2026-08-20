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
        "Take the product specification JSON document provided, validate that mandatory universal product identifiers "
        "(such as GTIN, UPC, EAN, MPN/VPN, ASIN) and product title exist, and invoke the `validate_and_generate_excel` tool. "
        "Summarize the validation status, list any missing critical fields, and return the path to the generated Excel (.xlsx) file."
    ),
    tools=[validate_and_generate_excel],
)
