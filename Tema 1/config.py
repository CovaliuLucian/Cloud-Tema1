import json


class Config:
    def __init__(self):
        with open('config.json', 'r') as f:
            self.data = json.load(f)
