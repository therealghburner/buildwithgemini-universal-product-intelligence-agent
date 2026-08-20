import pytest
from unittest.mock import AsyncMock, MagicMock
from app.sub_agents.research_agent import (
    research_agent,
    get_weather,
    get_current_time,
    generate_memories_callback,
)
from app.sub_agents.excel_agent import excel_agent


def test_research_agent_config():
    assert research_agent.name == "research_agent"
    assert "Researches sparse product data" in research_agent.description
    assert len(research_agent.tools) == 3


def test_get_weather():
    sf_weather = get_weather("What is the weather in SF?")
    assert "foggy" in sf_weather.lower()

    ny_weather = get_weather("What is the weather in New York?")
    assert "sunny" in ny_weather.lower()


def test_get_current_time():
    res = get_current_time("Tokyo")
    assert "The current time for query Tokyo" in res


@pytest.mark.asyncio
async def test_generate_memories_callback():
    mock_context = MagicMock()
    mock_context.add_session_to_memory = AsyncMock()

    res = await generate_memories_callback(mock_context)
    mock_context.add_session_to_memory.assert_called_once()
    assert res is None


def test_excel_agent_config():
    assert excel_agent.name == "excel_agent"
    assert "Validates product specification JSON data" in excel_agent.description
    assert len(excel_agent.tools) == 1
