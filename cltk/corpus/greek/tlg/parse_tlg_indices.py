"""For loading TLG .json files and searching, then pulling author ids.
"""

from cltk.corpus.greek.tlg.author_date import AUTHOR_DATE
from cltk.corpus.greek.tlg.author_epithet import AUTHOR_EPITHET
from cltk.corpus.greek.tlg.author_female import AUTHOR_FEMALE
from cltk.corpus.greek.tlg.author_geo import AUTHOR_GEO
from cltk.corpus.greek.tlg.id_author import ID_AUTHOR
from cltk.corpus.greek.tlg.index_lists import INDEX_LIST
import regex
import os
import json

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>',
              'Martín Pozzi <marpozzi@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# Gender
def get_female_authors():
    """Open female authors index and return ordered set of author ids."""
    return set(AUTHOR_FEMALE['Femina'])


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
    comp = regex.compile(r'{}'.format(query.casefold()), flags=regex.VERSION1)
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


# Dates
def get_date_author():
    """Returns entirety of date-author index."""
    _path = os.path.join(THIS_DIR, 'author_date.json')
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


def _get_epoch(_str):
    """Take incoming string, return its epoch."""
    if _str.startswith('B.C. '):
        return 'bc'
    elif _str.startswith('A.D. '):
        return 'ad'
    #Here we can not use .startswith('a. B.C. ') because there is a number between a. and B.C.
    #So regex is used for this purpose.
    elif regex.match(r'^a\. *[0-9]+ B\.C\. *', _str):
        return 'bc'
    elif regex.match(r'^p\. *[0-9]+ B\.C\. *', _str):
        return None  #?
    elif _str.startswith('a. A.D. '):
        return None  #?
    elif _str.startswith('p. A.D. '):
        return 'ad'
    elif _str == 'Incertum' or _str == 'Varia':
        return _str
    else:
        return None


'''
def _handle_splits(_str):
    """Check if incoming date has a '-" or '/', if so do stuff."""

    _tmp_dict = {}

    if '-' in _str:
        start, stop = _str.split('-')
    elif '/' in _str:
        start, stop = _str.split('/')
    else:
        _tmp_dict['start_epoch'] = _get_epoch(_str)
    _tmp_dict['start_raw'] = start
    _tmp_dict['stop_raw'] = stop

    start_epoch = _get_epoch(start)
    stop_epoch = _get_epoch(stop)

    if start_epoch:
        _tmp_dict['start_epoch'] = start_epoch
    else:
        _tmp_dict['start_epoch'] = stop_epoch

    if stop_epoch:
        _tmp_dict['stop_epoch'] = stop_epoch
    else:
        _tmp_dict['stop_epoch'] = start_epoch

    return _tmp_dict


def normalize_dates():
    """Experiment to make sense of TLG dates.
    TODO: start here, parse everything with pass
    """
    _dict = open_json('author_date.json')

    for tlg_date in _dict:

        date = {}

        if '-' in tlg_date:
            tmp_date = _handle_splits(tlg_date)
            date.update(tmp_date)
        elif '/' in _dict:
            tmp_date = _handle_splits(tlg_date)
            date.update(tmp_date)
        else:
            known_epoch = _get_epoch(tlg_date)
            if known_epoch:
                date['epoch'] = known_epoch

            if tlg_date is 'Varia' or 'Incertum':
                # give a homer-to-byz date for 'varia'
                # for incertum?
                pass  #?

        print(date)
'''


if __name__ == "__main__":
    pass
