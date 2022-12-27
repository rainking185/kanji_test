import os
from datetime import datetime
from json_utils import read_json, write_json, shuffle_json

QUESTIONS_FILEPATH = "questions.json"

if not os.path.exists(QUESTIONS_FILEPATH):
    write_json(QUESTIONS_FILEPATH, {})
QUESTIONS = read_json(QUESTIONS_FILEPATH)
THRESHOLD = 0.4


def split_old_questions_with_threshold(questions: dict) -> (dict, dict):
    rate_table = []
    over_threshold = {}
    under_threshold = {}
    for _id in questions:
        rate = questions[_id]["false"] / questions[_id]["attempt"]
        day_diff = (datetime.today() - datetime.strptime(questions[_id]["last_attempt"], "%Y/%m/%d")).days
        if rate <= THRESHOLD and day_diff < pow(questions[_id]["attempt"], 2):
            under_threshold[_id] = questions[_id]
        else:
            over_threshold[_id] = questions[_id]
            rate_table.append([_id, rate])
    rate_table.sort(key=lambda x: x[1])
    under_threshold = shuffle_json(under_threshold)
    print(f"Found {len(over_threshold.keys())} questions to revise and {len(under_threshold.keys())} other questions.")
    return over_threshold, under_threshold


def split_questions() -> (dict, dict, dict):
    old_questions = {}
    new_questions = {}
    for _id in QUESTIONS:
        if QUESTIONS[_id]["attempt"] > 0:
            old_questions[_id] = QUESTIONS[_id]
        else:
            new_questions[_id] = QUESTIONS[_id]
    questions2revise, ok_questions = split_old_questions_with_threshold(old_questions)
    new_questions = shuffle_json(new_questions)
    print(f"Found {len(new_questions.keys())} new questions.")
    return questions2revise, new_questions, ok_questions


def select_questions(num=10) -> dict:
    questions2revise, new_questions, ok_questions = split_questions()
    selected_questions = {}
    if len(questions2revise.keys()) >= num:
        i = 0
        for _id in questions2revise:
            selected_questions[_id] = questions2revise[_id]
            i += 1
            if i == num:
                break
        return selected_questions
    else:
        selected_questions = questions2revise
    extra = num - len(questions2revise.keys())
    if len(new_questions.keys()) >= extra:
        i = 0
        for _id in new_questions:
            selected_questions[_id] = new_questions[_id]
            i += 1
            if i == extra:
                break
        return selected_questions
    else:
        selected_questions.update(new_questions)
    extra -= len(new_questions.keys())
    if len(ok_questions.keys()) >= extra:
        i = 0
        for _id in ok_questions:
            selected_questions[_id] = ok_questions[_id]
            i += 1
            if i == extra:
                break
        return selected_questions
    else:
        selected_questions.update(ok_questions)
    return shuffle_json(selected_questions)


def get_ids() -> list:
    return list(QUESTIONS.keys())


def merge_questions(imported_questions: dict):
    global QUESTIONS
    ids = get_ids()
    for _id in imported_questions:
        if _id not in ids:
            QUESTIONS[_id] = imported_questions[_id]
        else:
            QUESTIONS[_id]["batch"].extend(imported_questions[_id]["batch"])
            for kana in imported_questions[_id]:
                if kana not in QUESTIONS[_id]["kana"]:
                    QUESTIONS[_id]["kana"].append(kana)
    write_json(QUESTIONS_FILEPATH, QUESTIONS)


def update_questions(selected_questions: dict):
    QUESTIONS.update(selected_questions)
    write_json(QUESTIONS_FILEPATH, QUESTIONS)
