# GeoVista SDK

Official Python SDK for the GeoVista Dataset & AI Platform.

## Installation

```bash
pip install geovista-sdk
```

## Quick Start

### Client Initialization

```python
from geovista import GeoVistaClient

client = GeoVistaClient(
    api_key="your-api-key",
    base_url="https://api.geovista.com"
)
```

### Dataset Management

```python
# Create a new dataset
dataset = client.datasets.create(
    name="Autonomous Driving Vision Data",
    description="High-resolution camera samples for road segmentation",
    public=False
)
print(f"Created Dataset: {dataset.id}")

# List all datasets
datasets = client.datasets.list(page=1, per_page=20)
for ds in datasets:
    print(f"Dataset: {ds.id} - {ds.name}")

# Get a dataset by ID
ds = client.datasets.get(dataset_id="ds_123")
```

### Samples & Annotations

```python
# Add a sample to a dataset
sample_data = dataset.add_sample(
    name="frame_001.jpg",
    attributes={"resolution": "1920x1080", "camera": "front_left"}
)

# Fetch sample details
sample = client.get_sample(sample_uuid=sample_data["uuid"])

# Add label annotations
label = sample.add_label(
    labelset="ground-truth",
    attributes={"polygons": [...]},
    label_status="LABELED"
)
```

## Async Usage

```python
import asyncio
from geovista import AsyncGeoVistaClient


async def main():
    client = AsyncGeoVistaClient(
        api_key="your-api-key",
        base_url="https://api.geovista.com"
    )

    try:
        print("Async client connected successfully.")
    finally:
        await client.close()


asyncio.run(main())
```

## Error Handling

```python
from geovista import GeoVistaClient
from geovista.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    NetworkError
)

client = GeoVistaClient(api_key="your-api-key")

try:
    dataset = client.datasets.get("non_existent_id")
except NotFoundError as err:
    print(f"Resource not found: {err}")
except AuthenticationError as err:
    print(f"Authentication failed: {err}")
except RateLimitError as err:
    print(f"Rate limited. Retry after {err.retry_after} seconds.")
finally:
    client.close()
```

## Development & Testing

Run unit tests:

```bash
pytest
```

Build sdist and wheel packages for distribution:

```bash
python -m build
```

Publish to PyPI using twine:

```bash
python -m twine upload dist/*
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.