import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from a2a.types import AgentCard, AgentInterface
from app.app_utils.a2a import (
    _A2AServerCallContextBuilder,
    _add_v0_3_compat_interface,
    _default_capabilities,
    attach_a2a_routes,
)


def test_a2a_server_call_context_builder_existing_header():
    builder = _A2AServerCallContextBuilder()
    mock_request = MagicMock()
    
    with patch("a2a.server.routes.common.DefaultServerCallContextBuilder.build") as mock_super_build:
        mock_context = MagicMock()
        mock_context.state = {"headers": {"a2a-version": "0.3"}}
        mock_super_build.return_value = mock_context

        res = builder.build(mock_request)
        assert res.state["headers"]["A2A-Version"] == "0.3"


def test_a2a_server_call_context_builder_infer_version():
    builder = _A2AServerCallContextBuilder()
    
    # Test v0.3 slash method
    mock_request = MagicMock()
    mock_request._json = {"method": "message/send"}
    with patch("a2a.server.routes.common.DefaultServerCallContextBuilder.build") as mock_super_build:
        mock_context = MagicMock()
        mock_context.state = {}
        mock_super_build.return_value = mock_context

        res = builder.build(mock_request)
        assert res.state["headers"]["A2A-Version"] == "0.3"

    # Test v1.0 pascal case method
    mock_request._json = {"method": "SendMessage"}
    with patch("a2a.server.routes.common.DefaultServerCallContextBuilder.build") as mock_super_build:
        mock_context = MagicMock()
        mock_context.state = {}
        mock_super_build.return_value = mock_context

        res = builder.build(mock_request)
        assert res.state["headers"]["A2A-Version"] == "1.0"


@pytest.mark.asyncio
async def test_add_v0_3_compat_interface():
    card = MagicMock(spec=AgentCard)
    card.supported_interfaces = [
        AgentInterface(protocol_binding="JSONRPC", protocol_version="1.0", url="http://test/rpc")
    ]

    updated_card = await _add_v0_3_compat_interface(card)
    assert len(updated_card.supported_interfaces) == 2
    assert updated_card.supported_interfaces[1].protocol_version == "0.3"


def test_default_capabilities():
    caps = _default_capabilities()
    assert caps.streaming is True
    assert len(caps.extensions) == 1


@pytest.mark.asyncio
async def test_attach_a2a_routes():
    mock_app = MagicMock()
    mock_agent = MagicMock()
    mock_runner = MagicMock()
    mock_task_store = MagicMock()

    with patch("app.app_utils.a2a.AgentCardBuilder") as mock_builder_cls:
        mock_builder_instance = MagicMock()
        mock_builder_instance.build = AsyncMock(return_value=MagicMock())
        mock_builder_cls.return_value = mock_builder_instance

        with patch("app.app_utils.a2a.add_a2a_routes_to_fastapi") as mock_add_routes:
            await attach_a2a_routes(
                mock_app,
                agent=mock_agent,
                runner=mock_runner,
                task_store=mock_task_store,
                rpc_path="/a2a/app",
            )
            mock_add_routes.assert_called_once()
