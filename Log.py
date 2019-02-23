import datetime
import uuid


class Log:
    def __init__(self, latency, response, success, request):
        self.id = str(uuid.uuid4())
        self.date = str(datetime.datetime.now())
        self.latency = latency
        self.success = success
        self.response = response
        self.request = request
