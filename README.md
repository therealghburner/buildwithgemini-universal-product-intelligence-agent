# Universal Product Intelligence Agent (Multi-Agent System)

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![ADK](https://img.shields.io/badge/framework-Google_ADK-4285F4.svg)](https://adk.dev/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](htmlcov/index.html)
[![Vertex AI Agent Runtime](https://img.shields.io/badge/deployment-Agent_Runtime-34A853.svg)](https://cloud.google.com/vertex-ai)

A multi-stage **Search & Retrieval, Extraction, Validation, and Normalization** multi-agent application built with Google ADK (Agent Development Kit). The system enriches sparse product inputs (VPN/MPN, UPC, or Description) into structured JSON documents, validates mandatory universal product identifiers, and generates formatted Excel spreadsheets (`.xlsx`).

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
      │  - ReAct search & specification harvesting             │
      │  - Long-term memory via Vertex AI Memory Bank          │
      │  - Universal ID resolution (GTIN, UPC, EAN, MPN, etc.)│
      │  - Generates exhaustive structured JSON payload        │
      └────────────────────────────┬───────────────────────────┘
                                   │
                                   ▼
      ┌────────────────────────────────────────────────────────┐
      │ Sub-Agent 2: Product Validation & Excel Agent          │
      │  - Validates presence of mandatory universal IDs      │
      │  - Generates styled Excel file using openpyxl          │
      │  - Returns file path and summary table to user          │
      └────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Multi-Agent Orchestration**: Sequential execution pipeline combining a research harvesting agent and an Excel validation/formatting agent.
2. **Universal Product ID Resolution**: Extracts and validates universally referenceable IDs:
   - **GTIN** (14-digit)
   - **UPC** (12-digit)
   - **EAN** (13-digit)
   - **MPN / VPN** (Manufacturer / Vendor Part Number)
   - **ASIN** (Amazon Standard Identification Number)
   - **UNSPSC** (8-digit taxonomy code)
   - **HS Code** (Customs classification)
3. **Vertex AI Memory Bank**: Integrates with Vertex AI Memory Bank (`4920386552309219328`) for cross-session facts and preferences persistence.
4. **Excel Export**: Formats spreadsheets with custom headers, verification tables, and technical specs.
5. **100% Test Coverage**: Fully tested using `pytest` and `pytest-cov` across all Python code in `app/`.

---

## 📁 Project Structure

```
universal-product-intelligence-agent/
├── app/
│   ├── agent.py                 # Root Orchestrator (SequentialAgent)
│   ├── fast_api_app.py          # FastAPI Backend server with A2A support
│   ├── sub_agents/
│   │   ├── research_agent.py    # Universal Product Research Sub-Agent
│   │   └── excel_agent.py       # Product Validation & Excel Sub-Agent
│   ├── tools/
│   │   └── excel_tools.py       # Validation and Excel generation tools
│   └── app_utils/               # Services, typing, and A2A helpers
├── tests/
│   ├── unit/                    # Unit tests achieving 100% code coverage
│   └── integration/             # End-to-end integration tests
├── project_brief.md             # Complete project design brief
├── pyproject.toml               # Python dependencies and configuration
└── walkthrough.md               # Implementation walkthrough artifact
```

---

## 🧪 Testing & Coverage

Run the test suite with coverage report:

```bash
uv run pytest --cov=app --cov-report=term-missing
```

### Final Test Coverage Output
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
app/sub_agents/research_agent.py      17      0   100%
app/tools/excel_tools.py             108      0   100%
------------------------------------------------------
TOTAL                                263      0   100%
```

---

## 🌐 Running Locally

Interactive agent execution:

```bash
uv run adk run app
```

Launch FastAPI web server with A2A protocol:

```bash
uv run uvicorn app.fast_api_app:app --host 0.0.0.0 --port 8000
```

---

## ☁️ Deployment

Deployed to Vertex AI Agent Runtime:
- **Project**: `qwiklabs-gcp-03-ef713aa8c2c9`
- **Location**: `us-central1`
- **Reasoning Engine ID**: `projects/562681496404/locations/us-central1/reasoningEngines/4445256791621632000`
- **GitHub Repository**: [`therealghburner/buildwithgemini-universal-product-intelligence-agent`](https://github.com/therealghburner/buildwithgemini-universal-product-intelligence-agent)
