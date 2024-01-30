import os
from datetime import datetime
from json_utils import read_json, write_json, shuffle_json

QUESTIONS_FILEPATH = "questions.json"
JLPT_FILEPATH = "jlpt.json"

if not os.path.exists(QUESTIONS_FILEPATH):
    write_json(QUESTIONS_FILEPATH, {})
QUESTIONS = read_json(QUESTIONS_FILEPATH)

if not os.path.exists(JLPT_FILEPATH):
    write_json(JLPT_FILEPATH, {})
JLPT = read_json(JLPT_FILEPATH)
THRESHOLD = 0.5


def split_old_questions_with_threshold(questions: dict, jlpt=False) -> (dict, dict):
    rate_table = []
    over_threshold = {}
    under_threshold = {}
    for _id in questions:
        rate = questions[_id]["false"] / questions[_id]["attempt"]
        last_attempt = questions[_id]["attempts_logs"][-1]
        day_diff = (datetime.today() - datetime.strptime(last_attempt, "%Y/%m/%d")).days
        if questions[_id]["attempt"] >= pow(2 if jlpt else 3, questions[_id]["false"] + 1) or (rate <= THRESHOLD and not questions[_id]["last_false"] and (
                day_diff < questions[_id]["attempt"] * 60 if jlpt else day_diff < pow(questions[_id]["attempt"], 2))):
            under_threshold[_id] = questions[_id]
        else:
            over_threshold[_id] = questions[_id]
            rate_table.append([_id, rate])
    rate_table.sort(key=lambda x: x[1])
    under_threshold = shuffle_json(under_threshold)
    print(f"Found {len(over_threshold.keys())} questions to revise and {len(under_threshold.keys())} other questions.")
    return over_threshold, under_threshold


def split_questions(jlpt=False) -> (dict, dict, dict):
    old_questions = {}
    new_questions = {}
    for _id in (QUESTIONS if not jlpt else JLPT):
        if (QUESTIONS if not jlpt else JLPT)[_id]["attempt"] > 0:
            old_questions[_id] = (QUESTIONS if not jlpt else JLPT)[_id]
        else:
            new_questions[_id] = (QUESTIONS if not jlpt else JLPT)[_id]
    questions2revise, ok_questions = split_old_questions_with_threshold(old_questions, jlpt)
    new_questions = shuffle_json(new_questions)
    print(f"Found {len(new_questions.keys())} new questions.")
    return questions2revise, new_questions, ok_questions


def select_questions(num=10, jlpt=False) -> dict:
    questions2revise, new_questions, ok_questions = split_questions(jlpt)
    selected_questions = {}
    if len(questions2revise.keys()) >= num:
        i = 0
        for _id in questions2revise:
            selected_questions[_id] = questions2revise[_id]
            i += 1
            if i == num:
                break
        return shuffle_json(selected_questions)
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
        return shuffle_json(selected_questions)
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
        return shuffle_json(selected_questions)
    else:
        selected_questions.update(ok_questions)
    return shuffle_json(selected_questions)


def get_questions(jlpt=False) -> list:
    return list((QUESTIONS if not jlpt else JLPT).keys())


def merge_questions(imported_questions: dict, jlpt=False):
    global QUESTIONS, JLPT
    questions = get_questions()
    for question in imported_questions:
        if question not in questions:
            (QUESTIONS if not jlpt else JLPT)[question] = imported_questions[question]
        else:
            (QUESTIONS if not jlpt else JLPT)[question]["tags"].extend(imported_questions[question]["tags"])
            for answer in imported_questions[question]["answers"]:
                if answer not in (QUESTIONS if not jlpt else JLPT)[question]["answers"]:
                    (QUESTIONS if not jlpt else JLPT)[question]["answers"].append(answer)
    write_json(QUESTIONS_FILEPATH if not jlpt else JLPT_FILEPATH, QUESTIONS if not jlpt else JLPT)


def update_questions(selected_questions: dict, jlpt=False):
    (QUESTIONS if not jlpt else JLPT).update(selected_questions)
    write_json(QUESTIONS_FILEPATH if not jlpt else JLPT_FILEPATH, QUESTIONS if not jlpt else JLPT)


def add_question(new_question: str, t: str, answers: list, tags: list):
    global QUESTIONS
    questions = get_questions()
    if new_question not in questions:
        QUESTIONS[new_question] = {
            "type": t,
            "answers": answers,
            "tags": tags,
            "attempt": 0,
            "false": 0,
            "attempts_logs": [],
            "last_false": False
        }
    else:
        for tag in tags:
            if tag not in QUESTIONS[new_question]["tags"]:
                QUESTIONS[new_question]["tags"].append(tags)
        for answer in answers:
            if answer not in QUESTIONS[new_question]["answers"]:
                QUESTIONS[new_question]["answers"].append(answer)
    update_questions(QUESTIONS)


def last_attempt_to_list():
    for q in QUESTIONS.keys():
        QUESTIONS[q]["attempts_logs"] = [QUESTIONS[q]["last_attempt"]]
    for q in JLPT.keys():
        JLPT[q]["attempts_logs"] = [JLPT[q]["last_attempt"]]
    write_json(QUESTIONS_FILEPATH, QUESTIONS)
    write_json(JLPT_FILEPATH, JLPT)
    

if __name__ == "__main__":
    last_attempt_to_list()