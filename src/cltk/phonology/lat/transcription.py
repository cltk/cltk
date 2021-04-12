"""Convert a word from Latin orthography into its hypothesized 
pronunciation in the International Phonetic Alphabet (IPA).

https://raw.githubusercontent.com/j-duff/cltk/ipa/
cltk/phonology/lat/transcription.py
"""
import re
import unicodedata
from typing import List

from nltk.tokenize import wordpunct_tokenize

from cltk.core.cltk_logger import logger
from cltk.prosody.lat import macronizer as m

try:
    # James Tauber's greek_accentuation package
    from greek_accentuation import characters as chars
except ImportError as import_error:
    message = (
        'Missing "greek_accentuation" package. Install with '
        "`pip install greek-accentuation`."
    )
    logger.error(message)
    logger.error(import_error)
    raise

__author__ = ["Jack Duff <jmunroeduff@gmail.com>"]
__license__ = "MIT License. See LICENSE."

# Dictionaries of phonological reconstructions for use in transcribing.
# Allen, W. Sidney. 1965. Vox Latina.

LATIN = {
    "Classical": {
        "Allen": {
            "correspondence": {
                "p": "p",
                "t": "t̪",
                "c": "k",
                "k": "k",
                "qu": "kʷ",
                "b": "b",
                "d": "d̪",
                "g": "g",
                "gu": "gʷ",
                "ph": "pʰ",
                "th": "t̪ʰ",
                "ch": "kʰ",
                "n": "n̪",
                "m": "m",
                "r": "r",
                "rh": "r",  # Voiceless r was spelled but not pronounced.
                "l": "l",
                "f": "f",
                "s": "s",
                "h": "h",
                "j": "j",
                "v": "w",
                "x": "ks",
                "z": "z",
                "ī": "iː",
                "ū": "uː",
                "i": "ɪ",
                "u": "ʊ",
                "e": "ɛ",
                "o": "ɔ",
                "ē": "eː",
                "ō": "oː",
                "a": "a",
                "ā": "aː",
                "y": "y",
                "ȳ": "y:",
                "ae": "aj",
                "au": "aw",
                "oe": "oj",
                "eu": "ew",
                "ei": "ej",
            },
            "diphthongs": [  # and digraphs
                "qu",
                "gu",
                "ph",
                "th",
                "ch",
                "rh",
                "ae",
                "au",
                "oe",
                "eu",
                "ei",
            ],
            "punctuation": [
                ".",
                ",",
                ";",
                ":",
                "-",
                "–",
                "?",
                "!",
                "(",
                ")",
                "'",
                '"',
                "[",
                "]",
            ],
            "alternations": [
                "j_maker",  # word initial and intervocalic i is assumed j
                "w_maker",  # word initial and intervocalic u is assumed w
                "wj_block",  # prevents accidental sequence wj
                "uj_diph_maker",  # after w and j have been created, recognizes
                # <ui> = [uj]
                "b_devoice",  # b devoices before /t/, /s/
                "g_n_nasality_assimilation",  # only before n
                "n_place_assimilation",  # should also do labial, and
                # labio-dental before f.
                "final_m_drop",  # m drops and lengthens + nasalizes preceding
                # vowel word-finally
                "ns_nf_lengthening",  # vowels lengthen before ns or nf
                "l_darken",  # l darkens to ɫ in coda
                "j_z_doubling",  # intervocalic j and z > jj and zz
                "long_vowel_catcher",  # corrects accidental instances of ɪː
                # and similar.
                "e_i_closer_before_vowel",  # ɛ to ɛ̣, ɪ to ɪ̣ before another vowel
                "intervocalic_j",  # j glide between vowels
            ],
        }
    }
}

# Unhandled exceptions: preposition "ad" becomes [at̪] not [ad̪] before s and t
# subf > suff, subm > summ, subg > sugg, subc > succ, subr > rr
# j exceptions like ad*j*ectivum and con*j*unx

# All IPA characters used sorted by natural classes.
# WILL NEED ADDITIONS AS MORE RECONSTRUCTIONS USED

