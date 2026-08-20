from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

MODEL = "gemini-2.5-flash"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it to get weather information."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city."""
    return f"The current time for query {query} is 2026-08-20 22:45:00 UTC."


async def generate_memories_callback(callback_context: CallbackContext):
    await callback_context.add_session_to_memory()
    return None


research_agent = Agent(
    name="research_agent",
    description="Researches sparse product data (VPN, UPC, or description) across web databases and generates an exhaustive structured JSON product specification document with universal identifiers (GTIN, UPC, EAN, MPN, ASIN, UNSPSC, HS Code).",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are an expert E-Commerce Universal Product Spec Harvester and Research Specialist. "
        "When given sparse product information (such as VPN/MPN, UPC, or description), search, aggregate, and "
        "synthesize an exhaustive structured JSON document containing:\n"
        "1. `product_info`: title, brand, category, price, currency, description.\n"
        "2. `universal_identifiers`: gtin, upc, ean, mpn, vpn, asin, unspsc, hs_code, isbn.\n"
        "3. `specifications`: detailed technical specifications, dimensions, weight, features, model numbers.\n"
        "4. `metadata`: data_sources, confidence_score, timestamp.\n\n"
        "Return the final JSON block enclosed within ```json ``` code blocks."
    ),
    tools=[get_weather, get_current_time, PreloadMemoryTool()],
    after_agent_callback=generate_memories_callback,
)
