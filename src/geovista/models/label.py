from .resource_api import Resource


class Label(Resource):
    """
    Represents a label belonging to a sample.
    """

    def __init__(self, **data):
        super().__init__(**data)

    def update(
        self,
        attributes=None,
        label_status=None,
        score=None,
        enable_compression=True
    ):
        """
        Updates this label.

        Parameters
        ----------
        attributes : dict, optional
            The label attributes.

        label_status : LabelStatus, optional
            Status of the label.

        score : float, optional
            Score of the label.

        enable_compression : bool
            Enable gzip compression.

        Returns
        -------
        Label
            Updated label.
        """

        if self._client is None:
            raise RuntimeError(
                "Client is not available for this Label object."
            )

        return self._client.update_label(
            dataset=self.dataset,
            sample=self.sample,
            labelset=self.labelset,
            attributes=attributes,
            label_status=label_status,
            score=score,
            enable_compression=enable_compression
        )

    def delete(self):
        """
        Deletes this label.

        Returns
        -------
        None
        """

        if self._client is None:
            raise RuntimeError(
                "Client is not available for this Label object."
            )

        return self._client.delete_label(
            dataset=self.dataset,
            sample=self.sample,
            labelset=self.labelset
        )