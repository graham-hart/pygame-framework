import json
import os


def read_map(fn: str) -> dict[str, dict[str, str]]:
    path = f"./{fn}"
    if os.path.exists(path):
        with open(path, "r+") as file:
            data = file.read()
            return json.loads(data) if data != "" else {}
    else:
        f = open(path, "x")
        f.close()
        return {}


def write_map(tilemap: dict[str, dict[str, str]], fn: str):
    with open(f"./{fn}", "w") as file:
        file.write(json.dumps(tilemap))
