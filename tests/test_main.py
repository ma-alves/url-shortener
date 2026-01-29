# from Claude Haiku 4.5

from datetime import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from ..app.database import get_session
from ..app.main import app
from ..app.models import Url


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
async def mock_session():
    """Create a mock AsyncSession."""
    mock = AsyncMock(spec=AsyncSession)
    return mock


@pytest.fixture
def mock_url_object():
    """Create a mock Url object."""
    return Url(
        uuid=str(uuid4()),
        long_url="https://example.com/very/long/url",
        short_code="abc123",
        created_at=datetime.now(),
    )


class TestIndexEndpoint:
    """Tests for GET / endpoint."""

    def test_index_returns_message(self, client):
        """Test that index endpoint returns a message with OK status."""
        response = client.get("/")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "http://127.0.0.1:8000/docs#/"}

    def test_index_response_json_structure(self, client):
        """Test that index response has correct JSON structure."""
        response = client.get("/")
        data = response.json()

        assert "message" in data
        assert isinstance(data["message"], str)


class TestShortenEndpoint:
    """Tests for POST /shorten endpoint."""

    @pytest.mark.asyncio
    async def test_shorten_url_creates_new_entry(self, client, mock_url_object):
        """Test successful URL shortening creates new entry."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.scalar.return_value = None
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()

            async def add_side_effect(obj):
                obj.uuid = mock_url_object.uuid
                obj.created_at = mock_url_object.created_at

            mock_session.add.side_effect = add_side_effect
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        response = client.post(
            "/shorten", params={"url": "https://example.com/very/long/url"}
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert "uuid" in data
        assert data["long_url"] == "https://example.com/very/long/url"
        assert "short_code" in data
        assert "created_at" in data

        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_shorten_url_returns_existing(self, client, mock_url_object):
        """Test that existing URL is returned without duplication."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.scalar.return_value = mock_url_object
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        response = client.post(
            "/shorten", params={"url": "https://example.com/very/long/url"}
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["long_url"] == "https://example.com/very/long/url"
        assert data["short_code"] == mock_url_object.short_code

        app.dependency_overrides.clear()

    def test_shorten_url_invalid_url(self, client):
        """Test that invalid URL returns validation error."""
        response = client.post("/shorten", params={"url": "not-a-valid-url"})

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_shorten_url_missing_url_parameter(self, client):
        """Test that missing URL parameter returns error."""
        response = client.post("/shorten")

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_shorten_url_response_structure(self, client, mock_url_object):
        """Test that shorten response has correct structure."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.scalar.return_value = mock_url_object
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        response = client.post(
            "/shorten", params={"url": "https://example.com/very/long/url"}
        )

        data = response.json()
        assert "uuid" in data
        assert "long_url" in data
        assert "short_code" in data
        assert "created_at" in data

        app.dependency_overrides.clear()


class TestGetUrlEndpoint:
    """Tests for GET /{short_code} endpoint."""

    @pytest.mark.asyncio
    async def test_get_url_redirects_to_long_url(self, client, mock_url_object):
        """Test that short code redirects to long URL."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.scalar.return_value = mock_url_object
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        with patch("app.main.get_cached_code", return_value=None):
            with patch("app.main.set_cached_data"):
                response = client.get(
                    f"/{mock_url_object.short_code}", follow_redirects=False
                )

        assert response.status_code == HTTPStatus.FOUND
        assert response.headers["location"] == mock_url_object.long_url

        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_get_url_from_cache(self, client, mock_url_object):
        """Test that URL is served from cache when available."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        with patch("app.main.get_cached_code", return_value=mock_url_object.long_url):
            response = client.get(
                f"/{mock_url_object.short_code}", follow_redirects=False
            )

        assert response.status_code == HTTPStatus.FOUND
        assert response.headers["location"] == mock_url_object.long_url

        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_get_url_not_found(self, client):
        """Test that 404 is returned for non-existent short code."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.scalar.return_value = None
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        with patch("app.main.get_cached_code", return_value=None):
            response = client.get("/nonexistent", follow_redirects=False)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "URL não encontrada" in response.json()["detail"]

        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_get_url_not_found_response_structure(self, client):
        """Test that 404 response has correct error structure."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.scalar.return_value = None
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        with patch("app.main.get_cached_code", return_value=None):
            response = client.get("/invalid")

        data = response.json()
        assert "detail" in data

        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_get_url_caches_data_when_found(self, client, mock_url_object):
        """Test that data is cached when URL is found in database."""

        async def override_get_session():
            mock_session = AsyncMock(spec=AsyncSession)
            mock_session.scalar.return_value = mock_url_object
            yield mock_session

        app.dependency_overrides[get_session] = override_get_session

        with patch("app.main.get_cached_code", return_value=None):
            with patch("app.main.set_cached_data") as mock_cache:
                response = client.get(
                    f"/{mock_url_object.short_code}", follow_redirects=False
                )

                mock_cache.assert_called_once_with(
                    mock_url_object.short_code, mock_url_object.long_url
                )

        assert response.status_code == HTTPStatus.FOUND

        app.dependency_overrides.clear()
