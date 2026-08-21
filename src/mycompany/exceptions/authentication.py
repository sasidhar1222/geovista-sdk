from .base import MyCompanyError


class AuthenticationError(MyCompanyError):
    """
    Raised when API authentication fails.
    """

    pass