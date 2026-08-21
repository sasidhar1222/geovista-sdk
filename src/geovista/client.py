import os
from typing import Any, Dict, List, Optional

from .http_client import HttpClient
from .resources.datasets import DatasetsResource
from .exceptions import AuthenticationError
from .models.dataset import Dataset
from .models.sample import Sample, _UNSET
from .models.label import Label
from .models.issue import Issue
from .models.collaborator import Collaborator
from .models.labelset import Labelset
from .models.release import Release


class GeoVistaClient:
    """
    Primary synchronous client for GeoVista SDK.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.geovista.com",
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        if api_key is None:
            api_key = os.getenv("GEOVISTA_API_KEY")

        if not api_key:
            raise AuthenticationError("API key is required.")

        self.http = HttpClient(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries
        )

        self.datasets = DatasetsResource(self.http)

    def close(self):
        """Close the HTTP client session."""
        self.http.close()

    # ==========================================
    # DATASET HELPERS
    # ==========================================

    def get_dataset(self, dataset_id: str) -> Dataset:
        """Fetch a Dataset by ID."""
        return self.datasets.get(dataset_id)

    # ==========================================
    # SAMPLE OPERATIONS
    # ==========================================

    def get_sample(self, sample_uuid: str) -> Sample:
        """Fetch a Sample by UUID."""
        data = self.http.get(f"/api/samples/{sample_uuid}")
        return Sample(client=self, **data)

    def update_sample(
        self,
        sample_uuid: str,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[float] = None,
        assigned_labeler: Any = _UNSET,
        assigned_reviewer: Any = _UNSET,
        readme: Optional[str] = None,
        enable_compression: bool = True
    ) -> Sample:
        """Update a Sample."""
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if attributes is not None:
            payload["attributes"] = attributes
        if metadata is not None:
            payload["metadata"] = metadata
        if priority is not None:
            payload["priority"] = priority
        if assigned_labeler is not _UNSET:
            payload["assigned_labeler"] = assigned_labeler
        if assigned_reviewer is not _UNSET:
            payload["assigned_reviewer"] = assigned_reviewer
        if readme is not None:
            payload["readme"] = readme

        data = self.http.patch(f"/api/samples/{sample_uuid}", json=payload)
        return Sample(client=self, **data)

    def delete_sample(self, sample_uuid: str) -> None:
        """Delete a Sample."""
        self.http.delete(f"/api/samples/{sample_uuid}")

    # ==========================================
    # LABEL OPERATIONS
    # ==========================================

    def get_label(
        self,
        sample_uuid: str,
        labelset: str = "ground-truth",
        transform_to_ego_coordinates: bool = False
    ) -> Label:
        """Get label for a sample."""
        params = {"transform_to_ego_coordinates": transform_to_ego_coordinates}
        data = self.http.get(
            f"/api/samples/{sample_uuid}/labels/{labelset}",
            params=params
        )
        return Label(_client=self, sample=sample_uuid, labelset=labelset, **data)

    def add_label(
        self,
        sample_uuid: str,
        labelset: str,
        attributes: Dict[str, Any],
        label_status: str = "PRELABELED",
        score: Optional[float] = None,
        enable_compression: bool = True
    ) -> Label:
        """Add label to a sample."""
        payload = {
            "labelset": labelset,
            "attributes": attributes,
            "label_status": label_status,
            "score": score
        }
        data = self.http.post(f"/api/samples/{sample_uuid}/labels", json=payload)
        return Label(_client=self, sample=sample_uuid, labelset=labelset, **data)

    def update_label(
        self,
        sample: str,
        labelset: str,
        dataset: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        label_status: Optional[str] = None,
        score: Optional[float] = None,
        enable_compression: bool = True
    ) -> Label:
        """Update label on a sample."""
        payload: Dict[str, Any] = {}
        if attributes is not None:
            payload["attributes"] = attributes
        if label_status is not None:
            payload["label_status"] = label_status
        if score is not None:
            payload["score"] = score

        data = self.http.patch(
            f"/api/samples/{sample}/labels/{labelset}",
            json=payload
        )
        return Label(_client=self, sample=sample, labelset=labelset, **data)

    def delete_label(
        self,
        sample: str,
        labelset: str,
        dataset: Optional[str] = None
    ) -> None:
        """Delete label from a sample."""
        self.http.delete(f"/api/samples/{sample}/labels/{labelset}")

    # ==========================================
    # ISSUE OPERATIONS
    # ==========================================

    def add_issue(
        self,
        sample_uuid: str,
        description: str,
        status: str = "OPEN",
        anchor: Optional[Dict[str, Any]] = None
    ) -> Issue:
        """Add an issue to a sample."""
        payload = {
            "description": description,
            "status": status,
            "anchor": anchor
        }
        data = self.http.post(f"/api/samples/{sample_uuid}/issues", json=payload)
        return Issue(_client=self, **data)

    def get_issues(self, sample_uuid: str) -> List[Issue]:
        """Get all issues for a sample."""
        data = self.http.get(f"/api/samples/{sample_uuid}/issues")
        items = data if isinstance(data, list) else data.get("items", [])
        return [Issue(_client=self, **item) for item in items]

    def update_issue(
        self,
        issue_id: str,
        description: Optional[str] = None,
        status: Optional[str] = None,
        anchor: Optional[Dict[str, Any]] = None
    ) -> Issue:
        """Update an issue."""
        payload: Dict[str, Any] = {}
        if description is not None:
            payload["description"] = description
        if status is not None:
            payload["status"] = status
        if anchor is not None:
            payload["anchor"] = anchor

        data = self.http.patch(f"/api/issues/{issue_id}", json=payload)
        return Issue(_client=self, **data)

    def delete_issue(self, issue_id: str) -> None:
        """Delete an issue."""
        self.http.delete(f"/api/issues/{issue_id}")

    # ==========================================
    # COLLABORATOR & SUB-RESOURCES
    # ==========================================

    def update_dataset_collaborator(
        self,
        dataset: str,
        username: str,
        role: str
    ) -> Collaborator:
        """Update dataset collaborator role."""
        data = self.http.put(
            f"/api/datasets/{dataset}/collaborators/{username}",
            json={"role": role}
        )
        return Collaborator(_client=self, username=username, role=role, **(data or {}))

    def delete_dataset_collaborator(
        self,
        dataset: str,
        username: str
    ) -> None:
        """Delete collaborator from dataset."""
        self.http.delete(f"/api/datasets/{dataset}/collaborators/{username}")

    def delete_labelset(
        self,
        dataset: str,
        labelset: str
    ) -> None:
        """Delete labelset from dataset."""
        self.http.delete(f"/api/datasets/{dataset}/labelsets/{labelset}")

    def delete_release(
        self,
        dataset: str,
        release: str
    ) -> None:
        """Delete release from dataset."""
        self.http.delete(f"/api/datasets/{dataset}/releases/{release}")