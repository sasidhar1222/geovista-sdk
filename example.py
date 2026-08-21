from geovista import GeoVistaClient

client = GeoVistaClient(
    api_key="test-api-key",
    base_url="http://127.0.0.1:8000"
)

try:
    print("Creating dataset...")
    ds = client.datasets.create(
        name="Demo Dataset",
        description="Dataset for testing GeoVista SDK features"
    )
    print(f"Created: {ds.id} - {ds.name}")

    print("Listing datasets...")
    datasets = client.datasets.list()
    for d in datasets:
        print(f"Dataset: {d.id} - {d.name}")

finally:
    client.close()