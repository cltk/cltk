"""Init for ``cltkv1.languages``."""

from typing import List

from cltkv1.utils.data_types import Language
from cltkv1.utils.exceptions import UnknownLanguageError

from .glottolog import LANGUAGES


def get_lang(iso_code: str) -> Language:
    """Take in search term of usual language name and find ISO code.


    >>> from cltkv1.languages import get_lang
    >>> get_lang("akk")
    Language(name='Akkadian', glottolog_id='akka1240', latitude=33.1, longitude=44.1, dates=[], family_id='afro1255', parent_id='east2678', level='language', iso_639_3_code='akk', type='a')
    >>> from cltkv1.utils.exceptions import UnknownLanguageError
    >>> get_lang("xxx")
    Traceback (most recent call last):
      ...
    cltkv1.utils.exceptions.UnknownLanguageError
    """
    try:
        return LANGUAGES[iso_code]
    except KeyError:
        raise UnknownLanguageError


def find_iso_name(common_name: str) -> List[str]:
    """Find the ISO 639-3 language code (e.g., ``lat``) by
    inputting the common name (``Latin``). This function just
    does simple substring matching, with some normalization
    of case, on the ``name`` field of the ``Language`` object.


    >>> from cltkv1.languages import find_iso_name
    >>> find_iso_name(common_name="Latin")
    ['lat']
    >>> find_iso_name(common_name="latin")
    ['lat']
    >>> find_iso_name(common_name="slav")
    ['chu']
    >>> find_iso_name(common_name="xxx")
    []
    """
    iso_return_list = list()  # type: List[str]
    for iso_key, language_obj in LANGUAGES.items():
        if common_name.lower() in language_obj.name.lower():
            iso_return_list.append(iso_key)
    return iso_return_list
