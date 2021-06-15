import json

def load(fileName):
    try:
        with open(fileName) as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")