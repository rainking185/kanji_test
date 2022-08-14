from datetime import datetime
from json_utils import read_json, write_json, shuffle_json

QUESTIONS_FILEPATH = "questions.json"
QUESTIONS = read_json(QUESTIONS_FILEPATH)
THRESHOLD = 0.4


def split_old_questions_with_threshold(questions: dict) -> (dict, dict):
    rate_table = []
    over_threshold = {}
    under_threshold = {}
    for id in questions:
        rate = questions[id]["false"] / questions[id]["attempt"]
        day_diff = (datetime.today() - datetime.strptime(questions[id]["last_attempt"], "%Y/%m/%d")).days
        if rate <= THRESHOLD and day_diff < pow(questions[id]["attempt"], 2):
            under_threshold[id] = questions[id]
        else:
            over_threshold[id] = questions[id]
            rate_table.append([id, rate])
    rate_table.sort(key=lambda x: x[1])
    under_threshold = shuffle_json(under_threshold)
    print(f"Found {len(over_threshold.keys())} questions to revise and {len(under_threshold.keys())} other questions.")
    return over_threshold, under_threshold


def split_questions() -> (dict, dict, dict):
    old_questions = {}
    new_questions = {}
    for id in QUESTIONS:
        if QUESTIONS[id]["attempt"] > 0:
            old_questions[id] = QUESTIONS[id]
        else:
            new_questions[id] = QUESTIONS[id]
    questions2revise, ok_questions = split_old_questions_with_threshold(old_questions)
    new_questions = shuffle_json(new_questions)
    print(f"Found {len(new_questions.keys())} new questions.")
    return questions2revise, new_questions, ok_questions


def select_questions(num=10) -> dict:
    questions2revise, new_questions, ok_questions = split_questions()
    selected_questions = {}
    if len(questions2revise.keys()) >= num:
        i = 0
        for id in questions2revise:
            selected_questions[id] = questions2revise[id]
            i += 1
            if i == num:
                break
        return selected_questions
    else:
        selected_questions = questions2revise
    extra = num - len(questions2revise.keys())
    if len(new_questions.keys()) >= extra:
        i = 0
        for id in new_questions:
            selected_questions[id] = new_questions[id]
            i += 1
            if i == extra:
                break
        return selected_questions
    else:
        selected_questions.update(new_questions)
    extra -= len(new_questions.keys())
    if len(ok_questions.keys()) >= extra:
        i = 0
        for id in ok_questions:
            selected_questions[id] = ok_questions[id]
            i += 1
            if i == extra:
                break
        return selected_questions
    else:
        selected_questions.update(ok_questions)
    return selected_questions


def get_ids() -> list:
    return list(QUESTIONS.keys())


def append_questions(new_questions: dict):
    global QUESTIONS
    QUESTIONS.update(new_questions)
    write_json(QUESTIONS_FILEPATH, QUESTIONS)


def update_questions(selected_questions: dict):
    QUESTIONS.update(selected_questions)
    write_json(QUESTIONS_FILEPATH, QUESTIONS)


if __name__ == "__main__":
    get_questions_false_rate(QUESTIONS)
