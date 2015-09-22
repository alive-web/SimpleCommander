import json


class Signal(object):
    def __init__(self, signal_name, *args, **kwargs):
        self.name = signal_name
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def from_message(cls, message):
        if isinstance(message, str):
            message = json.loads(message)
        obj = cls(message['name'], *message.get('args', ()), **message.get('kwargs', {}))
        return obj