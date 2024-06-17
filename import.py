import sys
from pathlib import Path
from question_utils import merge_questions
from csv_utils import read_csv


def prepare_data(data: list, batch="", has_heading=True) -> dict:
    if has_heading:
        data = data[1:]
    all_questions = {}
    for row in data:
        while "" in row:
            row.remove("")
        kanji = row[0]
        answer = row[2]
        if len(row) <= 3:
            question = f'\'{kanji}\'の\'{kanji}\'の仮名は何ですか？'
            if question in all_questions.keys():
                if answer not in all_questions[question]["answers"]:
                    all_questions[question]["answers"].append(answer)
            else:
                all_questions[question] = {
                    "type": "answer",
                    "answers": [answer],
                    "tags": [batch],
                    "attempt": 0,
                    "false": 0,
                    "attempt_logs": []
                }
        else:
            vocabs = row[3:]
            for vocab in vocabs:
                question = f'\'{vocab}\'の\'{kanji}\'の仮名は何ですか？'
                if question in all_questions.keys():
                    if answer not in all_questions[question]["answers"]:
                        all_questions[question]["answers"].append(answer)
                else:
                    all_questions[question] = {
                        "type": "answer",
                        "answers": [answer],
                        "tags": [batch],
                        "attempt": 0,
                        "false": 0,
                        "attempt_logs": []
                    }
    return all_questions


def import_kanji(filepath: str):
    kanji_data = read_csv(filepath)
    imported_questions = prepare_data(kanji_data, batch=Path(filepath).stem)
    merge_questions(imported_questions)


def import_jlpt(filepath: str):
    data = read_csv(filepath, encoding="utf-8-sig")
    all_questions = {}
    for row in data:
        all_questions[row[0]] = {
            "type": "mcq",
            "options": row[1:5],
            "answers": [row[5]],
            "tags": row[6:],
            "attempt": 0,
            "false": 0,
            "attempt_logs": []
        }
    merge_questions(all_questions, jlpt=True)


if __name__ == "__main__":
    # import_kanji(sys.argv[1])
    import_jlpt("jlpt_n2_kanji.csv")
    import_jlpt("jlpt_n2_grammar.csv")
    import_jlpt("jlpt_n2_vocab.csv")
