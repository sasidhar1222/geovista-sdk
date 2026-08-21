"""
Manual verification script for installed GeoVista SDK.
"""
from geovista import GeoVistaClient

client = GeoVistaClient(
    api_key="test-api-key",
    base_url="http://127.0.0.1:8000"
)

try:
    print("GeoVista SDK initialized successfully.")
finally:
    client.close()