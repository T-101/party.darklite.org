import re


def strip_trailing_year(string: str) -> str:
    return re.sub(r"\d\d\d\d$", "", string).strip()
