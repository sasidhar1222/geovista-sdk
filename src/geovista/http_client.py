import time
import httpx

from .logger import get_logger

from .exceptions import (
    ValidationError,
    AuthenticationError,
    NotFoundError,
    APIError,
    RateLimitError,
    NetworkError
)


class HttpClient:

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

        self.logger = get_logger()

        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

    # ==========================================
    # RETRY CHECK
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

    def _handle_response(
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

            # 400
            if status_code == 400:

                raise ValidationError(
                    message
                ) from error

            # 401
            if status_code == 401:

                raise AuthenticationError(
                    message
                    or "Authentication failed."
                ) from error

            # 404
            if status_code == 404:

                raise NotFoundError(
                    message
                    or "Resource not found."
                ) from error

            # 429
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

            # Other HTTP errors
            raise APIError(
                message,
                status_code=status_code
            ) from error

        # 204 No Content
        if response.status_code == 204:

            return None

        # Empty response
        if not response.content:

            return None

        return response.json()

    # ==========================================
    # COMMON REQUEST
    # ==========================================

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json: dict | None = None
    ):

        self.logger.info(
            f"{method} {path}"
        )

        for attempt in range(
            self.max_retries + 1
        ):

            try:

                response = self.client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json
                )

            except httpx.RequestError as error:

                self.logger.warning(
                    f"Network error: {error}"
                )

                if attempt >= self.max_retries:

                    raise NetworkError(
                        f"Network request failed: {error}"
                    ) from error

                delay = self._get_retry_delay(
                    attempt
                )

                self.logger.warning(
                    f"Retrying in {delay} seconds "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )

                time.sleep(delay)

                continue

            self.logger.info(
                f"Response: {response.status_code}"
            )

            if self._should_retry(
                response.status_code
            ):

                if attempt < self.max_retries:

                    delay = self._get_retry_delay(
                        attempt
                    )

                    self.logger.warning(
                        f"Retrying HTTP {response.status_code} "
                        f"in {delay} seconds "
                        f"(attempt {attempt + 1}/{self.max_retries})"
                    )

                    time.sleep(delay)

                    continue

            return self._handle_response(
                response
            )

    # ==========================================
    # GET
    # ==========================================

    def get(
        self,
        path: str,
        params: dict | None = None
    ):

        return self._request(
            "GET",
            path,
            params=params
        )

    # ==========================================
    # POST
    # ==========================================

    def post(
        self,
        path: str,
        json: dict | None = None
    ):

        return self._request(
            "POST",
            path,
            json=json
        )

    # ==========================================
    # PUT
    # ==========================================

    def put(
        self,
        path: str,
        json: dict | None = None
    ):

        return self._request(
            "PUT",
            path,
            json=json
        )

    # ==========================================
    # PATCH
    # ==========================================

    def patch(
        self,
        path: str,
        json: dict | None = None
    ):

        return self._request(
            "PATCH",
            path,
            json=json
        )

    # ==========================================
    # DELETE
    # ==========================================

    def delete(
        self,
        path: str
    ):

        return self._request(
            "DELETE",
            path
        )

    # ==========================================
    # CLOSE
    # ==========================================

    def close(self):

        self.client.close()