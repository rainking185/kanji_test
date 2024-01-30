from question_utils import add_question

if __name__ == "__main__":
    end = False
    while not end:
        csv = ""
        question = ""
        res = ""
        while csv == "" or len(csv.split(",")) < 4:
            print("CSVを入力してください。")
            csv = input()
        csv_split = csv.split(",")
        kanji = csv_split[0]
        kana = csv_split[2]
        vocabs = csv_split[3:]
        for vocab in vocabs:
            add_question(f'\'{vocab}\'の\'{kanji}\'の仮名は何ですか？', "answer", [kana], ["N2"])
        print("新しい問題の入力が完成しました。")
        # question = ""
        # t = ""
        # answers = []
        # tags = []
        # res = ""
        # while question == "":
        #     print("問題を入力してください。")
        #     question = input()
        # while t not in ["answer", "mcq"]:
        #     print("問題の種類を選んで入力してください。「answer, mcq」")
        #     t = input().lower()
        # while (t == "answer" and len(answers) < 1) or (t == "mcq" and len(answers) < 2):
        #     print("答えを入力してください。多数の答えは「；」を分けてください。")
        #     answers = input().replace("；", ";").split(";")
        # print("問題のタグを入力してください。多数のタグは「；」を分けてください。")
        # tags = input().replace("；", ";").split(";")
        # add_question(question, t, answers, tags)
        # print("新しい問題の入力が完成しました。")
        print("次の問題を入力しますか？(Y/n)")
        res = input().lower()
        if res == "n":
            end = True
    print("お疲れさまでした。")
