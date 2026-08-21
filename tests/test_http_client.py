import httpx
import pytest
import respx

from geovista.http_client import HttpClient
from geovista.exceptions import (
    ValidationError,
    AuthenticationError,
    NotFoundError,
    APIError,
    NetworkError,
)

BASE_URL = "http://test-api"


def create_client():
    return HttpClient(
        base_url=BASE_URL,
        api_key="test-api-key",
        max_retries=0
    )


@respx.mock
def test_get_success():
    route = respx.get(f"{BASE_URL}/api/datasets").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [],
                "page": 1,
                "per_page": 10,
                "total": 0
            }
        )
    )

    client = create_client()
    result = client.get("/api/datasets")

    assert route.called
    assert result["total"] == 0
    client.close()


@respx.mock
def test_401_authentication_error():
    respx.get(f"{BASE_URL}/api/datasets").mock(
        return_value=httpx.Response(
            401,
            json={"detail": "Invalid API key"}
        )
    )

    client = create_client()
    with pytest.raises(AuthenticationError):
        client.get("/api/datasets")
    client.close()


@respx.mock
def test_404_not_found():
    respx.get(f"{BASE_URL}/api/datasets/999").mock(
        return_value=httpx.Response(
            404,
            json={"detail": "Dataset not found"}
        )
    )

    client = create_client()
    with pytest.raises(NotFoundError):
        client.get("/api/datasets/999")
    client.close()


@respx.mock
def test_400_validation_error():
    respx.get(f"{BASE_URL}/api/datasets").mock(
        return_value=httpx.Response(
            400,
            json={"detail": "Invalid request"}
        )
    )

    client = create_client()
    with pytest.raises(ValidationError):
        client.get("/api/datasets")
    client.close()


@respx.mock
def test_500_api_error():
    respx.get(f"{BASE_URL}/api/datasets").mock(
        return_value=httpx.Response(
            500,
            json={"detail": "Internal server error"}
        )
    )

    client = create_client()
    with pytest.raises(APIError):
        client.get("/api/datasets")
    client.close()


@respx.mock
def test_retry_on_503():
    route = respx.get(f"{BASE_URL}/api/datasets")
    route.side_effect = [
        httpx.Response(503, json={"detail": "Service unavailable"}),
        httpx.Response(503, json={"detail": "Service unavailable"}),
        httpx.Response(200, json={"items": [], "page": 1, "per_page": 10, "total": 0})
    ]

    client = HttpClient(
        base_url=BASE_URL,
        api_key="test-api-key",
        max_retries=2
    )

    result = client.get("/api/datasets")
    assert result["total"] == 0
    assert route.call_count == 3
    client.close()


@respx.mock
def test_network_error():
    respx.get(f"{BASE_URL}/api/datasets").mock(
        side_effect=httpx.ConnectError("Connection failed")
    )

    client = HttpClient(
        base_url=BASE_URL,
        api_key="test-api-key",
        max_retries=0
    )

    with pytest.raises(NetworkError):
        client.get("/api/datasets")
    client.close()