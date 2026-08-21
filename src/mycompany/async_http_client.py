import httpx

from .exceptions import (
    ValidationError,
    AuthenticationError,
    NotFoundError,
    APIError,
    RateLimitError,
    NetworkError
)


class AsyncHttpClient:

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        max_retries: int = 3
    ):

        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

    # ==========================================
    # RETRY
    # ==========================================

    def _should_retry(
        self,
        status_code: int
    ) -> bool:

        return status_code in {
            429,
            502,
            503,
            504
        }

    # ==========================================
    # RETRY DELAY
    # ==========================================

    def _get_retry_delay(
        self,
        attempt: int
    ) -> float:

        return 2 ** attempt

    # ==========================================
    # RESPONSE HANDLER
    # ==========================================

    async def _handle_response(
        self,
        response: httpx.Response
    ):

        try:

            response.raise_for_status()

        except httpx.HTTPStatusError as error:

            status_code = response.status_code

            try:

                data = response.json()

                message = data.get(
                    "detail",
                    data.get(
                        "message",
                        "API request failed."
                    )
                )

            except Exception:

                message = (
                    response.text
                    or "API request failed."
                )

            if status_code == 400:

                raise ValidationError(
                    message
                ) from error

            if status_code == 401:

                raise AuthenticationError(
                    message
                    or "Authentication failed."
                ) from error

            if status_code == 404:

                raise NotFoundError(
                    message
                    or "Resource not found."
                ) from error

            if status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )

                retry_seconds = None

                if retry_after is not None:

                    try:
                        retry_seconds = int(
                            retry_after
                        )
                    except ValueError:
                        pass

                raise RateLimitError(
                    message
                    or "Rate limit exceeded.",
                    retry_after=retry_seconds
                ) from error

            raise APIError(
                message,
                status_code=status_code
            ) from error

        if response.status_code == 204:

            return None

        if not response.content:

            return None

        return response.json()

    # ==========================================
    # COMMON REQUEST
    # ==========================================

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json: dict | None = None
    ):

        for attempt in range(
            self.max_retries + 1
        ):

            try:

                response = await self.client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json
                )

            except httpx.RequestError as error:

                if attempt >= self.max_retries:

                    raise NetworkError(
                        f"Network request failed: {error}"
                    ) from error

                delay = self._get_retry_delay(
                    attempt
                )

                import asyncio

                await asyncio.sleep(delay)

                continue

            if self._should_retry(
                response.status_code
            ):

                if attempt < self.max_retries:

                    delay = self._get_retry_delay(
                        attempt
                    )

                    import asyncio

                    await asyncio.sleep(delay)

                    continue

            return await self._handle_response(
                response
            )

    # ==========================================
    # GET
    # ==========================================

    async def get(
        self,
        path: str,
        params: dict | None = None
    ):

        return await self._request(
            "GET",
            path,
            params=params
        )

    # ==========================================
    # POST
    # ==========================================

    async def post(
        self,
        path: str,
        json: dict | None = None
    ):

        return await self._request(
            "POST",
            path,
            json=json
        )

    # ==========================================
    # PUT
    # ==========================================

    async def put(
        self,
        path: str,
        json: dict | None = None
    ):

        return await self._request(
            "PUT",
            path,
            json=json
        )

    # ==========================================
    # DELETE
    # ==========================================

    async def delete(
        self,
        path: str
    ):

        return await self._request(
            "DELETE",
            path
        )

    # ==========================================
    # CLOSE
    # ==========================================

    async def close(self):

        await self.client.aclose()