import json
from random import shuffle


def read_json(filepath: str) -> dict:
    with open(filepath, "r", newline="", encoding="UTF-8") as infile:
        return json.load(infile)


def write_json(filepath: str, data: dict):
    with open(filepath, "w", newline="", encoding="UTF-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)


def shuffle_json(data: dict) -> dict:
    ids = list(data.keys())
    shuffle(ids)
    shuffled_json = {}
    for id in ids:
        shuffled_json[id] = data[id]
    return shuffled_json
