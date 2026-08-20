# Project Brief: Universal Product Intelligence Agent (Product Spec Harvester & Excel Validator)

## Overview
A multi-agent **Search & Retrieval, Extraction, Validation, and Normalization** system built with the Google Agent Development Kit (ADK). The system receives sparse inputs (VPN/MPN, UPC, or product description), scours online databases and web sources, generates an exhaustive structured JSON document with universal product identifiers, validates mandatory product IDs, and automatically populates a formatted Excel spreadsheet (`.xlsx`) output.

---

## 1. Multi-Agent System Architecture

```
                                [User Input]
                      (VPN / UPC / Product Description)
                                     │
                                     ▼
                   ┌──────────────────────────────────┐
                   │        Root Orchestrator         │
                   │        (SequentialAgent)         │
                   └────────────────┬─────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Step 1: Universal Research Agent                       │
       │  - ReAct search & specification harvesting              │
       │  - Cross-session memory via Vertex AI Memory Bank      │
       │  - Universal ID resolution (GTIN, UPC, EAN, MPN, etc.) │
       │  - Outputs exhaustive structured JSON product specs   │
       └────────────────────────────┬───────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Step 2: Validation & Excel Agent                       │
       │  - Validates presence of mandatory universal IDs       │
       │  - Sanitizes and structures JSON payload             │
       │  - Generates styled Excel spreadsheet (.xlsx)          │
       │  - Returns file path and summary to user               │
       └────────────────────────────────────────────────────────┘
```

---

## 2. Key Capabilities & Tool Coverage

- **Vertex AI Memory Bank**: Integrates with Vertex AI Memory Bank (`4920386552309219328`) to retain search history, saved product catalogs, and user preferences across sessions.
- **Universal ID Resolution**: Identifies and verifies universally referenceable product IDs:
  - **GTIN** (14-digit)
  - **UPC** (12-digit)
  - **EAN** (13-digit)
  - **MPN / VPN** (Manufacturer / Vendor Part Number)
  - **ASIN** (Amazon Standard Identification Number)
  - **UNSPSC** (8-digit taxonomy code)
  - **HS Code** (Customs & International Trade classification)
- **Validation & Excel Generation**:
  - Validates mandatory IDs in harvested product data.
  - Formats output spreadsheets using `openpyxl` with custom styling (dark headers, verification status tables, formatted specs).
- **100% Test Coverage**:
  - Comprehensive unit test suite (`tests/unit/`) covering 100% of all Python statements in `app/`.

---

## 3. Serving & Deployment

- **Local Execution**: Ran and verified locally via `uv run adk run app`.
- **Deployment**: Deployed on Vertex AI Agent Runtime:
  - **Project**: `qwiklabs-gcp-03-ef713aa8c2c9`
  - **Region**: `us-central1`
  - **Reasoning Engine ID**: `projects/562681496404/locations/us-central1/reasoningEngines/4445256791621632000`
- **GitHub Repository**: [`therealghburner/buildwithgemini-universal-product-intelligence-agent`](https://github.com/therealghburner/buildwithgemini-universal-product-intelligence-agent)
