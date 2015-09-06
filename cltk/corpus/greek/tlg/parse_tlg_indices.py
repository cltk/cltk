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


def get_female_authors():
    """Open female authors index and return list of author ids."""
    female_path = os.path.join(THIS_DIR, 'author_female.json')
    with open(female_path) as file_open:
        female_dict = json.load(file_open)
        return female_dict['Femina']


def get_author_geo():
    """"""
    _path = os.path.join(THIS_DIR, 'author_geo.json')
    with open(_path) as file_open:
        _dict = json.load(file_open)
    return _dict


def get_date_author():
    """"""
    _path = os.path.join(THIS_DIR, 'author_date.json')
    with open(_path) as file_open:
        _dict = json.load(file_open)
    return _dict


def get_epithets():
    _path = os.path.join(THIS_DIR, 'author_epithet.json')
    with open(_path) as file_open:
        _dict = json.load(file_open)
    return sorted(_dict.keys())


def get_author_epithet():
    """"""
    _path = os.path.join(THIS_DIR, 'author_epithet.json')
    with open(_path) as file_open:
        _dict = json.load(file_open)
    return _dict


def get_lists():
    """"""
    _path = os.path.join(THIS_DIR, 'index_lists.json')
    with open(_path) as file_open:
        _dict = json.load(file_open)
    return _dict


def get_id_author():
    """"""
    _path = os.path.join(THIS_DIR, 'id_author.json')
    with open(_path) as file_open:
        _dict = json.load(file_open)
    return _dict


def select_author_by_name(query):
    id_author = get_id_author()
    comp = re.compile(r'{}'.format(query.casefold()))
    matches = []
    for _id, author in id_author.items():
        match = comp.findall(author.casefold())
        if match:
            matches.append((_id, author))
    return matches


def select_authors_by_epithet(query):
    """Pass exact name (case insensitive) of epithet name, return list of author ids."""

    _path = os.path.join(THIS_DIR, 'author_epithet.json')
    with open(_path) as file_open:
        _dict = json.load(file_open)

    for epithet,ids in _dict.items():
        if epithet.casefold() == query.casefold():
            return sorted(ids)


def get_epithet_of_author(_id):
    """Takes author id, returns TLG's epithet"""
    _path = os.path.join(THIS_DIR, 'author_epithet.json')

    _id = str(_id)  # the loaded json expects a str

    with open(_path) as file_open:
        _dict = json.load(file_open)

    for epithet, ids in _dict.items():
        if _id in ids:
            return epithet

if __name__ == "__main__":
    print(get_epithet_of_author('0016'))