IPA = {
    "voiced": [  # [+voice]
        "b",
        "d̪",
        "g",
        "gʷ",
        "m",
        "n̪",
        "ŋ",
        "ɱ" "l",
        "ɫ",
        "r",
        "z",
    ],
    "labial": ["b", "p", "pʰ", "m"],  # [+labial, -labiodental]
    "labiodental": ["f", "ɱ"],  # [+labial, +labiodental]
    "coronal": ["d̪", "t̪", "t̪ʰ", "n̪", "s", "z", "r", "l", "ɫ"],  # [+coronal]
    "velar": ["g", "k", "kʰ", "kʷ", "gʷ", "ŋ"],  # [+velar]
    "nasal": ["m", "ɱ", "n", "ŋ"],  # [+consonantal, +nasal]
    "approximant": ["l", "ɫ", "r", "j", "w"],  # [+approximant]
    "continuant": ["h", "f", "s", "z", "l", "ɫ", "r"],  # [+continuant, +consonantal]
    "vowel": [  # [-consonantal -approximant]
        "a",
        "aː",
        "ɛ",
        "ɛ̣",
        "eː",
        "ɪ",
        "ɪ̣",
        "iː",
        "ɔ",
        "oː",
        "ʊ",
        "u",
        "uː",
        "y",
        "yː",
        "ãː",
        "ẽː",
        "ĩː",
        "õː",
        "ũː",
    ],
    "high": [  # [-consonantal, +high]
        "ɪ",
        "ɪ̣",
        "iː",
        "ʊ",
        "u",
        "uː",
        "y",
        "yː",
        "ɪ̃",
        "ɪ̣̃",
        "ĩː",
        "ʊ̃",
        "ũ",
        "ũː",
        "ỹ",
        "ỹː",
    ],
    "mid": [  # [-consonantal, -high, -low]
        "ɛ",
        "ɛ̣",
        "eː",
        "ɔ",
        "oː",
        "ɛ̃",
        "ɛ̣̃",
        "ẽː",
        "ɔ̃",
        "õː",
    ],
    "low": ["a", "aː", "ã", "ãː"],  # [-consonantal, +low]
    "front": [  # [-consonantal, +front]
        "ɪ",
        "ɪ̣",
        "iː",
        "y",
        "yː",
        "ɛ",
        "ɛ̣",
        "eː",
        "ɪ̃",
        "ɪ̣̃",
        "ĩː",
        "ỹ",
        "ỹː",
        "ɛ̃",
        "ɛ̣̃",
        "ẽː",
    ],
    "central": ["a", "aː", "ã", "ãː"],  # [-consonantal, -front, -back]
    "back": [  # [-consonantal, +back]
        "ʊ",
        "u",
        "uː",
        "ɔ",
        "oː",
        "ʊ̃",
        "ũ",
        "ũː",
        "ɔ̃",
        "õː",
    ],
    "boundary": ["#"],
}


class Phone:
    """A phonological unit to be manipulated and represented as an IPA string."""

    # Has a bundle of feature values that help classify it so that it can
    # trigger contextual pronunciation changes.

    def __init__(self, ipa_ch: str):
        """
        Analyzes features of phonetic signs
        :param ipa_ch: phonetic sign from IPA
        """

        # eventually exported to output string
        self.ipa = unicodedata.normalize("NFC", ipa_ch)
        # will be assigned once in Word, as the pre-context of this phone
        self.left = ""
        # .... as the post-context of this phone
        self.right = ""

        # bundle of features, stored as booleans:
        self.vce = self.ipa in IPA["voiced"]
        self.lab = self.ipa in IPA["labial"]
        self.lbd = self.ipa in IPA["labiodental"]
        self.cor = self.ipa in IPA["coronal"]
        self.vel = self.ipa in IPA["velar"]
        self.nas = self.ipa in IPA["nasal"]
        self.app = self.ipa in IPA["approximant"]
        self.cont = self.ipa in IPA["continuant"]
        self.vow = self.ipa in IPA["vowel"]
        self.hi = self.ipa in IPA["high"]
        self.mid = self.ipa in IPA["mid"]
        self.lo = self.ipa in IPA["low"]
        self.fr = self.ipa in IPA["front"]
        self.ctr = self.ipa in IPA["central"]
        self.bk = self.ipa in IPA["back"]
        self.bound = self.ipa in IPA["boundary"]

    def __repr__(self):
        return self.ipa


