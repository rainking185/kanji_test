import sys
from question_utils import get_ids, append_questions
from csv_utils import read_csv


def prepare_data(data: list, has_heading=True) -> dict:
    if has_heading:
        data = data[1:]
    all_questions = {}
    for row in data:
        while "" in row:
            row.remove("")
        kanji = row[0]
        kana = row[2]
        if len(row) <= 3:
            all_questions[f"{kanji}-{kanji}-{kana}"] = {
                "vocab": kanji,
                "kanji": kanji,
                "kana": kana,
                "attempt": 0,
                "false": 0,
                "last_attempt": ""
            }
        else:
            vocabs = row[3:]
            for vocab in vocabs:
                all_questions[f"{vocab}-{kanji}-{kana}"] = {
                    "vocab": vocab,
                    "kanji": kanji,
                    "kana": kana,
                    "attempt": 0,
                    "false": 0,
                    "last_attempt": ""
                }
    return all_questions


def import_kanji(filepath: str):
    kanji_data = read_csv(filepath)
    ids = get_ids()
    imported_questions = prepare_data(kanji_data)
    new_questions = {}
    for id in imported_questions:
        if id not in ids:
            new_questions[id] = imported_questions[id]
    append_questions(new_questions)


if __name__ == "__main__":
    import_kanji(sys.argv[1])
