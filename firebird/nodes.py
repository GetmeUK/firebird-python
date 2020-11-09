
__all__ = [
    'ForwardNode',
    'IVRNode',
    'TimeSwitchNode'
]


class _BaseNode:
    """
    A base node class. Nodes are used to simplify the process of building
    flows for numbers.
    """

    _node_type = 'Base'

    _fields = []

    def __init__(self):

        # The edges
        self._edges = {}

    def connect(self, key, node):
        assert key in self.connections, 'Not a supported connection'
        self._edges[key] = node

    @property
    def connections(self):
        return []

    def to_json_type(self):
        data = {
            'node_type': self._node_type,
            'edges': {k: e.to_json_type() for k, e in self._edges.items()},
        }

        for f in self._fields:
            data[f] = getattr(self, f, None)

        return data


class ForwardNode(_BaseNode):

    _node_type = 'forward'

    _fields = [
        'number',
        'messages',
        'whisper',
        'whisper_message',
        'disable_call_recording'
    ]

    _connections = []

    def __init__(
        self,
        number,
        messages=None,
        whisper='',
        whisper_message=None,
        disable_call_recording=False
    ):
        super().__init__()

        self.number = number
        self.messages = messages or []
        self.whisper = whisper
        self.whisper_message = whisper_message
        self.disable_call_recording = disable_call_recording


class IVRNode(_BaseNode):

    _node_type = 'ivr'

    _fields = [
        'digits',
        'messages',
        'repeats',
        'fallback_number'
    ]

    _connections = []

    def __init__(
        self,
        digits,
        messages=None,
        repeats=-1
    ):
        super().__init__()

        self.digits = digits or []
        self.messages = messages or []
        self.repeats = repeats

    @property
    def connections(self):
        connections = self.digits.copy()
        if self.repeats > -1:
            connections.append('fallback')
        return connections


class TimeSwitchNode(_BaseNode):

    _node_type = 'time_switch'

    _fields = [
        'weekdays',
        'christmas_day',
        'boxing_day',
        'new_years_day'
    ]

    _connections = []

    def __init__(
        self,
        weekdays,
        christmas_day,
        boxing_day,
        new_years_day
    ):
        super().__init__()

        self.weekdays = weekdays or []
        self.christmas_day = christmas_day or False
        self.boxing_day = boxing_day or False
        self.new_years_day = new_years_day or False

    @property
    def connections(self):
        return ['within', 'outside']