class Word:
    """Max. phonological unit, contains phones and triggers alternations."""

    # An ordered collection of Phones, which are bundles of
    # features/IPA strings.

    def __init__(self, ipa_str: str, root: dict):
        """

        :param ipa_str:
        :param root:
        """
        self.string = unicodedata.normalize("NFC", ipa_str)
        # Appropriate directory in the reconstruction dictionary
        self.root = root
        # list of contextual pronunciation alternations
        self.alts = self.root["alternations"]
        # Turns string of IPA characters into list of Phones
        self.phones = [Phone(c) for c in re.findall(r".[̪̣̃ʷʰ]*ː?", self.string)]

        self.syllables = []

    def _refresh(self):
        """
        Assigns left and right contexts for every phone
        """
        for n in range(len(self.phones)):
            p = self.phones[n]
            if n != 0:
                p.left = self.phones[n - 1]
            else:
                p.left = Phone("#")
            if n != len(self.phones) - 1:
                p.right = self.phones[n + 1]
            else:
                p.right = Phone("#")

    def _j_maker(self):
        """
        Assume word-initial or intervocalic i to be j
        """
        out_phones = self.phones
        target = Phone("j")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa == "ɪ" and (
                (p.left.bound and p.right.vow) or (p.left.vow and p.right.vow)
            ):
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _w_maker(self):
        """
        Assume word-initial or intervocalic u to be w
        """
        out_phones = self.phones
        target = Phone("w")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if ((p.ipa == "ʊ") or (p.ipa == "u")) and (
                (p.left.bound and (p.right.vow or p.right.ipa == "j"))
                or (p.left.vow and p.right.vow)
            ):
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _wj_block(self):
        """
        Addendum to correct possible 'wj' sequences
        """
        out_phones = self.phones
        target = Phone("ɪ")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.left.ipa == "w" and p.ipa == "j":
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _uj_diph_maker(self):
        """
        Find accidental "ʊɪ" instances and treat as diphthong [uj].
        """
        out_phones = self.phones
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.left.ipa == "ʊ" and p.ipa == "ɪ":
                out_phones[n - 1] = Phone("u")
                out_phones[n] = Phone("j")
        self.phones = out_phones
        self._refresh()

    def _b_devoice(self):
        """
        Pronounce b as p when followed by s or t.
        """
        out_phones = self.phones
        target = Phone("p")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa == "b" and (p.right.ipa == "s" or p.right.ipa == "t̪"):
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _final_m_drop(self):
        """
        Final m nasalizes and lengthens nucleus and drops.
        """
        out_phones = self.phones
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.left.vow and p.ipa == "m" and p.right.bound:
                out_phones[n - 1] = Phone(p.left.ipa + "̃ː")
                del out_phones[n]
        self.phones = out_phones
        self._refresh()

    def _n_place_assimilation(self):
        """
        Pronounce n as ŋ when followed by velar.
        """
        out_phones = self.phones
        target = Phone("ŋ")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa == "n̪" and p.right.vel:
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _g_n_nasality_assimilation(self):
        """
        Pronounce g as ŋ when followed by n.
        """

        out_phones = self.phones
        target = Phone("ŋ")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa == "g" and p.right.ipa == "n̪":
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _ns_nf_lengthening(self):
        """
        Lengthen vowel before ns or nf.
        """
        out_phones = self.phones
        for n in range(len(self.phones)):
            p = self.phones[n]
            if (
                p.left.vow
                and "ː" not in p.left.ipa
                and p.ipa == "n̪"
                and (p.right.ipa == "s" or p.right.ipa == "f")
            ):
                out_phones[n - 1] = Phone(p.left.ipa + "ː")
        self.phones = out_phones
        self._refresh()

    def _l_darken(self):
        """
        Pronounce l as ɫ in coda.
        """
        out_phones = self.phones
        target = Phone("ɫ")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa == "l" and ((not p.right.vow) or p.right.bound):
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _j_z_doubling(self):
        """
        Double j and z between vowels.
        """
        out_phones = self.phones
        dupl = []
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.right.vow and (p.ipa == "j" or p.ipa == "z") and p.left.vow:
                dupl.append((True, n - len(self.phones), p.ipa))
            else:
                dupl.append((False, n - len(self.phones), None))
        for t in sorted(dupl, key=lambda tup: tup[1]):
            if t[0]:
                out_phones.insert(t[1], Phone(t[2]))
        self.phones = out_phones
        self._refresh()

    def _long_vowel_catcher(self):
        """
        Replace ɪː with iː, ʊː with uː, and ɛː with eː.
        """
        out_phones = self.phones
        target_dict = {
            "ɪː": "iː",
            "ʊː": "uː",
            "ɛː": "eː",
            "ɪ̃ː": "ĩː",
            "ʊ̃ː": "ũː",
            "ɛ̃ː": "ẽː",
        }
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa in target_dict.keys():
                out_phones[n] = Phone(target_dict[p.ipa])
        self.phones = out_phones
        self._refresh()

    def _e_i_closer_before_vowel(self):
        """
        e and i become closer (̣) when followed by a vowel.
        """
        out_phones = self.phones
        for n in range(len(self.phones)):
            p = self.phones[n]
            if (p.ipa == "ɛ" or p.ipa == "ɪ") and p.right.vow:
                out_phones[n] = Phone(p.ipa + "̣")
        self.phones = out_phones
        self._refresh()

    def _intervocalic_j(self):
        """
        epenthesize j between vowels
        """
        out_phones = self.phones
        target = Phone("j")
        j = []
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.left.vow and p.vow:
                j.append((True, n - len(self.phones)))
            else:
                j.append((False, n - len(self.phones)))
        for t in sorted(j, key=lambda tup: tup[1]):
            if t[0]:
                out_phones.insert(t[1], target)
        self.phones = out_phones
        self._refresh()

    # list of all possible alternations
    ALTERNATIONS = [
        ("j_maker", _j_maker),
        ("w_maker", _w_maker),
        ("wj_block", _wj_block),
        ("uj_diph_maker", _uj_diph_maker),
        ("b_devoice", _b_devoice),
        ("final_m_drop", _final_m_drop),
        ("n_place_assimilation", _n_place_assimilation),
        ("g_n_nasality_assimilation", _g_n_nasality_assimilation),
        ("ns_nf_lengthening", _ns_nf_lengthening),
        ("l_darken", _l_darken),
        ("j_z_doubling", _j_z_doubling),
        ("long_vowel_catcher", _long_vowel_catcher),
        ("e_i_closer_before_vowel", _e_i_closer_before_vowel),
        ("intervocalic_j", _intervocalic_j),
    ]

    def _alternate(self):
        """
        After setting left and right contexts for every phone...
        """
        self._refresh()
        # runs all alternations
        for a in Word.ALTERNATIONS:
            if a[0] in self.alts:
                a[1](self)

    def syllabify(self) -> List[List[Phone]]:
        """
        Takes Word input and returns a list of syllables
        as (onset, nucleus, coda) tuples
        where onset, nucleus, and coda are all lists of Phones.
        :return: list of syllables
        """
        nuclei = []
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.vow:
                nuclei.append(n)
        # initialize syllables with a tuple for the first syllable
        # where onset is everything before the first nucleus
        # and coda remains unknown.
        syllables = [[self.phones[0 : nuclei[0]], [self.phones[nuclei[0]]], []]]
        # continue for every nucleus, assuming that everything between
        # the previous nucleus and it is the onset.
        for x in range(len(nuclei) - 1):
            i = nuclei[x + 1]
            onset = self.phones[nuclei[x] + 1 : i]
            nucleus = [self.phones[i]]
            syllables.append([onset, nucleus, []])
        # assume that everything after the final nucleus is final coda.
        syllables[-1][2] = self.phones[nuclei[-1] + 1 :]
        # now go through and check onset viability
        for x in range(len(syllables) - 1):
            onset = syllables[x + 1][0]
            nucleus = syllables[x + 1][1]
            coda = syllables[x + 1][2]
            # trim all onsets greater than the maximum 2 phones
            # removing extra phones from the left
            # and appending them to the previous coda
            if len(onset) > 2:
                trim = onset[:-2]
                del onset[:-2]
                syllables[x][2] = trim
            # once onset is 2 phones...
            if len(onset) == 2:
                # stop + liquid is the only viable sequence and passes
                if (
                    (not onset[0].cont)
                    and (not onset[0].app)
                    and (onset[1].nas or onset[1].app)
                ):
                    break
                # otherwise, onset must be right Phone only
                # the left phone is appended to the previous coda
                else:
                    trim = onset[0]
                    del onset[0]
                    syllables[x][2] += [trim]
        self.syllables = syllables
        return syllables

    def _print_ipa(self, syllabify, accentuate):
        """
        Depending on the syllabify and accentuate parameters
        Prints an appropriately marked up version of the transcription

        :param syllabify:
        :param accentuate:
        :return:
        """

        out = ""
        if syllabify:
            syllables = self.syllabify()
            # the ultima is the final syllable
            ultima = syllables[-1]
            # identify which syllable has stress and store index as accent
            if accentuate:
                # one syllable words have ultimate stress
                if len(syllables) == 1:
                    accent = -1
                # two syllable words have penultimate stress
                elif len(syllables) == 2:
                    accent = -2
                else:
                    # penult is second to last syllable
                    penult = syllables[-2]
                    # if penult is diphthong (long), penultimate stress
                    if len(penult[1]) > 1:
                        accent = -2
                    # if penult is long vowel, penultimate stress
                    elif "ː" in penult[1][0].ipa:
                        accent = -2
                    # if penult has coda (closed/long by position),
                    # penultimate stress
                    elif len(penult[2]) > 0:
                        accent = -2
                    # otherwise (penult is short) antepenultimate stress
                    else:
                        accent = -3
                # loop over syllables by index
                for x in range(len(syllables)):
                    s = syllables[x]
                    # if index matches accent index set above
                    if x - len(syllables) == accent:
                        # precede that syllable with
                        # IPA stress punctuation: '
                        out += "'"
                    # then, print IPA by syllable segment as usual
                    for n in s:
                        for p in n:
                            out += p.ipa
                    # seperate all syllables with IPA syllable punctuation: .
                    if s != ultima:
                        out += "."
            # if no accentuation flag, proceed with syllabified printing
            else:
                for s in syllables:
                    for n in s:
                        for p in n:
                            out += p.ipa
                    # seperate all syllables with IPA syllable punctuation: .
                    if s != ultima:
                        out += "."
        # if no syllabification flag, proceed with
        # unsyllabified IPA printing
        else:
            for p in self.phones:
                out += p.ipa
        return out


