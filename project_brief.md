# My agent: Universal Product Intelligence Agent (Product Spec Harvester)

One-liner: A multi-stage Search & Retrieval, Extraction, and Normalization agent that takes sparse inputs (VPN/MPN, UPC, or Description), scours the web, resolves universal product identifiers (GTIN, UPC, EAN, ASIN, UNSPSC, HS Code), and generates exhaustive, validated JSON specification sheets.

## Tool Coverage & Blueprint:
- Memory: Remembers user search history, saved product catalogs, custom attribute schemas, export preferences, and confidence threshold settings across sessions.
- Tools:
  - `product_search`: Web search to locate brand pages, retail catalogs, and spec sheets.
  - `gtin_upc_resolver`: Barcode & GTIN/UPC registry lookup + GTIN-14/UPC-12 checksum algorithm validator.
  - `attribute_extractor`: Multi-stage page content scraper and structured LLM specification extractor.
  - `schema_normalizer`: Normalizes output to standardized JSON schema with confidence scoring and source verification.
- Catalog/UI: Interactive A2UI product cards displaying primary metadata, universal ID mapping tables (GTIN, UPC, EAN, ASIN, MPN, UNSPSC, HS Code), technical spec accordions, and data confidence scores.
- Image gen: Primary & secondary product image retrieval/previews and AI-generated product visualizations.
- Sandbox: Python sandbox for running GTIN/UPC checksum validation, Pydantic JSON schema compliance checks, and unit conversions.

## Architecture Stages:
1. Router & Strategy: Smart routing based on input type (UPC -> direct registry lookup; VPN/MPN -> manufacturer search; Description -> semantic disambiguation).
2. Scour & Retrieve: Multi-step ReAct retrieval loop across search engines & catalog databases.
3. Extract & Disambiguate: Extract specs, categories, and universal IDs.
4. Normalize & Validate: Pydantic structured output validation and cross-source confidence scoring.

## Target Standardized Identifiers:
GTIN (14-digit), UPC (12-digit), EAN (13-digit), ISBN, MPN/VPN, ASIN, UNSPSC (8-digit taxonomy), HS Code (Customs/Trade).

Core rails (everyone): memory, tools, eval, deploy, frontend
My stretch menu (pick later): A2UI product cards & tables, Python sandbox for GTIN checksums & JSON validation, Cloud Storage/Firestore catalog persistence, multi-source confidence scoring.
First eval question: "Given a sparse input like UPC '888462054324' or VPN 'MYFM2LL/A', can the agent resolve the full GTIN, UPC, EAN, MPN, and ASIN, extract complete technical specs (display, chipset, dimensions), score data confidence >= 0.90, and output a valid standardized JSON schema document?"
