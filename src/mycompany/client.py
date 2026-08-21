import os

from .http_client import HttpClient
from .exceptions import AuthenticationError


class MyCompanyClient:

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.mycompany.com",
        timeout: float = 30.0,
        max_retries: int = 3
    ):

        if api_key is None:
            api_key = os.getenv(
                "MYCOMPANY_API_KEY"
            )

        if not api_key:
            raise AuthenticationError(
                "API key is required."
            )

        self.http = HttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries
        )

    def close(self):

        self.http.close()