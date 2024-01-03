import re
import os

from django.conf import settings


def strip_trailing_year(string: str) -> str:
    return re.sub(r"\d\d\d\d$", "", string).strip()


def get_dependency_version(dependency: str) -> str:
    path = os.path.join(settings.BASE_DIR, "party", "templates", "party", "base.html")
    with open(path, "r") as raw_data:
        data = raw_data.readlines()
    try:
        depe = [x for x in data if dependency in x][0]
    except IndexError:
        return ""
    try:
        return re.search(r"\d+\.\d+\.\d+", depe).group()
    except AttributeError:
        return ""
