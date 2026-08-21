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


def test_search_product_catalog_domains():
    # Test Footwear / Boot domain
    res_boot = search_product_catalog("Tecovas The Dean Western Boot")
    assert "Tecovas" in res_boot
    assert "Western Boots" in res_boot
    assert "Calfskin Leather" in res_boot
    assert "6403.51.1110" in res_boot

    # Test Fragrance domain
    res_coco = search_product_catalog("COCO MADEMOISELLE CRUSH ABSOLU")
    assert "CHANEL" in res_coco
    assert "3145891165203" in res_coco

    # Test Electronics domain
    res_tech = search_product_catalog("Laptop Computer")
    assert "Electronics & Consumer Goods" in res_tech
    assert "128GB" in res_tech

    # Test General Merchandise Fallback
    res_general = search_product_catalog("Product Description: 'Ceramic Coffee Mug'")
    assert "Ceramic Coffee Mug" in res_general
    assert "Universal Global Brand" in res_general

    # Test Low Confidence / Insufficient Data
    res_invalid = search_product_catalog("unknown_random_string_xyz999")
    assert "INSUFFICIENT_DATA" in res_invalid
    assert "confidence score is too low" in res_invalid


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
