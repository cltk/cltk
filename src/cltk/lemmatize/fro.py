"""
Lemmatizer for Old French.
Rules are based on Brunot & Bruneau (1949).
"""

import importlib.machinery
import os

from cltk.lemmatize.naive_lemmatizer import DictionaryRegexLemmatizer
from cltk.utils import CLTK_DATA_DIR

__author__ = ["Natasha Voake <natashavoake@gmail.com>"]
__license__ = "MIT License. See LICENSE."

estre_replace = [
    (
        "^sereient$|^fussions$|^fussiens$|^sereies$|^sereiet$|^serïens$|^seriiez$|^fussiez$|^fussent$|^ierent$|^fustes$|^furent$|^ierent$|^sereie$|^seroie$|^sereit$|^seiens$|^seient$|^fusses$|^fussez$|^estant$|^seiens$|^somes$|^estes$|^ieres$|^ieres$|^eiens$|^eriez$|^erent$|^fumes$|^irmes$|^ertes$|^seies$|^seiet$|^seiez$|^fusse$|^seies$|^seiez$|^suis$|^sont$|^iere$|^eres$|^eret$|^iers$|^iert$|^seie$|^seit$|^fust$|^esté$|^ies$|^est$|^ere$|^ert$|^fui$|^fus$|^ier$|^ert$|^es$|^fu$",
        "estre",
    )
]

avoir_replace = [
    (
        "^avreient$|^avroient$|^eüssions$|^eüssiens$|^avrarai$|^avreies$|"
        "^avroies$|^avreiet$|^avroiet$|^avrïens$|^avrïons$|^avriiez$|"
        "^eüssiez$|^eüssent$|^eüstes$|^óurent$|^avrons$|^avront$|^avreie$|"
        "^avrïez$|^eüsses$|^eüssez$|^avons$|^eümes$|^orent$|^avrai$|"
        "^avras$|^avrez$|^aiens$|^ayons$|^aient$|^eüsse$|^avez$|^avra$|"
        "^arai$|^aies$|^aiet$|^aiez$|^ayez$|^eüst$|^ont$|^eüs$|"
        "^oüs$|^óut$|^oiz$|^aie$|^ait$|^ai$|^as$|^at$|^oi$|"
        "^ot$|^oü$|^eü$|^a$",
        "avoir",
    )
]

auxiliary_rules = estre_replace + avoir_replace

first_conj_rules = [
    (
        "es$|e$|ons$|ez$|ent$|z$|(e)ai$|(e)as$|(e)a$|(e)at$|(e)ames$|(e)astes$|(e)erent$|(e)asse$|é$",
        "er",
    )
]

i_type_rules = [("i$|is$|it$|imes$|istes$|irent$|isse$", "ir")]

u_type_rules = [("ui$|us$|ut$|umes$|ustes$|urent$|usse$", "oir")]

verbal_rules = u_type_rules + i_type_rules + first_conj_rules

regime_rules = [("on$|ain$", "e")]

plural_rules = [("ales$|aux$|aus$", "al"), ("s$", "")]

masc_to_fem_rules = [("se$", "x"), ("ive$", "if"), ("ee$", "e")]

french_nominal_rules = regime_rules + plural_rules + masc_to_fem_rules

misc_rules = [("x$", "l"), ("z$", "t"), ("un$", "on"), ("eus$", "os"), ("^e$", "et")]

determiner_rules = [
    ("^li$|^lo$|^le$|^la$|^les$", "le"),
    ("^del$|^du$", "de le"),
    ("^al$|^au$", "a le"),
    ("^as$|^aus$|^aux$", "a les"),
    ("^uns$|^une$|^unes$", "un"),
]

reduction_rules = [
    ("d'", "de"),
    ("m'", "me"),
    ("t'", "te"),
    ("l'", "le"),
    ("qu'", "que"),
]

patterns = (
    determiner_rules
    + misc_rules
    + auxiliary_rules
    + verbal_rules
    + french_nominal_rules
    + reduction_rules
)


class OldFrenchDictionaryLemmatizer(DictionaryRegexLemmatizer):
    """
    Naive lemmatizer for Old French.

    >>> lemmatizer = OldFrenchDictionaryLemmatizer()
    >>> lemmatizer.lemmatize_token('corant')
    'corant'
    >>> lemmatizer.lemmatize_token('corant', return_frequencies=True)
    ('corant', -9.319508628976836)
    >>> lemmatizer.lemmatize_token('corant', return_frequencies=True, best_guess=False)
    [('corir', 0), ('corant', -9.319508628976836)]
    >>> lemmatizer.lemmatize(['corant', '.', 'vult', 'premir'], return_frequencies=True, best_guess=False)
    [[('corir', 0), ('corant', -9.319508628976836)], [('PUNK', 0)], [('vout', -7.527749159748781)], [('premir', 0)]]
    """

    def _load_forms_and_lemmas(self):
        """Load the dictionary of lemmas and forms from the fro data repository."""

        rel_path = os.path.join(
            CLTK_DATA_DIR, "fro", "text", "fro_models_cltk", "inverted_lemma_dict.py"
        )
        path = os.path.expanduser(rel_path)
        loader = importlib.machinery.SourceFileLoader("file", path)
        module = loader.load_module()
        return module.inverted_index

    def _load_unigram_counts(self):
        """Load the table of frequency counts of word forms."""

        rel_path = os.path.join(
            CLTK_DATA_DIR, "fro", "text", "fro_models_cltk", "fro_unigrams.txt"
        )
        path = os.path.expanduser(rel_path)

        type_counts = {}

        with open(path, "r") as infile:
            lines = infile.read().splitlines()
            for line in lines:
                count, word = line.split()
                type_counts[word] = int(count)

        return type_counts

    def _specify_regex_rules(self):
        return determiner_rules
        +misc_rules
        +auxiliary_rules
        +verbal_rules
        +french_nominal_rules
        +reduction_rules
