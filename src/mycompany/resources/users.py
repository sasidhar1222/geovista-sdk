from ..http_client import HttpClient
from ..models.user import User
from ..models.pagination import PaginatedResponse
from ..models.user_filter import UserFilter


class UsersResource:

    def __init__(self, http: HttpClient):
        self.http = http

    # ======================================
    # LIST USERS
    # Pagination + Filtering + Sorting
    # ======================================

    def list(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: UserFilter | None = None
    ) -> PaginatedResponse[User]:

        params = {
            "page": page,
            "page_size": page_size
        }

        if filters is not None:
            params.update(
                filters.to_params()
            )

        data = self.http.get(
            "/api/users",
            params=params
        )

        users = [
            User.from_dict(item)
            for item in data["items"]
        ]

        return PaginatedResponse(
            items=users,
            page=data["page"],
            page_size=data["page_size"],
            total=data["total"]
        )

    # ======================================
    # LIST ALL USERS
    # Automatic Pagination
    # ======================================

    def list_all(
        self,
        page_size: int = 10,
        filters: UserFilter | None = None
    ):

        page = 1

        while True:

            response = self.list(
                page=page,
                page_size=page_size,
                filters=filters
            )

            for user in response.items:
                yield user

            if page * page_size >= response.total:
                break

            page += 1

    # ======================================
    # GET ONE USER
    # ======================================

    def get(
        self,
        user_id: int
    ) -> User:

        data = self.http.get(
            f"/api/users/{user_id}"
        )

        return User.from_dict(data)

    # ======================================
    # CREATE USER
    # ======================================

    def create(
        self,
        name: str,
        email: str
    ) -> User:

        data = self.http.post(
            "/api/users",
            json={
                "name": name,
                "email": email
            }
        )

        return User.from_dict(data)

    # ======================================
    # UPDATE USER
    # ======================================

    def update(
        self,
        user_id: int,
        name: str,
        email: str
    ) -> User:

        data = self.http.put(
            f"/api/users/{user_id}",
            json={
                "name": name,
                "email": email
            }
        )

        return User.from_dict(data)

    # ======================================
    # DELETE USER
    # ======================================

    def delete(
        self,
        user_id: int
    ):

        return self.http.delete(
            f"/api/users/{user_id}"
        )