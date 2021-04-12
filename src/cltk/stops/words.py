"""Stopwords for languages.

TODO: Give definition here of stopwords.
"""

from typing import List

from cltk.languages.utils import get_lang
from cltk.stops import (
    akk,
    ang,
    arb,
    cop,
    enm,
    fro,
    gmh,
    grc,
    hin,
    lat,
    non,
    omr,
    pan,
    san,
)

MAP_ISO_TO_MODULE = dict(
    akk=akk,
    ang=ang,
    arb=arb,
    cop=cop,
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


class Stops:
    """Class for filtering stopwords.

    >>> from cltk.stops.words import Stops
    >>> from cltk.languages.example_texts import get_example_text
    >>> from boltons.strutils import split_punct_ws
    >>> stops_obj = Stops(iso_code="lat")
    >>> tokens = split_punct_ws(get_example_text("lat"))
    >>> len(tokens)
    178
    >>> tokens[25:30]
    ['legibus', 'inter', 'se', 'differunt', 'Gallos']
    >>> tokens_filtered = stops_obj.remove_stopwords(tokens=tokens)
    >>> len(tokens_filtered)
    142
    >>> tokens_filtered[22:26]
    ['legibus', 'se', 'differunt', 'Gallos']
    """

    def __init__(self, iso_code: str):
        self.iso_code = iso_code
        get_lang(iso_code=self.iso_code)
        self.stops = self.get_stopwords()

    def get_stopwords(self) -> List[str]:
        """Take language code, return list of stopwords."""
        stops_module = MAP_ISO_TO_MODULE[self.iso_code]
        return stops_module.STOPS

    def remove_stopwords(
        self, tokens: List[str], extra_stops: List[str] = None
    ) -> List[str]:
        """Take list of strings and remove stopwords."""
        if extra_stops and not isinstance(extra_stops, list):
            raise ValueError("``extra_stops`` must be a list.")
        if extra_stops and not isinstance(extra_stops[0], str):
            raise ValueError("List ``extra_stops`` must contain str type only.")
        return [token for token in tokens if token not in self.stops]
