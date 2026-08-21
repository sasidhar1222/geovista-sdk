import httpx
import pytest
import respx

from geovista import GeoVistaClient
from geovista.models.dataset import Dataset
from geovista.models.sample import Sample

BASE_URL = "http://test-api"


@respx.mock
def test_create_and_list_datasets():
    respx.post(f"{BASE_URL}/api/datasets").mock(
        return_value=httpx.Response(
            201,
            json={
                "id": "ds_123",
                "name": "Traffic Sign Dataset",
                "description": "Dataset containing traffic sign images",
                "public": False
            }
        )
    )

    respx.get(f"{BASE_URL}/api/datasets").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": "ds_123",
                        "name": "Traffic Sign Dataset",
                        "description": "Dataset containing traffic sign images",
                        "public": False
                    }
                ],
                "total": 1
            }
        )
    )

    client = GeoVistaClient(api_key="test-key", base_url=BASE_URL)

    ds = client.datasets.create(
        name="Traffic Sign Dataset",
        description="Dataset containing traffic sign images"
    )
    assert isinstance(ds, Dataset)
    assert ds.id == "ds_123"
    assert ds.name == "Traffic Sign Dataset"

    datasets = client.datasets.list()
    assert len(datasets) == 1
    assert datasets[0].id == "ds_123"

    client.close()


@respx.mock
def test_dataset_sample_operations():
    respx.post(f"{BASE_URL}/api/datasets/ds_123/samples").mock(
        return_value=httpx.Response(
            201,
            json={
                "uuid": "samp_456",
                "name": "image_1.jpg",
                "dataset_uuid": "ds_123",
                "attributes": {"resolution": "1080p"}
            }
        )
    )

    client = GeoVistaClient(api_key="test-key", base_url=BASE_URL)
    ds = Dataset(data={"id": "ds_123", "name": "Test DS"}, http=client.http)

    result = ds.add_sample(
        name="image_1.jpg",
        attributes={"resolution": "1080p"}
    )
    assert result["uuid"] == "samp_456"

    client.close()
