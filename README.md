# Universal Product Intelligence Agent (Multi-SKU & Multi-Line Excel System)

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![ADK](https://img.shields.io/badge/framework-Google_ADK-4285F4.svg)](https://adk.dev/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](htmlcov/index.html)
[![Vertex AI Agent Runtime](https://img.shields.io/badge/deployment-Agent_Runtime-34A853.svg)](https://cloud.google.com/vertex-ai)

A multi-stage **Search & Retrieval, Multi-SKU Extraction, Validation, and Normalization** application built with Google ADK (Agent Development Kit). The system enriches sparse product inputs (VPN/MPN, UPC, or Description) into tree-structured JSON documents containing all product variant SKUs, validates mandatory universal identifiers, preserves confidence score and timestamp metadata, and generates styled multi-line Excel spreadsheets (`.xlsx`).

---

## 🏗️ Architecture Overview

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
      │ Sub-Agent 1: Universal Research Agent                  │
      │  - Multi-SKU family search & harvesting                │
      │  - Long-term memory via Vertex AI Memory Bank          │
      │  - Universal ID resolution per SKU (GTIN, UPC, EAN,    │
      │    MPN, VPN, ASIN, UNSPSC, HS Code)                    │
      │  - Generates tree-structured JSON payload (SKUs array) │
      └────────────────────────────┬───────────────────────────┘
                                   │
                                   ▼
      ┌────────────────────────────────────────────────────────┐
      │ Sub-Agent 2: Product Validation & Excel Agent          │
      │  - Validates presence of mandatory IDs for all SKUs    │
      │  - Retains confidence score, timestamp & data sources  │
      │  - Generates styled multi-line Excel file using openpyxl│
      │  - Returns file path and summary table to user          │
      └────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Multi-SKU Tree Structure**: Captures all variant SKUs (sizes, colors, volumes, configurations) under a single product family hierarchy in JSON.
2. **Multi-Line Excel Export**: Formats each SKU on its own row in Excel with columns for SKU ID, Variant Name, Price, GTIN, UPC, EAN, MPN, VPN, ASIN, UNSPSC, HS Code, Technical Attributes, and ID Status.
3. **Metadata & Audit Trail**: Preserves confidence score (`confidence_score`), ISO timestamp (`timestamp`), and source provenance (`data_sources`) in both JSON and Excel output headers.
4. **Vertex AI Memory Bank**: Integrates with Vertex AI Memory Bank (`4920386552309219328`) for cross-session facts and preferences persistence.
5. **100% Test Coverage**: Fully tested using `pytest` and `pytest-cov` across all Python code in `app/`.

---

## 🧪 Testing & Coverage

Run the test suite with coverage report:

```bash
uv run pytest --cov=app --cov-report=term-missing
```

### Coverage Report Summary
```
Name                               Stmts   Miss  Cover
------------------------------------------------------
app/__init__.py                        2      0   100%
app/agent.py                           6      0   100%
app/app_utils/a2a.py                  39      0   100%
app/app_utils/services.py             38      0   100%
app/app_utils/typing.py                9      0   100%
app/fast_api_app.py                   38      0   100%
app/sub_agents/excel_agent.py          6      0   100%
app/sub_agents/research_agent.py      16      0   100%
app/tools/excel_tools.py             102      0   100%
------------------------------------------------------
TOTAL                                256      0   100%
```

---

## 🌐 Running & Testing Locally

Interactive agent execution UI:

```bash
agents-cli playground
```
Open browser at: [http://localhost:8000/dev-ui/?app=app](http://localhost:8000/dev-ui/?app=app)

---

## ☁️ Deployment

Deployed to Vertex AI Agent Runtime:
- **Project**: `qwiklabs-gcp-03-ef713aa8c2c9`
- **Location**: `us-central1`
- **Reasoning Engine ID**: `projects/562681496404/locations/us-central1/reasoningEngines/4445256791621632000`
- **GitHub Repository**: [`therealghburner/buildwithgemini-universal-product-intelligence-agent`](https://github.com/therealghburner/buildwithgemini-universal-product-intelligence-agent)
