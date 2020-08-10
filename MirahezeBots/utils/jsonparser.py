import json


def createdict(filename):
    with open(filename) as jsonfile:
        data = jsonfile.read()
    return json.loads(data)


def validatecache(filename, dict):
    cached = createdict(filename)
    if cached == dict:
        return True
    else:
        return False
