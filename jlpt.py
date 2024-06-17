from csv_utils import read_csv, write_csv

A_DAN = ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ", "が", "ざ", "だ", "ば", "ぱ", "ゃ"]
I_DAN = ["い", "き", "し", "ち", "に", "ひ", "み", "い", "り", "ゐ", "ぎ", "じ", "ぢ", "び", "ぴ", "ぃ"]
U_DAN = ["う", "く", "す", "つ", "ぬ", "ふ", "む", "ゆ", "る", "う", "ぐ", "ず", "づ", "ぶ", "ぷ", "ゅ"]
E_DAN = ["え", "け", "せ", "て", "ね", "へ", "め", "え", "れ", "ゑ", "げ", "ぜ", "で", "べ", "ぺ", "ぇ"]
O_DAN = ["お", "こ", "そ", "と", "の", "ほ", "も", "よ", "ろ", "を", "ご", "ぞ", "ど", "ぼ", "ぽ", "ょ"]

HIRAGANA_AND_NUMBERS = A_DAN + I_DAN + U_DAN + E_DAN + O_DAN + ["ん"] + [*"0123456789"]

# data = read_csv("jlpt_grammar.csv", encoding="utf-8-sig")
# data = [[r[3], r[2]] for r in data[1:] if "\n" in r[2]]

data = read_csv("jlpt_vocab.csv", encoding="utf-8-sig")
data = [[r[3], r[2]] for r in data[1:] if "\n" in r[2]]

# data = read_csv("jlpt_kanji.csv", encoding="utf-8-sig")
# data = [[r[2], r[4], r[5]] for r in data[1:] if "\n" in r[4] or r[5] != ""]

_type = "goi"  # goi | grammar | kanji

questions = {}


def is_answer(t: str) -> bool:
    return t.split()[0] == "Question"


def get_page_id(p: str) -> str:
    return f"{p.split()[1]}-{p.split()[-1]}"


def get_question_id(p: str, t: str) -> str:
    return f"{get_page_id(p)}-{t.split('.')[0]}"


def process_answer(p: str, t: str):
    for r in t.split("\n"):
        num = r.split(": ")[0].split()[1]
        try:
            ans = int(r.split(": ")[1]) - 1
        except ValueError:
            ans = int(r.split(": ")[1][0]) - 1
        questions[f"{get_page_id(p)}-{num}"]["answer"] = [questions[f"{get_page_id(p)}-{num}"]["options"][ans]]


def process_question(_t: str, _id: str, t: str, u: str):
    if _t == "kanji":
        _ty = "表記"
        if len([ji for ji in u if ji not in HIRAGANA_AND_NUMBERS]) > 0:
            _ty = "漢字読み"
    elif _t == "goi":
        _ty = "文脈規定"
        if "_______" in t:
            _ty = "言い換え類義"
    else:
        _ty = "文法の形式の判断"
        if "「１」" in t:
            _ty = "文章の文法"
        elif "★" in t:
            _ty = "文の組み立て"
    question = "\n".join(t.split("\n")[:-4]).split(". ")[1].replace("\u3000", "").replace("\x81", " ")
    if _t == "kanji":
        question = f"{question}({u})"
    questions[_id] = {
        "question": question,
        "options": t.split("\n ")[-4:],
        "type": _ty,
        "level": _id.split("-")[0],
        "id": _id
    }
    pass


if __name__ == "__main__":
    q = ""
    for row in data:
        page = row[0]
        text = row[1]
        if is_answer(text):
            process_answer(page, text)
        else:
            if _type == "kanji" and len(text.split(". ")) < 2:
                q = text
                continue
            underline = ""
            if _type == "kanji":
                underline = row[2]
                if underline == "":
                    underline = text.split("\n")[0].split(". ")[1]
                    text = "\n".join([". ".join([text.split(". ")[0], q])] + text.split("\n")[1:])
            question_id = get_question_id(page, text)
            if len(question_id) > 8:
                raise ValueError
            process_question(_type, question_id, text, underline)
    export = [[value["question"]] + value["options"] + value["answer"] + [value["type"], value["level"], value["id"]]
              for value in questions.values()]
    write_csv("jlpt_n2_vocab.csv", export, encoding="utf-8-sig")
