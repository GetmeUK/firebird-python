from .base import _BaseResource

__all__ = [
    'Number',
    'PartialNumber'
]


class PartialNumber(_BaseResource):
    """
    A partial view of an number on Firebird.

    NOTE: Partial number are returned when requesting a list of numbers from
    the API. You can expand a partial number to a full number by calling the
    `expand` method.
    """

    def __init__(self, client, document):
        super().__init__(client, document)

        # Convert `created` and `modified` to dates
        self._document['created'] \
                = datetime.fromisoformat(self._document['created'])

        self._document['modified'] \
                = datetime.fromisoformat(self._document['modified'])

    def __str__(self):
        return f'Partial number: {self.number}'

    def expand(self):
        """Return a full Number for the partial number"""
        return self._client.get_number(self.id)


class Number(_BaseResource):
    """
    An number stored on Hangar51.
    """

    def __init__(self, client, document):
        super().__init__(client, document)

        # Convert `created` and `modified` to dates
        self._document['created'] \
                = datetime.fromisoformat(self._document['created'])

        self._document['modified'] \
                = datetime.fromisoformat(self._document['modified'])

    def __str__(self):
        return f'Number: {self.number}'
