from .resource_api import Resource


class Collaborator(Resource):
    """
    Represents a dataset collaborator.
    """

    def __init__(self, **data):
        self._dataset = data.pop("_dataset", None)
        super().__init__(**data)

    @property
    def dataset(self):
        if self._dataset is None:
            raise RuntimeError("Dataset context is not available.")
        return self._dataset

    def update(self, role):
        if self._client is None:
            raise RuntimeError("Client is not available.")

        dataset_id = getattr(self.dataset, "id", str(self.dataset))
        username = getattr(self, "username", None)
        return self._client.update_dataset_collaborator(
            dataset=dataset_id,
            username=username,
            role=role
        )

    def delete(self):
        if self._client is None:
            raise RuntimeError("Client is not available.")

        dataset_id = getattr(self.dataset, "id", str(self.dataset))
        username = getattr(self, "username", None)
        return self._client.delete_dataset_collaborator(
            dataset=dataset_id,
            username=username
        )