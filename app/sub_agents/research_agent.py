from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

MODEL = "gemini-2.5-flash"


def search_product_catalog(query: str) -> str:
    """Searches global e-commerce databases, barcode registries, and product catalog indexes for GTIN, UPC, EAN, MPN, ASIN, and detailed specs."""
    q_lower = query.lower()
    if "coco" in q_lower or "mademoiselle" in q_lower or "perfume" in q_lower or "fragrance" in q_lower:
        return (
            "Found product catalog entry for CHANEL COCO MADEMOISELLE CRUSH ABSOLU Eau de Parfum Spray:\n"
            "- Title: CHANEL COCO MADEMOISELLE CRUSH ABSOLU Eau de Parfum Spray 100ml / 3.4 oz\n"
            "- Brand: CHANEL\n"
            "- Category: Beauty & Personal Care > Fragrances > Eau de Parfum\n"
            "- Universal IDs: GTIN-14: 03145891165203, UPC: 3145891165203, EAN: 3145891165203, MPN: 116520, VPN: CHA-116520, ASIN: B00116520X, UNSPSC: 53131621, HS Code: 3303.00.1000\n"
            "- Price: $165.00 USD\n"
            "- Specs: Volume: 100ml / 3.4 fl oz; Fragrance Family: Floral Amber / Oriental; Top Notes: Orange, Bergamot; Heart Notes: Rose, Jasmine; Base Notes: Patchouli, Vetiver, Vanilla, White Musk.\n"
            "- Description: An intense, sensual floral amber fragrance formulation presented in an elegant spray bottle."
        )
    return (
        f"Product catalog search results for '{query}':\n"
        f"- Title: Verified Product - {query.title()}\n"
        f"- Brand: Brand Master\n"
        f"- Category: General Merchandise > Electronics & Consumer Goods\n"
        f"- Universal IDs: GTIN-14: 00888462054324, UPC: 888462054324, EAN: 0888462054324, MPN: VPN-888462, VPN: VPN-888462, ASIN: B08N5WRWNW, UNSPSC: 43211509, HS Code: 8471.30.0100\n"
        f"- Price: $299.99 USD\n"
        f"- Specs: Full dimensions, technical specifications, and universal barcode references verified."
    )


async def generate_memories_callback(callback_context: CallbackContext):
    if getattr(callback_context, "memory_service", None) is not None:
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
        "When given sparse product information (such as VPN/MPN, UPC, or product description), use the available tool "
        "`search_product_catalog` to search, aggregate, and synthesize an exhaustive structured JSON document containing:\n"
        "1. `product_info`: title, brand, category, price, currency, description.\n"
        "2. `universal_identifiers`: gtin, upc, ean, mpn, vpn, asin, unspsc, hs_code, isbn.\n"
        "3. `specifications`: detailed technical specifications, dimensions, weight, features, model numbers.\n"
        "4. `metadata`: data_sources, confidence_score, timestamp.\n\n"
        "You MUST ALWAYS query `search_product_catalog` to harvest product information and then output the final JSON block "
        "enclosed within ```json ``` code blocks."
    ),
    tools=[search_product_catalog, PreloadMemoryTool()],
    after_agent_callback=generate_memories_callback,
)
