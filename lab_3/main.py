import csv
import re
from typing import Dict
from checksum import serialize_result, calculate_checksum

PATTERNS = {
    "telephone": re.compile(r"^[+]7?-[(][0-9]{3}[)]-[0-9]{3}-[0-9]{2}-[0-9]{2}$"),
    "height": re.compile(r"^[0-9][.][0-9]{2}$"),
    "snils": re.compile(r"^[0-9]{11}$"),
    "identifier": re.compile(r"^[0-9]{2}-[0-9]{2}/[0-9]{2}$"),
    "occupation": re.compile(r"^[a-zA-Zа-яА-Я- ]+$"),
    "longitude": re.compile(r"^-?([0-9]|[1-9][0-9]|1[0-8][0-9])[.][0-9]{1,6}$"),
    "blood_type": re.compile(r"^(O|A|B|AB)[+\u2212]$"),
    "issn": re.compile(r"^[0-9]{4}-[0-9]{4}$"),
    "locale_code": re.compile(r"^[a-z]{2,3}(-[a-zA-Z]+){0,2}$"),
    "date": re.compile(r"^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])$"),
}


def is_valid_row(row: Dict[str, str]) -> bool:
    for k in row.keys():
        if not PATTERNS[k].match(row[k]):
            return False
    return True


def main(filename: str) -> None:
    invalid_rows = []
    with open(filename, encoding="utf-16") as f:
        reader = csv.DictReader(f, delimiter=";", quotechar='"')
        for i, row in enumerate(reader):
            if not is_valid_row(row):
                invalid_rows.append(i)
    print("Найдено неверных записей:", len(invalid_rows))
    print("Контрольная сумма:", checksum := calculate_checksum(invalid_rows))
    serialize_result(4, checksum)


if __name__ == "__main__":
    main("./4.csv")