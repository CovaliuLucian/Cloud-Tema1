import json


class Metric:
    def __init__(self, total, failed, avg_latency, min_latency, max_latency):
        self.total = total
        self.failed = failed
        self.avg_latency = avg_latency
        self.min_latency = min_latency
        self.max_latency = max_latency


class Metrics:
    def __init__(self, translation, random, se):
        self.translation = translation
        self.random = random
        self.se = se

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
