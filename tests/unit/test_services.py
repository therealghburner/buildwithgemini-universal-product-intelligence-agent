import os
from unittest.mock import patch, MagicMock
from app.app_utils.services import (
    get_session_service,
    get_artifact_service,
    get_memory_service,
)
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService, GcsArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService


def test_get_session_service_default():
    get_session_service.cache_clear()
    with patch.dict(os.environ, {}, clear=True):
        srv = get_session_service()
        assert isinstance(srv, InMemorySessionService)


def test_get_session_service_custom_uri():
    get_session_service.cache_clear()
    with patch.dict(os.environ, {"SESSION_SERVICE_URI": "memory://"}):
        srv = get_session_service()
        assert srv is not None


def test_get_session_service_agent_engine():
    get_session_service.cache_clear()
    with patch.dict(
        os.environ,
        {
            "GOOGLE_CLOUD_AGENT_ENGINE_ID": "12345",
            "GOOGLE_CLOUD_PROJECT": "test-project",
            "GOOGLE_CLOUD_LOCATION": "us-central1",
        },
    ):
        with patch("google.adk.sessions.vertex_ai_session_service.VertexAiSessionService") as mock_vertex:
            srv = get_session_service()
            mock_vertex.assert_called_once()


def test_get_artifact_service_in_memory():
    get_artifact_service.cache_clear()
    with patch.dict(os.environ, {}, clear=True):
        srv = get_artifact_service()
        assert isinstance(srv, InMemoryArtifactService)


def test_get_artifact_service_gcs():
    get_artifact_service.cache_clear()
    with patch.dict(os.environ, {"LOGS_BUCKET_NAME": "my-test-bucket"}):
        with patch("app.app_utils.services.GcsArtifactService") as mock_gcs:
            srv = get_artifact_service()
            mock_gcs.assert_called_once_with(bucket_name="my-test-bucket")


def test_get_memory_service_default():
    get_memory_service.cache_clear()
    with patch.dict(os.environ, {}, clear=True):
        srv = get_memory_service()
        assert isinstance(srv, InMemoryMemoryService)


def test_get_memory_service_custom_uri():
    get_memory_service.cache_clear()
    with patch.dict(os.environ, {"MEMORY_SERVICE_URI": "memory://"}):
        srv = get_memory_service()
        assert srv is not None


def test_get_memory_service_bank_id():
    get_memory_service.cache_clear()
    with patch.dict(
        os.environ,
        {
            "MEMORY_BANK_ID": "4920386552309219328",
            "GOOGLE_CLOUD_PROJECT": "test-proj",
            "GOOGLE_CLOUD_LOCATION": "us-central1",
        },
    ):
        with patch("google.adk.memory.vertex_ai_memory_bank_service.VertexAiMemoryBankService") as mock_bank:
            srv = get_memory_service()
            mock_bank.assert_called_once()
