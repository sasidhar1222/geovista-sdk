from typing import Any, Dict, Optional


class Resource:
    """
    Base class for all resource API objects.

    Stores the raw API data and optionally a client that can
    perform API operations.
    """

    def __init__(self, **data):
        self._client = data.pop("_client", None)

        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"<{class_name} {self.__dict__}>"