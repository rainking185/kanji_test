import sys
from pathlib import Path
from question_utils import get_ids, merge_questions
from csv_utils import read_csv


def prepare_data(data: list, batch="", has_heading=True) -> dict:
    if has_heading:
        data = data[1:]
    all_questions = {}
    for row in data:
        while "" in row:
            row.remove("")
        kanji = row[0]
        kana = row[2]
        if len(row) <= 3:
            key = f"{kanji}-{kanji}"
            if key in all_questions.keys():
                if kana not in all_questions[key]["kana"]:
                    all_questions[key]["kana"].append(kana)
            else:
                all_questions[key] = {
                    "vocab": kanji,
                    "kanji": kanji,
                    "kana": [kana],
                    "attempt": 0,
                    "false": 0,
                    "last_attempt": "",
                    "batch": [batch]
                }
        else:
            vocabs = row[3:]
            for vocab in vocabs:
                key = f"{vocab}-{kanji}"
                if key in all_questions.keys():
                    if kana not in all_questions[key]["kana"]:
                        all_questions[key]["kana"].append(kana)
                else:
                    all_questions[key] = {
                        "vocab": vocab,
                        "kanji": kanji,
                        "kana": [kana],
                        "attempt": 0,
                        "false": 0,
                        "last_attempt": "",
                        "batch": [batch]
                    }
    return all_questions


def import_kanji(filepath: str):
    kanji_data = read_csv(filepath)
    imported_questions = prepare_data(kanji_data, batch=Path(filepath).stem)
    merge_questions(imported_questions)


if __name__ == "__main__":
    import_kanji(sys.argv[1])
