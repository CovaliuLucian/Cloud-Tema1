import json
from urllib import parse
from sqlalchemy.ext.declarative import DeclarativeMeta


class Utilities:
    @staticmethod
    def get_args(path):
        args = {}
        idx = path.find('?')
        if idx >= 0:
            rpath = path[:idx]
            args = parse.parse_qs(path[idx + 1:])
        else:
            rpath = path
        return rpath, args


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
