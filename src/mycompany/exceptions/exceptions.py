class MyCompanyError(Exception):
    pass


class AuthenticationError(MyCompanyError):
    pass


class NotFoundError(MyCompanyError):
    pass


class ValidationError(MyCompanyError):
    pass


class APIError(MyCompanyError):
    pass


class NetworkError(MyCompanyError):
    pass