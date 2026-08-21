from .async_http_client import AsyncHttpClient
from .resources.async_users import AsyncUsersResource


class AsyncMyCompanyClient:

    def __init__(
        self,
        api_key: str,
        base_url: str = "http://127.0.0.1:8000",
        timeout: float = 30.0,
        max_retries: int = 3
    ):

        self.http = AsyncHttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries
        )

        self.users = AsyncUsersResource(
            self.http
        )

    async def close(self):

        await self.http.close()