from .base import MyCompanyError


class APIError(MyCompanyError):
    """
    Raised when the API returns an unexpected error.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None
    ):

        super().__init__(message)

        self.status_code = status_code