from google.adk.agents import SequentialAgent
from google.adk.apps import App
from app.agent import root_agent, app
from app.sub_agents.research_agent import research_agent
from app.sub_agents.excel_agent import excel_agent


def test_orchestrator_agent():
    assert isinstance(root_agent, SequentialAgent)
    assert root_agent.name == "root_agent"
    assert len(root_agent.sub_agents) == 2
    assert root_agent.sub_agents[0] == research_agent
    assert root_agent.sub_agents[1] == excel_agent


def test_app_initialization():
    assert isinstance(app, App)
    assert app.name == "app"
    assert app.root_agent == root_agent
