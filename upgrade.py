import os
from json_utils import read_json, write_json
from question_utils import JLPT_FILEPATH, QUESTIONS_FILEPATH


def append_last_false(filepath):
    if os.path.exists(filepath):
        data = read_json(filepath)
        for k in data.keys():
            data[k]["last_false"] = False
        write_json(filepath, data)


if __name__ == "__main__":
    append_last_false(JLPT_FILEPATH)
    append_last_false(QUESTIONS_FILEPATH)
