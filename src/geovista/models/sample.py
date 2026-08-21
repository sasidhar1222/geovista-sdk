from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .dataset import Dataset


# Used to distinguish:
# assigned_labeler=None
# from
# assigned_labeler not provided
_UNSET = object()


class Sample:
    """
    Represents a Sample resource.

    This class provides a high-level object-oriented API
    for managing samples.
    """

    def __init__(self, client, **data):
        """
        Initialize Sample.

        Parameters
        ----------
        client:
            SDK client used to communicate with the API.

        data:
            Sample data returned from the API.
        """

        self._client = client

        # Store all API response data
        self._data = data

        # Common properties
        self.uuid = data.get("uuid")
        self.name = data.get("name")
        self.attributes = data.get("attributes")
        self.metadata = data.get("metadata")
        self.priority = data.get("priority")

        self.assigned_labeler = data.get("assigned_labeler")
        self.assigned_reviewer = data.get("assigned_reviewer")

        self.readme = data.get("readme")

        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

        # Dataset information
        self.dataset_uuid = data.get("dataset_uuid")

        # Lazy loaded dataset
        self._dataset = None

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def data(self) -> Dict[str, Any]:
        """
        Returns the complete raw sample data.
        """

        return self._data

    @property
    def dataset(self) -> Optional["Dataset"]:
        """
        Gets the Dataset this Sample belongs to.

        The dataset is loaded lazily.
        """

        if self._dataset is not None:
            return self._dataset

        if not self.dataset_uuid:
            return None

        self._dataset = self._client.get_dataset(
            self.dataset_uuid
        )

        return self._dataset

    # ---------------------------------------------------------
    # Sample Operations
    # ---------------------------------------------------------

    def delete(self) -> None:
        """
        Deletes this sample.

        Returns
        -------
        None
        """

        self._client.delete_sample(
            sample_uuid=self.uuid
        )

    def update(
        self,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        priority: Optional[float] = None,
        assigned_labeler: Any = _UNSET,
        assigned_reviewer: Any = _UNSET,
        readme: Optional[str] = None,
        enable_compression: bool = True
    ) -> "Sample":
        """
        Updates this sample.

        Returns
        -------
        Sample
            Updated sample object.
        """

        updated_sample = self._client.update_sample(
            sample_uuid=self.uuid,
            name=name,
            attributes=attributes,
            metadata=metadata,
            priority=priority,
            assigned_labeler=assigned_labeler,
            assigned_reviewer=assigned_reviewer,
            readme=readme,
            enable_compression=enable_compression
        )

        self._update_local_data(updated_sample)

        return self

    # ---------------------------------------------------------
    # Label Operations
    # ---------------------------------------------------------

    def get_label(
        self,
        labelset: str = "ground-truth",
        transform_to_ego_coordinates: bool = False
    ):
        """
        Gets the label for this sample.

        Returns
        -------
        Label
        """

        return self._client.get_label(
            sample_uuid=self.uuid,
            labelset=labelset,
            transform_to_ego_coordinates=
                transform_to_ego_coordinates
        )

    def add_label(
        self,
        labelset: str,
        attributes: Dict[str, Any],
        label_status: str = "PRELABELED",
        score: Optional[float] = None,
        enable_compression: bool = True
    ):
        """
        Adds a label to this sample.

        Returns
        -------
        Label
        """

        return self._client.add_label(
            sample_uuid=self.uuid,
            labelset=labelset,
            attributes=attributes,
            label_status=label_status,
            score=score,
            enable_compression=enable_compression
        )

    def update_label(
        self,
        labelset: str,
        attributes: Optional[Dict[str, Any]] = None,
        label_status: Optional[str] = None,
        score: Optional[float] = None,
        enable_compression: bool = True
    ):
        """
        Updates a label for this sample.

        Returns
        -------
        Label
        """

        return self._client.update_label(
            sample_uuid=self.uuid,
            labelset=labelset,
            attributes=attributes,
            label_status=label_status,
            score=score,
            enable_compression=enable_compression
        )

    def delete_label(
        self,
        labelset: str
    ) -> None:
        """
        Deletes a label from this sample.

        Returns
        -------
        None
        """

        self._client.delete_label(
            sample_uuid=self.uuid,
            labelset=labelset
        )

    # ---------------------------------------------------------
    # Issue Operations
    # ---------------------------------------------------------

    def add_issue(
        self,
        description: str,
        status: str = "OPEN",
        anchor: Optional[Dict[str, Any]] = None
    ):
        """
        Adds an issue to this sample.

        Returns
        -------
        Issue
        """

        return self._client.add_issue(
            sample_uuid=self.uuid,
            description=description,
            status=status,
            anchor=anchor
        )

    def get_issues(self):
        """
        Gets all issues associated with this sample.

        Returns
        -------
        List[Issue]
        """

        return self._client.get_issues(
            sample_uuid=self.uuid
        )

    # ---------------------------------------------------------
    # Internal Methods
    # ---------------------------------------------------------

    def _update_local_data(self, sample):
        """
        Updates the local Sample object after an API update.
        """

        if sample is None:
            return

        if isinstance(sample, Sample):

            self._data = sample._data

            self.uuid = sample.uuid
            self.name = sample.name
            self.attributes = sample.attributes
            self.metadata = sample.metadata
            self.priority = sample.priority

            self.assigned_labeler = sample.assigned_labeler
            self.assigned_reviewer = sample.assigned_reviewer

            self.readme = sample.readme

            self.created_at = sample.created_at
            self.updated_at = sample.updated_at

            self.dataset_uuid = sample.dataset_uuid

        elif isinstance(sample, dict):

            self._data.update(sample)

            for key, value in sample.items():
                setattr(self, key, value)

    def __repr__(self):
        return (
            f"Sample("
            f"uuid={self.uuid!r}, "
            f"name={self.name!r}"
            f")"
        )