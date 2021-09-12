import json


def read_map(path):
    with open(path) as f:
        obj = json.loads(f.read())
        return obj
