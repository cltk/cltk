"""For loading TLG .json files and searching, then pulling author ids."""

import json
import os
from typing import Optional

import regex
from regex import Pattern

from cltk.corpora.grc.tlg.author_date import MAP_DATE_TO_AUTHORS
from cltk.corpora.grc.tlg.author_epithet import MAP_EPITHET_TO_AUTHOR_IDS
from cltk.corpora.grc.tlg.author_female import AUTHOR_FEMALE
from cltk.corpora.grc.tlg.author_geo import AUTHOR_GEO
from cltk.corpora.grc.tlg.id_author import ID_AUTHOR
from cltk.corpora.grc.tlg.index_lists import ALL_TLG_INDICES
from cltk.corpora.grc.tlg.work_numbers import WORK_NUMBERS

__author__ = [
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Stephen Margheim <stephen.margheim@gmail.com>",
    "Martín Pozzi <marpozzi@gmail.com>",
]
__license__ = "MIT License. See LICENSE."

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def get_female_authors() -> set[str]:
    """Open female authors index and return ordered
    set of author ids."""
    return set(AUTHOR_FEMALE["Femina"])


def get_epithet_index() -> dict[str, set[str]]:
    """Return dict of epithets (key) to a set of all
    author ids of that epithet (value).
    """
    _dict: dict[str, set[str]] = dict()
    for key, val in MAP_EPITHET_TO_AUTHOR_IDS.items():
        _dict[key] = set(val)
    return _dict


def get_epithets() -> list[str]:
    """Return a list of all the epithet labels."""
    return sorted(MAP_EPITHET_TO_AUTHOR_IDS.keys())


def select_authors_by_epithet(query: str) -> set[str]:
    """Pass exact name (case-insensitive) of
    epithet name, return ordered set of author ids.
    """
    for epithet, ids in MAP_EPITHET_TO_AUTHOR_IDS.items():
        if epithet.casefold() == query.casefold():
            return set(ids)


def get_epithet_of_author(_id: str) -> str:
    """Pass author id and return the name of its associated epithet."""
    for epithet, ids in MAP_EPITHET_TO_AUTHOR_IDS.items():
        if _id in ids:
            return epithet


def get_geo_index() -> dict[str, set[str]]:
    """Get entire index of geographic name (key) and
    set of associated authors (value).
    """
    _dict: dict[str, set[str]] = dict()
    for key, val in MAP_EPITHET_TO_AUTHOR_IDS.items():
        _dict[key] = set(val)
    return _dict


def get_geographies() -> list[str]:
    """Return a list of all the epithet labels."""
    return sorted(AUTHOR_GEO.keys())


def select_authors_by_geo(query: str) -> set[str]:
    """Pass exact name (case-insensitive) of
    geography name, return ordered set of author ids.
    """
    for geo, ids in AUTHOR_GEO.items():
        if geo.casefold() == query.casefold():
            return set(ids)


def get_geo_of_author(_id: str) -> str:
    """Pass author id and return the name of its associated epithet."""
    for geo, ids in AUTHOR_GEO.items():
        if _id in ids:
            return geo


def get_lists() -> dict[str, dict[str, str]]:
    """Return all of the TLG's indices."""
    return ALL_TLG_INDICES


def get_id_author() -> dict[str, str]:
    """Returns entirety of id-author TLG index."""
    return ID_AUTHOR


def select_id_by_name(query) -> list[tuple[str, str]]:
    """Do a case-insensitive regex match on author name, returns TLG id."""
    id_author: dict[str, str] = get_id_author()
    comp: Pattern[str] = regex.compile(
        r"{}".format(query.casefold()), flags=regex.VERSION1
    )
    matches: list[tuple[str, str]] = list()
    for _id, author in id_author.items():
        match: list[str] = comp.findall(author.casefold())
        if match:
            matches.append((_id, author))
    return matches


def open_json(_file):
    """Loads the json file as a dictionary and returns it."""
    with open(_file) as f:
        return json.load(f)


def get_works_by_id(_id):
    """Pass author id and return a dictionary of its works."""
    return WORK_NUMBERS[_id]


def check_id(_id):
    """Pass author id and return a string with the author label"""
    return ID_AUTHOR[_id]


def get_date_author() -> dict[str, list[str]]:
    """Returns entirety of date-author index."""
    return MAP_DATE_TO_AUTHORS


def get_dates():
    """Return a list of all the date epithet labels."""
    map_date_to_authors: dict[str, list[str]] = get_date_author()
    return sorted(map_date_to_authors.keys())


def get_date_of_author(_id):
    """Pass author id and return the name of its associated date."""
    map_date_to_authors: dict[str, list[str]] = get_date_author()
    for date, ids in map_date_to_authors.items():
        if _id in ids:
            return date
    return None


def _get_epoch(_str) -> Optional[str]:
    """Take incoming string, return its epoch."""
    _return = None
    if _str.startswith("A.D. "):
        _return = "ad"
    elif _str.startswith("a. A.D. "):
        _return = None  # ?
    elif _str.startswith("p. A.D. "):
        _return = "ad"
    elif regex.match(r"^[0-9]+ B\.C\. *", _str):
        _return = "bc"
    elif regex.match(r"^a\. *[0-9]+ B\.C\. *", _str):
        _return = "bc"
    elif regex.match(r"^p\. *[0-9]+ B\.C\. *", _str):
        _return = None  # ?
    elif _str == "Incertum" or _str == "Varia":
        _return = _str
    return _return


def _check_number(_str) -> bool:
    """check if the string contains only a number followed by ?"""
    if regex.match(r"^[0-9]+\?*", _str):
        return True
    return False


def _handle_splits(_str: str) -> dict[str, Optional[str]]:
    """Check if incoming date has a '-' or '/', if so do stuff."""
    _str = _str.replace("/", "-")
    _tmp_dict: dict[str, Optional[str]] = dict()
    if "-" in _str:
        start, stop = _str.split("-")
        if _check_number(start):
            start = regex.sub(r"[0-9]+\?*", start, stop)
        elif _check_number(stop):
            stop = regex.sub(r"[0-9]+\?*", stop, start)
    else:
        start = _str
        stop = _str
    _tmp_dict["start_raw"] = start
    _tmp_dict["stop_raw"] = stop
    _tmp_dict["start_epoch"] = _get_epoch(start)
    _tmp_dict["stop_epoch"] = _get_epoch(stop)
    return _tmp_dict


def normalize_dates():
    """Experiment to make sense of TLG dates.
    TODO: start here, parse everything with pass
    """
    map_date_to_authors: dict[str, list[str]] = get_date_author()
    for tlg_date in map_date_to_authors:
        date = {}
        if tlg_date == "Varia":
            # give a homer-to-byz date for 'varia'
            pass
        elif tlg_date == "Incertum":
            # ?
            pass
        else:
            tmp_date = _handle_splits(tlg_date)
            date.update(tmp_date)
        print(date)
