# Walkthrough: Vertex AI Memory Bank Integration & Agent Deployment

We successfully integrated **Vertex AI Memory Bank** into the `universal-product-intelligence-agent` and deployed the updated agent to **Google Cloud Agent Runtime**.

## 1. Created Vertex AI Memory Bank Instance
- **Script Executed**: [`scripts/create_memory_bank.py`](file:///config/Desktop/BuildWithGemini/universal-product-intelligence-agent/scripts/create_memory_bank.py)
- **Memory Bank Instance ID**: `4920386552309219328`
- **GCP Location**: `us-central1`
- **GCP Resource Path**: `projects/562681496404/locations/us-central1/reasoningEngines/4920386552309219328`

## 2. Updated Agent Code
- **[`app/agent.py`](file:///config/Desktop/BuildWithGemini/universal-product-intelligence-agent/app/agent.py)**:
  - Wired `PreloadMemoryTool()` into `root_agent` tools to recall user preferences across sessions automatically.
  - Added `generate_memories_callback` as `after_agent_callback` to store facts to Memory Bank after turns.
  - Updated model to `gemini-2.5-flash` for region compatibility.
- **[`app/app_utils/services.py`](file:///config/Desktop/BuildWithGemini/universal-product-intelligence-agent/app/app_utils/services.py)**:
  - Added `get_memory_service()` to instantiate `VertexAiMemoryBankService` when `MEMORY_BANK_ID` is present.
- **[`app/fast_api_app.py`](file:///config/Desktop/BuildWithGemini/universal-product-intelligence-agent/app/fast_api_app.py)**:
  - Passed `memory_service` to `Runner` and `get_fast_api_app`.

## 3. Deployment & Verification
- **Deployed via `agents-cli`**:
  ```bash
  agents-cli deploy -d agent_runtime --project qwiklabs-gcp-03-ef713aa8c2c9 --region us-central1
  ```
- **Deployment Status**: `SUCCESSFUL`
- **Agent Runtime Resource**: `projects/562681496404/locations/us-central1/reasoningEngines/4445256791621632000`
- **Environment Variables**: `MEMORY_BANK_ID=4920386552309219328` injected into deployed container.
- **Verification**: Verified agent query execution locally and on deployment.
