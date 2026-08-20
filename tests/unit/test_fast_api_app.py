import pytest
import runpy
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.fast_api_app import app, lifespan
from app.app_utils.typing import Feedback


def test_collect_feedback():
    client = TestClient(app)
    feedback_payload = {
        "score": 5,
        "text": "Great agent response!",
        "service_name": "my-agent",
        "log_type": "feedback"
    }

    with patch("app.fast_api_app.logger.log_struct") as mock_log:
        response = client.post("/feedback", json=feedback_payload)
        assert response.status_code == 200
        assert response.json() == {"status": "success"}
        mock_log.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan():
    mock_app = MagicMock()
    mock_app.state = MagicMock()

    with patch("app.fast_api_app.attach_a2a_routes") as mock_attach:
        async with lifespan(mock_app):
            assert mock_app.state.runner is not None
            assert mock_app.state.agent_app_name == "app"
        mock_attach.assert_called_once()


def test_feedback_typing_defaults():
    fb = Feedback(score=4.5)
    assert fb.score == 4.5
    assert fb.text == ""
    assert fb.log_type == "feedback"
    assert fb.service_name == "my-agent"
    assert fb.user_id is not None
    assert fb.session_id is not None


def test_main_block():
    with patch("uvicorn.run") as mock_run:
        runpy.run_module("app.fast_api_app", run_name="__main__")
        assert mock_run.called
