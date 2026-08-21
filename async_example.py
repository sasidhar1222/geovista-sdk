import asyncio
from geovista import AsyncGeoVistaClient


async def main():
    client = AsyncGeoVistaClient(
        api_key="test-api-key",
        base_url="http://127.0.0.1:8000"
    )

    try:
        print("Async GeoVista client initialized successfully.")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())