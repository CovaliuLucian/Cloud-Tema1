import json
from Util import AlchemyEncoder


class Response:
    def __init__(self, success, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error

    def to_json(self):
        return json.dumps(self.__dict__, cls=AlchemyEncoder).encode()
