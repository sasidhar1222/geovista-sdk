from typing import Any, Dict, List, Optional
from ..models.dataset import Dataset


class DatasetsResource:
    """
    Resource for managing Datasets.
    """

    def __init__(self, http):
        self.http = http

    def create(
        self,
        name: str,
        description: str = "",
        category: Optional[str] = None,
        public: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dataset:
        """
        Create a new dataset.
        """
        payload: Dict[str, Any] = {
            "name": name,
            "description": description,
            "public": public,
        }
        if category is not None:
            payload["category"] = category
        if metadata is not None:
            payload["metadata"] = metadata

        data = self.http.post("/api/datasets", json=payload)
        return Dataset(data=data, http=self.http)

    def get(self, dataset_id: str) -> Dataset:
        """
        Get a dataset by ID.
        """
        data = self.http.get(f"/api/datasets/{dataset_id}")
        return Dataset(data=data, http=self.http)

    def list(
        self,
        page: int = 1,
        per_page: int = 100,
        name: Optional[str] = None
    ) -> List[Dataset]:
        """
        List datasets with optional pagination and filtering.
        """
        params: Dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }
        if name:
            params["name"] = name

        response = self.http.get("/api/datasets", params=params)
        items = response.get("items", response) if isinstance(response, dict) else response
        if isinstance(items, list):
            return [Dataset(data=item, http=self.http) for item in items]
        return []

    def delete(self, dataset_id: str) -> None:
        """
        Delete a dataset by ID.
        """
        self.http.delete(f"/api/datasets/{dataset_id}")
