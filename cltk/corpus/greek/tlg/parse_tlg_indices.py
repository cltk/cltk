"""Load .json files and allow easy searching, then pulling author ids.
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>',
              'Martín Pozzi <marpozzi@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

import inspect
import json
import os
import re
import sys

# http://stackoverflow.com/a/50905
THIS_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def open_json(file_name):
    """Opens json file, returns contents."""
    json_path = os.path.join(THIS_DIR, file_name)
    with open(json_path) as file_open:
        return json.load(file_open)


# Gender
def get_female_authors():
    """Open female authors index and return ordered set of author ids."""
    _path = os.path.join(THIS_DIR, 'author_female.json')
    _dict = open_json(_path)
    return set(_dict['Femina'])


# Epithet
def get_epithet_index():
    """Return dict of epithets (key) to a set of all author ids of that
    epithet (value).
    """
    _path = os.path.join(THIS_DIR, 'author_epithet.json')
    _dict = open_json(_path)

    for k, v in _dict.items():
        _dict[k] = set(v)
    return _dict


def get_epithets():
    """Return a list of all the epithet labels."""
    _path = os.path.join(THIS_DIR, 'author_epithet.json')
    _dict = open_json(_path)
    return sorted(_dict.keys())


def select_authors_by_epithet(query):
    """Pass exact name (case insensitive) of epithet name, return ordered set
    of author ids.
    """

    _path = os.path.join(THIS_DIR, 'author_epithet.json')
    _dict = open_json(_path)

    for epithet, ids in _dict.items():
        if epithet.casefold() == query.casefold():
            return set(ids)


def get_epithet_of_author(_id):
    """Pass author id and return the name of its associated epithet."""
    _path = os.path.join(THIS_DIR, 'author_epithet.json')

    _id = str(_id)

    _dict = open_json(_path)

    for epithet, ids in _dict.items():
        if _id in ids:
            return epithet


# Geography
def get_geo_index():
    """Get entire index of geographic name (key) and set of associated authors
    (value).
    """
    _path = os.path.join(THIS_DIR, 'author_geo.json')
    _dict = open_json(_path)

    for k, v in _dict.items():
        _dict[k] = set(v)

    return _dict


def get_geographies():
    """Return a list of all the epithet labels."""
    _path = os.path.join(THIS_DIR, 'author_geo.json')
    _dict = open_json(_path)
    return sorted(_dict.keys())


def select_authors_by_geo(query):
    """Pass exact name (case insensitive) of geography name, return ordered set
    of author ids.
    """

    _path = os.path.join(THIS_DIR, 'author_geo.json')
    _dict = open_json(_path)

    for geo, ids in _dict.items():
        if geo.casefold() == query.casefold():
            return set(ids)


def get_geo_of_author(_id):
    """Pass author id and return the name of its associated epithet."""
    _path = os.path.join(THIS_DIR, 'author_geo.json')

    _id = str(_id)

    _dict = open_json(_path)

    for geo, ids in _dict.items():
        if _id in ids:
            return geo


# List of TLG indices
def get_lists():
    """A list of the TLG's lists."""
    _path = os.path.join(THIS_DIR, 'index_lists.json')
    _dict = open_json(_path)
    return _dict


# Master author index (`id_author.json`)
def get_id_author():
    """Returns entirety of id-author TLG index."""
    _path = os.path.join(THIS_DIR, 'id_author.json')
    _dict = open_json(_path)
    return _dict


def select_id_by_name(query):
    """Do a case-insensitive regex match on author name, returns TLG id."""
    id_author = get_id_author()
    comp = re.compile(r'{}'.format(query.casefold()))
    matches = []
    for _id, author in id_author.items():
        match = comp.findall(author.casefold())
        if match:
            matches.append((_id, author))
    return matches


# Dates
def get_date_author():
    """Returns entirety of date-author index."""
    _path = os.path.join(THIS_DIR, 'author_date.json')
    return open_json(_path)


def get_dates():
    """Return a list of all the epithet labels."""
    _path = os.path.join(THIS_DIR, 'author_date.json')
    _dict = open_json(_path)
    return sorted(_dict.keys())


def get_date_of_author(_id):
    """Pass author id and return the name of its associated date."""
    _path = os.path.join(THIS_DIR, 'author_date.json')

    _id = str(_id)

    _dict = open_json(_path)

    for date, ids in _dict.items():
        if _id in ids:
            return date


if __name__ == "__main__":
    print(get_date_of_author('0001'))