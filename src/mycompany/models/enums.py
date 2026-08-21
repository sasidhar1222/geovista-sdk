from enum import Enum


class SortOrder(str, Enum):

    ASC = "asc"

    DESC = "desc"


class UserSortField(str, Enum):

    ID = "id"

    NAME = "name"

    EMAIL = "email"