class Transcriber:
    """Uses a reconstruction to transcribe a orthographic string into IPA."""

    def __init__(self, dialect: str, reconstruction: str):
        """

        :param dialect: Latin dialect
        :param reconstruction: reconstruction method
        """
        self.lect = dialect
        self.recon = reconstruction
        self.root = LATIN[self.lect][self.recon]
        self.table = self.root["correspondence"]
        self.diphs = self.root["diphthongs"]
        self.punc = self.root["punctuation"]
        self.macronizer = m.Macronizer("tag_ngram_123_backoff")

    def _parse_diacritics(self, ch: str) -> str:
        """

        EG: input with base a -> a/LENGTH/DIAERESIS/

        :param ch: character
        :return: a string with separated and organized diacritics for easier access later.
        """

        out = chars.base(ch).lower()  # Initialize out as base of character.

        length = chars.length(ch)
        dia = chars.diaeresis(ch)

        out += "/"  # Create 1st boundary

        # If any length, place between 1st and 2nd boundary
        if length:
            out += length

        out += "/"  # Create 2nd boundary

        if dia:  # If any diaeresis,
            out += dia  # place between second and final boundary

        out += "/"  # Create final boundary

        return out

    def _prep_text(self, text: str):
        """
        Performs preparatory tasks grouping and reordering characters
        in order to make transcription formulaic.

        :param text:
        :return:
        """
        string_in = "".join([self._parse_diacritics(ch) for ch in text])

        # searches for diphthongs and treats them as one phone
        for d in self.diphs:
            d1 = d[0]
            d2 = d[1]
            pattern = r"(" + d1 + r")\/\/\/(" + d2 + r")(\/\/\/)"
            string_in = re.sub(pattern, r"\1\2\3", string_in)

        tup_out = re.findall(r"(..?)\/([̄̆]*)\/(¨?)\/", string_in)

        return tup_out

    def transcribe(
        self,
        text,
        macronize=True,
        syllabify=True,
        accentuate=True,
        with_squared_brackets=True,
    ):
        """
        >>> allen_transcriber = Transcriber("Classical", "Allen")
        >>> example = allen_transcriber.transcribe("Quo usque tandem, O Catilina, " + "abutere nostra patientia?")
        >>> example
        "['kʷoː 'ʊs.kʷɛ 't̪an̪.d̪ẽː 'oː ka.t̪ɪ.'liː.n̪aː a.buː.'t̪eː.rɛ 'n̪ɔs.t̪raː pa.t̪ɪ̣.'jɛn̪.t̪ɪ̣.ja]"

        :param text: text to transcribe
        :param macronize: if True, macronize result
        :param syllabify: if True, syllabify result
        :param accentuate: if True, accentuate result
        :param with_squared_brackets: if True, put squared brackets around transcription
        :return: transcribed text
        """
        # if macronize, will first use the tagger to macronize input
        # otherwise, input will be the raw input string
        if macronize:
            text = self.macronizer.macronize_text(text)
        # input is word-tokenized, stripped of non-diacritic punctuation,
        # and diphthongs and diacritics are handled
        inp = [
            self._prep_text(w) for w in wordpunct_tokenize(text) if w not in self.punc
        ]
        words = []
        for w in inp:
            out = ""
            for c in w:
                if "̄" in c[1]:
                    macron_added = c[0] + "̄"
                    ipa = self.table.get(macron_added, macron_added)
                else:
                    ipa = self.table.get(c[0], c[0])
                out += ipa
            transcription = Word(out, self.root)
            transcription._alternate()
            words.append(transcription)
        # Encloses output in brackets, proper notation for surface form.
        result = " ".join([w._print_ipa(syllabify, accentuate) for w in words])
        if with_squared_brackets:
            result = "[" + result + "]"
        return result
