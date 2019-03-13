from urllib import parse


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
