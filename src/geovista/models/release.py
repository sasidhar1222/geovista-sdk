from .resource_api import Resource


class Release(Resource):
    """
    Represents a dataset release.
    """

    def __init__(self, **data):
        self._dataset = data.pop("_dataset", None)
        super().__init__(**data)

    @property
    def dataset(self):
        if self._dataset is None:
            raise RuntimeError("Dataset context is not available.")
        return self._dataset

    def delete(self):
        if self._client is None:
            raise RuntimeError("Client is not available.")

        dataset_id = getattr(self.dataset, "id", str(self.dataset))
        release_name = getattr(self, "name", None)
        return self._client.delete_release(
            dataset=dataset_id,
            release=release_name
        )