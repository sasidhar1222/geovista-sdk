from mycompany import MyCompanyClient


def test_client_creation():

    client = MyCompanyClient(
        api_key="test-api-key",
        base_url="http://127.0.0.1:8000"
    )

    assert client is not None
    assert client.users is not None

    client.close()