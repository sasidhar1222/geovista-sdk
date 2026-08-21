import os
from typing import Optional

from .async_http_client import AsyncHttpClient
from .exceptions import AuthenticationError


class AsyncGeoVistaClient:
    """
    Primary asynchronous client for GeoVista SDK.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.geovista.com",
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        if api_key is None:
            api_key = os.getenv("GEOVISTA_API_KEY")

        if not api_key:
            raise AuthenticationError("API key is required.")

        self.http = AsyncHttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries
        )

    async def close(self):
        """Close the async HTTP client session."""
        await self.http.close()
