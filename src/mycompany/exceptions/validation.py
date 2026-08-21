from .base import MyCompanyError


class ValidationError(MyCompanyError):
    """
    Raised when SDK input validation fails.
    """

    pass