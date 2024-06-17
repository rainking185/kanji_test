from csv_utils import read_csv, write_csv

table = read_csv("verbs.csv", encoding="utf-8-sig")

COLUMNS = [
    "単語", "ひらがな", "JLPT", "種類", "グループ", "ます形", "て形", "た形", "ない形", "条件形", "受身動詞", "使役動詞", "命令形",
    "可能動詞", "意向形", "禁止形"
]
INDICES = {}

suffix = ["", "k", "s", "t", "n", "h", "m", "y", "r", "w", "g", "z", "d", "b", "p", "xy"]
A_DAN = ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ", "が", "ざ", "だ", "ば", "ぱ", "ゃ"]
I_DAN = ["い", "き", "し", "ち", "に", "ひ", "み", "い", "り", "ゐ", "ぎ", "じ", "ぢ", "び", "ぴ", "ぃ"]
U_DAN = ["う", "く", "す", "つ", "ぬ", "ふ", "む", "ゆ", "る", "う", "ぐ", "ず", "づ", "ぶ", "ぷ", "ゅ"]
E_DAN = ["え", "け", "せ", "て", "ね", "へ", "め", "え", "れ", "ゑ", "げ", "ぜ", "で", "べ", "ぺ", "ぇ"]
O_DAN = ["お", "こ", "そ", "と", "の", "ほ", "も", "よ", "ろ", "を", "ご", "ぞ", "ど", "ぼ", "ぽ", "ょ"]

HIRAGANA = tuple(A_DAN + I_DAN + U_DAN + E_DAN + O_DAN + ["ん"])

U_DAN_EXCEPT_RU = U_DAN.copy()
U_DAN_EXCEPT_RU.remove("る")
U_DAN_EXCEPT_RU = tuple(U_DAN_EXCEPT_RU)
SPECIAL_GROUP_1 = (
    "切る", "帰る", "走る", "嘲る", "焦る", "要る", "炒る", "煎る", "入る", "返る", "限る", "齧る", "覆る", "蹴る", "滑る", "散る",
    "遮る", "茂る", "湿る", "送る", "知る", "喋る", "照る", "握る", "練る", "罵る", "捻る", "耽る", "減る", "参る", "混じる",
    "漲る", "蘇る", "甦る"
)
SPECIAL_GROUP_3 = "来る"

for column in COLUMNS:
    INDICES[column] = table[0].index(column)

for row in table[1:]:
    if not row[INDICES["種類"]].endswith("動詞"):
        continue
    # データを読み取る
    word = row[INDICES["単語"]]
    hiragana = row[INDICES["ひらがな"]]
    group = ""
    masu = ""
    te = ""
    ta = ""
    nai = ""
    cmd = ""
    kinshi = ""
    ikou = ""
    ukemi = ""
    shieki = ""
    ba = ""
    # 動詞のグルーピング
    if not word.endswith(HIRAGANA):
        group = "3-外来語"
    elif word.endswith(SPECIAL_GROUP_3):
        group = "3-特例"
    elif hiragana.endswith(U_DAN_EXCEPT_RU):
        group = "1-う段る除き"
    elif hiragana.endswith(tuple([f"{h}る" for h in A_DAN + U_DAN + O_DAN])):
        group = "1-あうお段+る"
    elif word.endswith(SPECIAL_GROUP_1):
        group = "1-特例"
    elif hiragana.endswith("る"):
        group = "2-る"
    else:
        print(f"動詞のグルーピング：{word} is not considered")
    # 活用形の転換
    kinshi = f"{word}な"
    if group.startswith("1"):
        ending = word[-1]
        ikou = f"{word[:-1]}{O_DAN[U_DAN.index(ending)]}う"
        if hiragana == "おっしゃる":
            masu = f"{word[:-1]}います"
            nai = f"{masu[:-3]}らない"
            cmd = f"{word[:-1]}い"
        else:
            masu = f"{word[:-1]}{I_DAN[U_DAN.index(ending)]}ます"
            if ending == "う":
                nai = f"{word[:-1]}わない"
            else:
                nai = f"{word[:-1]}{A_DAN[U_DAN.index(ending)]}ない"
            cmd = f"{word[:-1]}{E_DAN[U_DAN.index(ending)]}"
        if ending in ["う", "つ", "る"] or hiragana == "いく":
            te = f"{word[:-1]}って"
        elif ending in ["む", "ぶ", "ぬ"]:
            te = f"{word[:-1]}んで"
        elif ending == "く":
            te = f"{word[:-1]}いて"
        elif ending == "ぐ":
            te = f"{word[:-1]}いで"
        elif ending == "す":
            te = f"{word[:-1]}して"
        else:
            print(f"て形グループ１：{word} is not considered")
        ukemi = f"{nai[:-2]}れる"
        shieki = f"{nai[:-2]}せる"
        ba = f"{word[:-1]}{E_DAN[U_DAN.index(ending)]}ば"
    elif group.startswith("2"):
        masu = f"{word[:-1]}ます"
        nai = f"{word[:-1]}ない"
        te = f"{word[:-1]}て"
        cmd = f"{word[:-1]}ろ"
        ikou = f"{word[:-1]}よう"
        ukemi = f"{nai[:-2]}られる"
        shieki = f"{nai[:-2]}させる"
        ba = f"{word[:-1]}れば"
    elif group.startswith("3"):
        if group == "3-外来語":
            masu = f"{word}します"
            te = f"{word}して"
            nai = f"{word}しない"
            cmd = f"{word}しろ"
            kinshi = f"{word}するな"
            ikou = f"{word}しよう"
            ukemi = f"{word}される"
            shieki = f"{word}させる"
            ba = f"{word}すれば"
        elif group == "3-特例":
            masu = "きます"
            nai = "こない"
            cmd = "こい"
            te = "きて"
            kinshi = "くるな"
            ikou = "こよう"
            ukemi = "こられる"
            shieki = "こさせる"
            ba = "くれば"
    else:
        print(f"活用形の転換：{word} is not considered")
    if te[-1] == "て":
        ta = f"{te[:-1]}た"
    elif te[-1] == "で":
        ta = f"{te[:-1]}だ"
    # テーブルに記入する
    row[INDICES["グループ"]] = group
    row[INDICES["ます形"]] = masu
    row[INDICES["て形"]] = te
    row[INDICES["た形"]] = ta
    row[INDICES["命令形"]] = cmd
    row[INDICES["禁止形"]] = kinshi
    row[INDICES["ない形"]] = nai
    row[INDICES["意向形"]] = ikou
    row[INDICES["受身動詞"]] = ukemi
    row[INDICES["使役動詞"]] = shieki
    row[INDICES["条件形"]] = ba
write_csv("verbs_filled.csv", table, encoding="utf-8-sig")
