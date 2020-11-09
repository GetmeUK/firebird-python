from datetime import datetime
import json

__all__ = ['_BaseResource']


# NOTE: The resource classes provide thin wrappers to data fetched from the
# API by the API client. They should not be initialized directly. Instead they
# should be returned by class methods such as `create`, `all`, `one` and
# `many`.


class _BaseResource:
    """
    A base resource used to wrap documents fetched from the API with dot
    notation access to attributes and methods for access to related API
    endpoints.
    """

    def __init__(self, client, document):

        # The API client used to fetch the resource
        self._client = client

        # The document representing the resource's data
        self._document = document

    def __getattr__(self, name):

        if '_document' in self.__dict__:
            return self.__dict__['_document'].get(name, None)

        raise AttributeError(
            f"'{self.__class__.__name__}' has no attribute '{name}'"
        )

    def __getitem__(self, name):
        return self.__dict__['_document'][name]

    def __contains__(self, name):
        return name in self.__dict__['_document']

    def get(self, name, default=None):
        return self.__dict__['_document'].get(name, default)
