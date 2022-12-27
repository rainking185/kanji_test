import sys

from datetime import datetime
from question_utils import select_questions, update_questions

if __name__ == '__main__':

    try:
        num = int(sys.argv[1])
    except IndexError:
        num = 30

    selected_questions = select_questions(num)
    score = 0
    count = 0
    try:
        for i, question in enumerate(selected_questions.values()):
            vocab = question["vocab"]
            kanji = question["kanji"]
            kana = question["kana"]
            kana_display = "/".join(kana)
            batch = ",".join(question["batch"])
            print(f'{i + 1}.\'{vocab}\'の\'{kanji}\'の仮名は何ですか？({batch})')
            attempt = input()
            question["attempt"] += 1
            question["last_attempt"] = datetime.today().strftime('%Y/%m/%d')
            if attempt in kana:
                score += 1
                print("正解！")
            else:
                question["false"] += 1
                print(f"違います。正解は\"{kana_display}\"です。")
        update_questions(selected_questions)
        print(f"テスト結果：{score}/{len(selected_questions.keys())}")
        with open("results.txt", "a+", newline="") as outfile:
            outfile.write(f"{datetime.today().strftime('%Y/%m/%d')}\t{score}/{len(selected_questions.keys())}\n")

    except KeyboardInterrupt:
        print("バイバイ。")
