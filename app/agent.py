from google.adk.agents import SequentialAgent
from google.adk.apps import App
from app.sub_agents.research_agent import research_agent
from app.sub_agents.excel_agent import excel_agent

# Root Orchestrator Agent: executes research harvester first, then validation & Excel generator
root_agent = SequentialAgent(
    name="root_agent",
    description="Orchestrates end-to-end product research, JSON specification harvesting, identifier validation, and Excel (.xlsx) file generation.",
    sub_agents=[research_agent, excel_agent],
)

app = App(
    root_agent=root_agent,
    name="app",
)
