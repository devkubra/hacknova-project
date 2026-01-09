import json

def load_incidents():
    with open("data/incidents.json", "r") as f:
        return json.load(f)
