from geovista import GeoVistaClient, AsyncGeoVistaClient


def test_client_creation():
    client = GeoVistaClient(
        api_key="test-api-key",
        base_url="http://127.0.0.1:8000"
    )

    assert client is not None
    assert client.datasets is not None

    client.close()


def test_async_client_creation():
    client = AsyncGeoVistaClient(
        api_key="test-api-key",
        base_url="http://127.0.0.1:8000"
    )

    assert client is not None
    assert client.http is not None