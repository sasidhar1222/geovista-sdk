from .resource_api import Resource

class Issue(Resource):
    """
    Represents an issue associated with a sample.
    """

    def __init__(self, **data):
        super().__init__(**data)

    def update(
        self,
        description=None,
        status=None,
        anchor=None
    ):
        """
        Updates this issue.

        Parameters
        ----------
        description : str, optional
            Description of the issue.

        status : IssueStatus, optional
            OPEN or CLOSED.

        anchor : optional
            Optional location or object anchor.

        Returns
        -------
        Issue
            Updated issue.
        """

        if self._client is None:
            raise RuntimeError(
                "Client is not available for this Issue object."
            )

        return self._client.update_issue(
            issue_id=self.id,
            description=description,
            status=status,
            anchor=anchor
        )

    def delete(self):
        """
        Deletes this issue.

        Returns
        -------
        None
        """

        if self._client is None:
            raise RuntimeError(
                "Client is not available for this Issue object."
            )

        return self._client.delete_issue(
            issue_id=self.id
        )