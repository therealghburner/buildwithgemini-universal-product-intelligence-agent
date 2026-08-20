import pytest
from unittest.mock import AsyncMock, MagicMock
from app.sub_agents.research_agent import (
    research_agent,
    search_product_catalog,
    generate_memories_callback,
)
from app.sub_agents.excel_agent import excel_agent


def test_research_agent_config():
    assert research_agent.name == "research_agent"
    assert "Researches sparse product data" in research_agent.description
    assert len(research_agent.tools) == 2


def test_search_product_catalog():
    res_coco = search_product_catalog("COCO MADEMOISELLE CRUSH ABSOLU")
    assert "CHANEL" in res_coco
    assert "3145891165203" in res_coco

    res_gen = search_product_catalog("Generic Phone")
    assert "Brand Master" in res_gen


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
