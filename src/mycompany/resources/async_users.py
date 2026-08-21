from ..models.user import User
from ..models.pagination import PaginatedResponse


class AsyncUsersResource:

    def __init__(self, http):

        self.http = http

    async def list(
        self,
        page: int = 1,
        page_size: int = 10,
        filters=None
    ):

        params = {
            "page": page,
            "page_size": page_size
        }

        if filters:

            params.update(
                filters.to_params()
            )

        data = await self.http.get(
            "/api/users",
            params=params
        )

        return PaginatedResponse(
            items=[
                User(**item)
                for item in data["items"]
            ],
            page=data["page"],
            page_size=data["page_size"],
            total=data["total"]
        )

    async def get(
        self,
        user_id: int
    ):

        data = await self.http.get(
            f"/api/users/{user_id}"
        )

        return User(**data)

    async def create(
        self,
        name: str,
        email: str
    ):

        data = await self.http.post(
            "/api/users",
            json={
                "name": name,
                "email": email
            }
        )

        return User(**data)

    async def update(
        self,
        user_id: int,
        name: str,
        email: str
    ):

        data = await self.http.put(
            f"/api/users/{user_id}",
            json={
                "name": name,
                "email": email
            }
        )

        return User(**data)

    async def delete(
        self,
        user_id: int
    ):

        return await self.http.delete(
            f"/api/users/{user_id}"
        )