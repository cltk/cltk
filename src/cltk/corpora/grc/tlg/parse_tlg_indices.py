"""For loading TLG .json files and searching, then pulling author ids.
"""

import json
import os

import regex

from cltk.corpora.grc.tlg.author_date import AUTHOR_DATE
from cltk.corpora.grc.tlg.author_epithet import AUTHOR_EPITHET
from cltk.corpora.grc.tlg.author_female import AUTHOR_FEMALE
from cltk.corpora.grc.tlg.author_geo import AUTHOR_GEO
from cltk.corpora.grc.tlg.id_author import ID_AUTHOR
from cltk.corpora.grc.tlg.index_lists import INDEX_LIST
from cltk.corpora.grc.tlg.work_numbers import WORK_NUMBERS

__author__ = [
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Stephen Margheim <stephen.margheim@gmail.com>",
    "Martín Pozzi <marpozzi@gmail.com>",
]
__license__ = "MIT License. See LICENSE."

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# Gender
def get_female_authors():
    """Open female authors index and return ordered set of author ids."""
    return set(AUTHOR_FEMALE["Femina"])


# Epithet
def get_epithet_index():
    """Return dict of epithets (key) to a set of all author ids of that
    epithet (value).
    """
    _dict = {}
    for k, v in AUTHOR_EPITHET.items():
        _dict[k] = set(v)
    return _dict


def get_epithets():
    """Return a list of all the epithet labels."""
    return sorted(AUTHOR_EPITHET.keys())


def select_authors_by_epithet(query):
    """Pass exact name (case insensitive) of epithet name, return ordered set
    of author ids.
    """

    for epithet, ids in AUTHOR_EPITHET.items():
        if epithet.casefold() == query.casefold():
            return set(ids)


def get_epithet_of_author(_id):
    """Pass author id and return the name of its associated epithet."""
    for epithet, ids in AUTHOR_EPITHET.items():
        if _id in ids:
            return epithet


# Geography
def get_geo_index():
    """Get entire index of geographic name (key) and set of associated authors
    (value).
    """
    _dict = {}
    for k, v in AUTHOR_EPITHET.items():
        _dict[k] = set(v)

    return _dict


def get_geographies():
    """Return a list of all the epithet labels."""
    return sorted(AUTHOR_GEO.keys())


def select_authors_by_geo(query):
    """Pass exact name (case insensitive) of geography name, return ordered set
    of author ids.
    """
    for geo, ids in AUTHOR_GEO.items():
        if geo.casefold() == query.casefold():
            return set(ids)


def get_geo_of_author(_id):
    """Pass author id and return the name of its associated epithet."""
    for geo, ids in AUTHOR_GEO.items():
        if _id in ids:
            return geo


# List of TLG indices
def get_lists():
    """A list of the TLG's lists."""
    return INDEX_LIST


# Master author index (`id_author.json`)
def get_id_author():
    """Returns entirety of id-author TLG index."""
    return ID_AUTHOR


def select_id_by_name(query):
    """Do a case-insensitive regex match on author name, returns TLG id."""
    id_author = get_id_author()
    comp = regex.compile(r"{}".format(query.casefold()), flags=regex.VERSION1)
    matches = []
    for _id, author in id_author.items():
        match = comp.findall(author.casefold())
        if match:
            matches.append((_id, author))
    return matches


def open_json(_file):
    """Loads the json file as a dictionary and returns it."""
    with open(_file) as f:
        return json.load(f)


# Work numbers
def get_works_by_id(_id):
    """Pass author id and return a dictionary of its works."""
    return WORK_NUMBERS[_id]


# Check id
def check_id(_id):
    """Pass author id and return a string with the author label"""
    return ID_AUTHOR[_id]


# Dates
def get_date_author():
    """Returns entirety of date-author index."""
    _path = os.path.join(THIS_DIR, "author_date.json")
    return open_json(_path)


def get_dates():
    """Return a list of all the epithet labels."""
    _dict = get_date_author()
    return sorted(_dict.keys())


def get_date_of_author(_id):
    """Pass author id and return the name of its associated date."""
    _dict = get_date_author()
    for date, ids in _dict.items():
        if _id in ids:
            return date
    return None


def _get_epoch(_str):
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


def _check_number(_str):
    """check if the string contains only a number followed by ?"""
    if regex.match(r"^[0-9]+\?*", _str):
        return True
    return False


def _handle_splits(_str):
    """Check if incoming date has a '-" or '/', if so do stuff."""
    _str = _str.replace("/", "-")
    _tmp_dict = {}

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
    _dict = get_date_author()
    for tlg_date in _dict:
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
