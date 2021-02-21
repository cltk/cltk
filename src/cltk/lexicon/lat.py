

from functools import lru_cache
import os
import re
import yaml
from cltk.utils import CLTK_DATA_DIR


class LatinLewisLexicon:
    def __init__(self):
        rel_path = os.path.join(CLTK_DATA_DIR, "lat", "lexicon", "cltk_lat_lewis_elementary_lexicon")
        with open(os.path.join(rel_path, "lewis.yaml"), "r", encoding="utf-8") as f:
            entries = yaml.load(f, Loader=yaml.Loader)
        self.entries = entries

    @lru_cache(maxsize=None)
    def lookup(self, lemma):
        """
        >>> lll = LatinLewisLexicon()
        >>> lll.lookup("clemens")[:50]
        'clēmēns entis (abl. -tī; rarely -te, L.), adj. with comp. and sup, mild, calm, gentle: clementissimus amnis, O.—Fig., calm, quiet, gentle, tranquil, kind: vita, T.: cupio me esse clementem: satis in disputando.—Mild, forbearing, indulgent, compassionate, merciful: animo clementi in illam, T : iudices: viro clemens misero peperci, H.: vir ab innocentiā clementissimus: legis interpres, L.: castigatio: clementior sententia, L.—Mitigated, qualified: rumor, S.'

        :param lemma:
        :return:
        """
        if not self.entries:
            raise
        keys = self.entries.keys()
        matches = [key for key in keys if re.match(rf"{lemma}[0-9]?", key)]
        n_matches = len(matches)
        if n_matches > 1:
            return "\n".join([self.entries[key] for key in matches])
        elif n_matches == 1:
            return self.entries[lemma]
        else:
            return ""
