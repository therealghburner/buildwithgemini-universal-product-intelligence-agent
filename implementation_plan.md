# Add Vertex AI Memory Bank & Deploy Agent

Implement cross-session long-term memory for the `universal-product-intelligence-agent` using Vertex AI Memory Bank, and deploy the updated agent to Google Cloud Agent Runtime.

## User Review Required

> [!IMPORTANT]
> - **Memory Bank Creation**: A managed Agent Engine instance will be created in your GCP project (`qwiklabs-gcp-03-ef713aa8c2c9`).
> - **Agent Deployment**: The agent will be deployed to Vertex AI Agent Runtime using `agents-cli deploy`.

## Proposed Changes

### `universal-product-intelligence-agent`

#### [NEW] [create_memory_bank.py](file:///config/Desktop/BuildWithGemini/universal-product-intelligence-agent/scripts/create_memory_bank.py)
- Create Python script to instantiate a Vertex AI Memory Bank instance (`client.agent_engines.create()`) and output `MEMORY_BANK_ID`.

#### [MODIFY] [agent.py](file:///config/Desktop/BuildWithGemini/universal-product-intelligence-agent/app/agent.py)
- Add `PreloadMemoryTool()` to `root_agent` tools to automatically retrieve memories at turn start.
- Add `generate_memories_callback` as `after_agent_callback` to store durable facts/preferences to Memory Bank after each turn.

#### [MODIFY] [fast_api_app.py](file:///config/Desktop/BuildWithGemini/universal-product-intelligence-agent/app/fast_api_app.py)
- Add `memory_bank_service_builder` using `VertexAiMemoryBankService` pointing to the created `MEMORY_BANK_ID`.

## Verification Plan

### Automated / CLI Verification
1. Run `create_memory_bank.py` to obtain `MEMORY_BANK_ID`.
2. Test memory persistence locally using `uv run adk run`.
3. Deploy the agent using `agents-cli deploy --prototype -y`.
4. Verify deployment with `agents-cli run --mode a2a`.
