from typing import List

from cltk.core.data_types import Language
from cltk.core.exceptions import UnknownLanguageError
from cltk.languages.glottolog import LANGUAGES


def get_lang(iso_code: str) -> Language:
    """Take ISO 639-3 code and return ``Language`` object for language.

    TODO: Split this into another fn, ``check_language()``, which is how is usually used now.

    >>> from cltk.languages.utils import get_lang
    >>> get_lang("akk")
    Language(name='Akkadian', glottolog_id='akka1240', latitude=33.1, longitude=44.1, dates=[], family_id='afro1255', parent_id='east2678', level='language', iso_639_3_code='akk', type='a')
    >>> from cltk.core.exceptions import UnknownLanguageError
    >>> get_lang("xxx")
    Traceback (most recent call last):
      ...
    cltk.core.exceptions.UnknownLanguageError: Unknown ISO language code 'xxx'.
    """
    try:
        return LANGUAGES[iso_code]
    except KeyError:
        raise UnknownLanguageError(f"Unknown ISO language code '{iso_code}'.")


def find_iso_name(common_name: str) -> List[str]:
    """Find the ISO 639-3 language code (e.g., ``lat``) by
    inputting the common name (``Latin``). This function just
    does simple substring matching, with some normalization
    of case, on the ``name`` field of the ``Language`` object.

    >>> find_iso_name(common_name="Latin")
    ['lat']
    >>> find_iso_name(common_name="lat")
    ['xga', 'lat']
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
