import json


def createdict(filename):
  with open(filename) as jsonfile:
    data = jsonfile.read()
  return json.loads(data)
