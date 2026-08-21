"""
Test installed package verification script.
"""
import geovista
from geovista import GeoVistaClient, AsyncGeoVistaClient

print(f"geovista version: {geovista.__version__}")
client = GeoVistaClient(api_key="test-key", base_url="http://localhost:8000")
print("GeoVista SDK client loaded successfully.")
client.close()