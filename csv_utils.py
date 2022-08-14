import csv


def write_csv(filepath: str, content: list):
    with open(filepath, "w", newline="", encoding="UTF-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(content)


def read_csv(filepath: str) -> list:
    with open(filepath, "r", newline="", encoding="UTF-8") as infile:
        return list(csv.reader(infile))


def append_csv_row(filepath: str, row: any):
    with open(filepath, "a", newline="", encoding="UTF-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(row)


def append_csv_rows(filepath: str, rows: list):
    with open(filepath, "a", newline="", encoding="UTF-8") as outfile:
        writer = csv.writer(outfile)
        for row in rows:
            writer.writerow([row])
