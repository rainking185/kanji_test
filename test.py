import sys

from random import shuffle
from datetime import datetime
from question_utils import select_questions, update_questions

if __name__ == '__main__':

    try:
        num = int(sys.argv[1])
    except IndexError:
        num = 50

    selected_questions = select_questions(num)
    score = 0
    count = len(selected_questions.keys())
    wrong_questions = []
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
                wrong_questions.append(question)
                print(f"違います。正解は\"{kana_display}\"です。")

        update_questions(selected_questions)
        print(f"テスト結果：{score}/{count}")
        with open("results.txt", "a+", newline="") as outfile:
            outfile.write(f"{datetime.today().strftime('%Y/%m/%d')}\t{score}/{len(selected_questions.keys())}\n")

        print("続けるのは間違った問題です。")
        while len(wrong_questions) > 0:
            shuffle(wrong_questions)
            for question in wrong_questions:
                vocab = question["vocab"]
                kanji = question["kanji"]
                kana = question["kana"]
                kana_display = "/".join(kana)
                batch = ",".join(question["batch"])
                print(f'\'{vocab}\'の\'{kanji}\'の仮名は何ですか？({batch})')
                attempt = input()
                if attempt in kana:
                    wrong_questions.remove(question)
                    print("正解！")
                else:
                    print(f"違います。正解は\"{kana_display}\"です。")
        print("終了！お疲れさまでした。")


    except KeyboardInterrupt:
        print("バイバイ。")
