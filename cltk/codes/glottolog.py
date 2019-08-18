"""Module for mapping Glottolog codes to standard family names.

Glottolog is a project run by the Max Planck Institute for the
Science of Human History. The website contains codes for languages
as well as reconstructions of language families: http://glottolog.org/.

TODO: Consider whether this kind of module is necessary.

TODO: Consider the other codes that users might want (ISO 639-1 639-2, ISO 639-3)
"""

from typing import Dict
from typing import List
from typing import Union

LANGUOID_NAME: Dict[str, Union[str, List[str]]] = dict(
    anci1242="Ancient Greek",
    lati1261="Latin",
    oldn1244="Old Norse",
    olde1238="Old English",
    unlabeled=["Ottoman"],
)
