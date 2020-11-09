from datetime import datetime
import json
import time

from firebird import pagination
from firebird.nodes import _BaseNode

from .base import _BaseResource

__all__ = ['Number']


class Number(_BaseResource):
    """
    A number on Firebird.
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

    @property
    def node(self):
        """Return a node for the number"""

        if not hasattr(self._cached_node, '_cached_node'):
            self._cached_node \
                    = self._client('get', f'numbers/{self.number[1:]}/nodes')

        return self._cached_node

    @node.setter
    def node(self, value):

        if isinstance(value, _BaseNode):
            value = value.to_json_type()

        self._cached_node = self._client(
            'post',
            f'numbers/{self.number[1:]}/nodes',
            data={'node': json.dumps(value)}
        )

    @classmethod
    def all(cls, client, tag=None, q=None, rate_buffer=0):
        """
        Get all numbers.

        Setting the `rate_buffer` to a value greater than 0 ensures the method
        will wait before continuing to fetch results if the number of
        remaining requests falls below the given rate buffer.
        """

        assets = []
        after = None
        has_more = True
        while has_more:

            # Fetch a page of results
            r = client(
                'get',
                'numbers',
                params={
                    'tag': tag,
                    'q': q,
                    'after': after,
                    'limit': 100
                }
            )
            assets.extend([cls(client, a) for a in r['results']])
            after = assets[-1].uid
            has_more = r['has_more']

            if has_more and client.rate_limit_remaining <= rate_buffer:

                # Wait for the rate limit to be reset before requesting
                # another page.
                time.sleep(time.time() - client.rate_limit_reset)

        return assets

    @classmethod
    def many(
        cls,
        client,
        tag=None,
        q=None,
        before=None,
        after=None,
        limit=None
    ):
        """Get a page of assets"""
        r = client(
            'get',
            'numbers',
            params={
                'tag': tag,
                'q': q,
                'before': before,
                'after': after,
                'limit': limit
            }
        )

        return pagination.Page(
            results=[cls(client, a) for a in r['results']],
            result_count=r['result_count'],
            has_more=r['has_more'],
            url=r['url']
        )

    @classmethod
    def one(cls, client, number):
        """Return a number matching the given number"""
        return cls(client, client('get', f'numbers/{number}'))
