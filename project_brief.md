# Project Brief: Universal Product Intelligence Agent (Multi-SKU Tree Harvester & Multi-Line Excel Validator)

## Overview
A multi-agent **Search & Retrieval, Extraction, Validation, and Normalization** system built with the Google Agent Development Kit (ADK). The system receives sparse inputs (VPN/MPN, UPC, or product description), scours online databases and web sources, generates an exhaustive structured JSON document with a tree structure traversing all discovered product SKUs/variants, validates mandatory product IDs across all SKUs, retains metadata (confidence scores, timestamps, data sources), and automatically populates a styled multi-line Excel spreadsheet (`.xlsx`) output.

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
       │  - ReAct search & multi-SKU family harvesting           │
       │  - Cross-session memory via Vertex AI Memory Bank      │
       │  - Universal ID resolution per SKU (GTIN, UPC, EAN,    │
       │    MPN, VPN, ASIN, UNSPSC, HS Code)                    │
       │  - Outputs tree-structured JSON (family + SKUs array) │
       └────────────────────────────┬───────────────────────────┘
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ Step 2: Product Validation & Excel Agent               │
       │  - Validates presence of mandatory IDs for all SKUs    │
       │  - Retains confidence scores, timestamps & metadata    │
       │  - Generates styled multi-line Excel file (.xlsx)      │
       │  - Returns file path and summary table to user         │
       └────────────────────────────────────────────────────────┘
```

---

## 2. Key Capabilities & Multi-SKU Features

- **Multi-SKU Tree Structure**: Parses complex product families and traverses all variant SKUs (sizes, colors, volumes, configurations) into a structured `skus` JSON array.
- **Multi-Line Excel Spreadsheet**: Formats each SKU on its own row with columns for SKU ID, Variant Name, Price, GTIN, UPC, EAN, MPN, VPN, ASIN, UNSPSC, HS Code, Technical Attributes, and ID Verification Status.
- **Metadata Retention**: Preserves confidence score (`confidence_score`), ISO timestamp (`timestamp`), and data source origins (`data_sources`) in both JSON and Excel title headers.
- **Vertex AI Memory Bank**: Integrates with Vertex AI Memory Bank (`4920386552309219328`) for cross-session facts and preferences persistence.
- **100% Test Coverage**: Comprehensive unit test suite (`tests/unit/`) covering 100% of all Python statements in `app/`.

---

## 3. Serving & Deployment

- **Local Execution**: Tested locally via `uv run adk run app` and live dev UI `http://localhost:8000/dev-ui/?app=app`.
- **Deployment**: Deployed on Vertex AI Agent Runtime:
  - **Project**: `qwiklabs-gcp-03-ef713aa8c2c9`
  - **Region**: `us-central1`
  - **Reasoning Engine ID**: `projects/562681496404/locations/us-central1/reasoningEngines/4445256791621632000`
- **GitHub Repository**: [`therealghburner/buildwithgemini-universal-product-intelligence-agent`](https://github.com/therealghburner/buildwithgemini-universal-product-intelligence-agent)
