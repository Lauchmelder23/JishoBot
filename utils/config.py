import json

config = None
with open("config.json") as file:
    config = json.load(file)

if config is None:
    raise "Failed to load config file"

def get(key: str) -> str:
    return config[key]