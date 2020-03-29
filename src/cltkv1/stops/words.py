"""Stopwords for languages.

TODO: Give definition here of stopwords.
"""

from typing import List

from cltkv1.languages.utils import get_lang
from cltkv1.stops import akk, ang, arb, enm, fro, gmh, grc, hin, lat, non, omr, pan, san

MAP_ISO_TO_MODULE = dict(
    akk=akk,
    ang=ang,
    arb=arb,
    enm=enm,
    fro=fro,
    gmh=gmh,
    grc=grc,
    hin=hin,
    lat=lat,
    non=non,
    omr=omr,
    pan=pan,
    san=san,
)


def get_stopwords(iso_code: str) -> List[str]:
    """Take language code, return list of stopwords."""
    get_lang(iso_code=iso_code)
    stops_module = MAP_ISO_TO_MODULE[iso_code]
    return stops_module.STOPS


def remove_stopwords(
    iso_code: str, tokens: List[str], extra_stops: List[str] = None
) -> List[str]:
    """Take list of strings and remove stopwords."""
    if extra_stops and not isinstance(extra_stops, list):
        raise ValueError("``extra_stops`` must be a list.")
    if extra_stops and not isinstance(extra_stops[0], str):
        raise ValueError("List ``extra_stops`` must contain str type only.")
    stopwords = get_stopwords(iso_code=iso_code)
    return [token for token in tokens if token not in stopwords]
