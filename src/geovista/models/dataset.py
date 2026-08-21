from typing import Any, Dict, List, Optional


class Dataset:
    def __init__(self, data: Dict[str, Any], http):
        self.http = http
        self._data = data

    @property
    def id(self) -> Optional[str]:
        return self._data.get("id")

    @property
    def name(self) -> Optional[str]:
        return self._data.get("name")

    @property
    def description(self) -> Optional[str]:
        return self._data.get("description")

    def __repr__(self):
        return f"Dataset(id={self.id!r}, name={self.name!r})"

    # ---------------------------------------------------------
    # Dataset
    # ---------------------------------------------------------

    def update(
        self,
        description: Optional[str] = None,
        category: Optional[str] = None,
        public: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        payload = {}

        if description is not None:
            payload["description"] = description

        if category is not None:
            payload["category"] = category

        if public is not None:
            payload["public"] = public

        if metadata is not None:
            payload["metadata"] = metadata

        data = self.http.patch(
            f"/api/datasets/{self.id}",
            json=payload
        )

        self._data = data

        return self

    def delete(self):
        self.http.delete(
            f"/api/datasets/{self.id}"
        )

    def clone(
        self,
        new_name: Optional[str] = None,
        public: Optional[bool] = None
    ):
        payload = {}

        if new_name is not None:
            payload["new_name"] = new_name

        if public is not None:
            payload["public"] = public

        data = self.http.post(
            f"/api/datasets/{self.id}/clone",
            json=payload
        )

        return Dataset(
            data=data,
            http=self.http
        )

    # ---------------------------------------------------------
    # Samples
    # ---------------------------------------------------------

    def add_sample(
        self,
        name: str,
        attributes: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        priority: float = 0,
        assigned_labeler: Optional[str] = None,
        assigned_reviewer: Optional[str] = None,
        readme: str = "",
        enable_compression: bool = True,
    ):

        payload = {
            "name": name,
            "attributes": attributes,
            "metadata": metadata,
            "priority": priority,
            "assigned_labeler": assigned_labeler,
            "assigned_reviewer": assigned_reviewer,
            "readme": readme,
            "enable_compression": enable_compression,
        }

        return self.http.post(
            f"/api/datasets/{self.id}/samples",
            json=payload
        )

    def get_samples(
        self,
        name: Optional[str] = None,
        label_status: Optional[str] = None,
        sort: str = "name",
        direction: str = "asc",
        per_page: int = 1000,
        page: int = 1,
    ):

        params = {
            "name": name,
            "label_status": label_status,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page,
        }

        return self.http.get(
            f"/api/datasets/{self.id}/samples",
            params=params
        )

    def delete_samples(self, uuids: List[str]):

        if not uuids:
            raise ValueError("uuids cannot be empty")

        if len(uuids) > 1000:
            raise ValueError(
                "Maximum 1000 samples can be deleted per request"
            )

        return self.http.post(
            f"/api/datasets/{self.id}/samples/delete",
            json={
                "uuids": uuids
            }
        )

    # ---------------------------------------------------------
    # Collaborators
    # ---------------------------------------------------------

    def get_collaborator(self, username: str):

        return self.http.get(
            f"/api/datasets/{self.id}/collaborators/{username}"
        )

    def add_collaborator(
        self,
        username: str,
        role: str = "labeler"
    ):

        return self.http.post(
            f"/api/datasets/{self.id}/collaborators",
            json={
                "username": username,
                "role": role
            }
        )

    # ---------------------------------------------------------
    # Releases
    # ---------------------------------------------------------

    def add_release(
        self,
        name: str,
        description: str = ""
    ):

        return self.http.post(
            f"/api/datasets/{self.id}/releases",
            json={
                "name": name,
                "description": description
            }
        )

    def get_release(self, name: str):

        return self.http.get(
            f"/api/datasets/{self.id}/releases/{name}"
        )

    def get_releases(self):

        return self.http.get(
            f"/api/datasets/{self.id}/releases"
        )

    # ---------------------------------------------------------
    # Labelsets
    # ---------------------------------------------------------

    def add_labelset(
        self,
        name: str,
        description: str = ""
    ):

        return self.http.post(
            f"/api/datasets/{self.id}/labelsets",
            json={
                "name": name,
                "description": description
            }
        )

    def get_labelset(self, name: str):

        return self.http.get(
            f"/api/datasets/{self.id}/labelsets/{name}"
        )

    def get_labelsets(self):

        return self.http.get(
            f"/api/datasets/{self.id}/labelsets"
        )

    # ---------------------------------------------------------
    # Issues
    # ---------------------------------------------------------

    def get_issues(self):

        return self.http.get(
            f"/api/datasets/{self.id}/issues"
        )

    # ---------------------------------------------------------
    # Workunits
    # ---------------------------------------------------------

    def get_workunits(
        self,
        sort: str = "created_at",
        direction: str = "desc",
        start: Optional[str] = None,
        end: Optional[str] = None,
        per_page: int = 1000,
        page: int = 1,
        include_session_time_metrics: bool = False,
    ):

        params = {
            "sort": sort,
            "direction": direction,
            "start": start,
            "end": end,
            "per_page": per_page,
            "page": page,
            "include_session_time_metrics":
                include_session_time_metrics,
        }

        return self.http.get(
            f"/api/datasets/{self.id}/workunits",
            params=params
        )