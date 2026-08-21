from .base import MyCompanyError


class RateLimitError(MyCompanyError):
    """
    Raised when the API rate limit is exceeded.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded.",
        retry_after: int | None = None
    ):

        super().__init__(message)

        self.retry_after = retry_after