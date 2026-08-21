from .base import MyCompanyError


class NotFoundError(MyCompanyError):
    """
    Raised when a requested resource does not exist.
    """

    pass