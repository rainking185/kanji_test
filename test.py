import sys

from random import shuffle
from datetime import datetime
from question_utils import select_questions, update_questions, split_questions

sys.stdout.reconfigure(encoding='utf-8')

if __name__ == '__main__':
    take_jlpt = False
    try:
        if sys.argv[2] == "jlpt":
            take_jlpt = True
    except IndexError:
        pass
    try:
        num = int(sys.argv[1])
        if num == 0:
            split_questions(take_jlpt)
            quit()
    except IndexError:
        num = 100

    selected_questions = select_questions(num, take_jlpt)
    score = 0
    count = len(selected_questions.keys())
    wrong_questions = []
    try:
        for i, question in enumerate(selected_questions.keys()):
            detail = selected_questions[question]
            answers = detail["answers"]
            answers_display = "/".join(detail["answers"])
            tags = ",".join(detail["tags"])
            print(f'{i + 1}/{count}.{question}({tags})')
            if detail["type"] == "mcq":
                options = detail["options"]
                shuffle(options)
                for j, option in enumerate(options):
                    print(f"{j + 1}. {option}")
            attempt = ""
            while attempt == "" or (detail["type"] == "mcq" and attempt not in [*"1234"]):
                attempt = input()
            detail["attempt"] += 1
            if detail["type"] == "mcq":
                attempt = options[int(attempt) - 1]
            if attempt in answers:
                score += 1
                detail["attempt_logs"].append([datetime.today().strftime('%Y/%m/%d'), True])
                print("正解！")
            else:
                detail["false"] += 1
                detail["attempt_logs"].append([datetime.today().strftime('%Y/%m/%d'), False])
                wrong_questions.append(question)
                print(f"違います。正解は\"{answers_display}\"です。")

        update_questions(selected_questions, take_jlpt)
        print(f"テスト結果：{score}/{count}")
        with open("results.txt", "a+", newline="") as outfile:
            outfile.write(
                f"{datetime.today().strftime('%Y/%m/%d')}\t{score}/{len(selected_questions.keys())}\t{'jlpt' if take_jlpt else 'kanji'}\n")

        if len(wrong_questions) == 0:
            print("全問正解です！")
        else:
            print("続けるのは間違った問題です。")
            while len(wrong_questions) > 0:
                shuffle(wrong_questions)
                for question in wrong_questions:
                    detail = selected_questions[question]
                    answers = detail["answers"]
                    answers_display = "/".join(detail["answers"])
                    tags = ",".join(detail["tags"])
                    print(f"{question}({tags})")
                    if detail["type"] == "mcq":
                        options = detail["options"]
                        shuffle(options)
                        for j, option in enumerate(options):
                            print(f"{j + 1}. {option}")
                    attempt = ""
                    while attempt == "" or (detail["type"] == "mcq" and attempt not in [*"1234"]):
                        attempt = input()
                    if detail["type"] == "mcq":
                        attempt = options[int(attempt) - 1]
                    if attempt in answers:
                        wrong_questions.remove(question)
                        print("正解！")
                    else:
                        print(f"違います。正解は\"{answers_display}\"です。")
        print("終了！お疲れさまでした。")

    except KeyboardInterrupt:
        print("バイバイ")
