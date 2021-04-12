"""Verse structures of Old Norse poetry"""


import re
from math import floor
from typing import Dict, List, Tuple, Union

import cltk.phonology.non.syllabifier as old_norse_syllabifier
import cltk.phonology.non.transcription as old_norse_transcription
from cltk.core.cltk_logger import logger
from cltk.phonology.non.utils import Transcriber
from cltk.phonology.syllabify import Syllabifier
from cltk.stops.non import STOPS
from cltk.tag.pos import POSTag
from cltk.tokenizers.non import OldNorseWordTokenizer

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


# extension of stop words for poetry
stops_for_poetry = ["ek", "it"]  # to be completed
STOPS.extend(stops_for_poetry)


def old_norse_normalize(text: str) -> str:
    """
    >>> old_norse_normalize("Hvat er  þat?")
    'hvat er þat'

    :param text: text to normalize
    :return: normalized text
    """
    res = text.lower()
    res = re.sub(r"[\-:?;.,]", "", res)
    res = re.sub(r" +", " ", res)
    return res


class ShortLine:
    """
    A short line, or half line, is a
    """

    def __init__(self, text):
        self.text = text
        self.tokenizer = OldNorseWordTokenizer()
        self.syllabified = []
        self.transcribed = []
        self.alliterations = {}
        self.phonological_features_text = []
        self.n_alliterations = 0

        # self.syllabified_transcribed_text = []
        self.syllabified_phonological_features_text = []

    @property
    def tokenized_text(self):
        return self.tokenizer.tokenize(self.text)

    def syllabify(self, syllabifier):
        """
        >>> raw_short_line = "Deyr fé"
        >>> short_line = ShortLine(raw_short_line)
        >>> syl = Syllabifier(language="non", break_geminants=True)
        >>> syl.set_invalid_onsets(old_norse_syllabifier.invalid_onsets)
        >>> short_line.syllabify(syl)

        :param syllabifier: function that transforms a word into a list of its syllables
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = old_norse_normalize(viisuordh)
            if word:
                self.syllabified.append(syllabifier.syllabify(word))

    def to_phonetics(self, transcriber, with_squared_brackets=True):
        """
        Phonetic transcription of the ShortLine instances.
        :param transcriber: Old Norse transcriber
        :param with_squared_brackets:
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = old_norse_normalize(viisuordh)
            if word:
                transcribed_word = transcriber.text_to_phonetic_representation(
                    word, with_squared_brackets
                )
                # phonological features list, result of Transcriber.text_to_phonemes()
                pfl = transcriber.text_to_phonemes(word)

                self.transcribed.append(transcribed_word)
                self.phonological_features_text.append(pfl)

    @property
    def first_sounds(self):
        """
        The first first sound of each word of the ShortLine.
        :return: first sound of each word
        """
        first_sounds = []
        for viisuord in self.phonological_features_text:
            first_sounds.append(viisuord[0])
        return first_sounds

    def find_alliterations(self, other_short_line):
        """
        Alliterations is the repetition of a same sound pattern (usually the first sound) of important words.
        This usually excludes stop words.

        :param other_short_line: short line to compare with
        :return:
        """
        self.n_alliterations = 0
        self.alliterations = []
        for j, sound1 in enumerate(self.first_sounds):
            word1 = old_norse_normalize(self.tokenized_text[j])
            for k, sound2 in enumerate(other_short_line.first_sounds):
                word2 = old_norse_normalize(other_short_line.tokenized_text[k])
                if word1 not in STOPS and word2 not in STOPS:
                    if (
                        isinstance(sound1, old_norse_transcription.Consonant)
                        and isinstance(sound2, old_norse_transcription.Consonant)
                        and sound1.ipar == sound2.ipar
                    ):
                        self.alliterations.append((word1, word2))
                        self.n_alliterations += 1
                    elif isinstance(
                        sound1, old_norse_transcription.Vowel
                    ) and isinstance(sound2, old_norse_transcription.Vowel):
                        self.alliterations.append((word1, word2))
                        self.n_alliterations += 1
        return self.alliterations, self.n_alliterations


class LongLine:
    """"""

    def __init__(self, text):
        self.text = text
        self.tokenizer = OldNorseWordTokenizer()
        self.short_lines = None
        self.syllabified = []
        self.transcribed = []
        self.alliterations = []
        self.phonological_features_text = []
        self.n_alliterations = 0
        self.syllabified_phonological_features_text = []

    @property
    def tokenized_text(self):
        return self.tokenizer.tokenize(self.text)

    def syllabify(self, syllabifier):
        """
        >>> raw_long_line = "Deyr fé,\\ndeyja frændr"
        >>> short_line = ShortLine(raw_long_line)
        >>> syl = Syllabifier(language="non", break_geminants=True)
        >>> syl.set_invalid_onsets(old_norse_syllabifier.invalid_onsets)
        >>> short_line.syllabify(syl)

        :param syllabifier: Old Norse syllabifier
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = old_norse_normalize(viisuordh)
            if word:
                self.syllabified.append(syllabifier.syllabify(word))

    def to_phonetics(self, transcriber, with_squared_brackets=True):
        """
        Phontic transcription of the ShortLine instances.
        :param transcriber: Old Norse transcriber
        :param with_squared_brackets:
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = old_norse_normalize(viisuordh)
            if word:
                transcribed_word = transcriber.text_to_phonetic_representation(
                    word, with_squared_brackets
                )
                pfl = transcriber.text_to_phonemes(word)

                self.transcribed.append(transcribed_word)
                self.phonological_features_text.append(pfl)

    @property
    def first_sounds(self):
        """
        The first first sound of each word of the ShortLine.
        :return:
        """
        first_sounds = []
        for viisuord in self.phonological_features_text:
            first_sounds.append(viisuord[0])
        return first_sounds

    def find_alliterations(self):
        """
        Alliterations is the repetition of a same sound pattern (usually the first sound) of important words.
        This usually excludes stop words.
        :return:
        """
        self.n_alliterations = 0
        self.alliterations = []
        for j, sound1 in enumerate(self.first_sounds):
            word1 = old_norse_normalize(self.tokenized_text[j])
            if j < len(self.first_sounds) - 1:
                for k, sound2 in enumerate(self.first_sounds[j + 1 :]):
                    word2 = old_norse_normalize(self.tokenized_text[k])
                    if word1 not in STOPS and sound2 not in STOPS:
                        if (
                            isinstance(sound1, old_norse_transcription.Consonant)
                            and sound1.ipar == sound2.ipar
                        ):
                            self.alliterations.append((word1, word2))
                            self.n_alliterations += 1
                        elif isinstance(
                            sound1, old_norse_transcription.Vowel
                        ) and isinstance(sound2, old_norse_transcription.Vowel):
                            self.alliterations.append((word1, word2))
                            self.n_alliterations += 1
        return self.alliterations, self.n_alliterations


class Metre:
    """
    Verse, strophe or stanza. This is here a regular set of meters.
    'Abstract' class which implements global methods on verse.
    """

    def __init__(self):
        """"""
        self.text = ""  # raw text
        self.short_lines = []  # list of minimal lines
        self.long_lines = []  # list of long lines
        self.syllabified_text = []  # each word is replaced by a list of its syllables
        self.transcribed_text = (
            []
        )  # each line is replaced by its phonetic transcription
        self.phonological_features_text = []
        self.syllabified_phonological_features_text = []

    def from_short_lines_text(self, text: str):
        """
        Only implemented in daughter classes.
        :type text: str
        """
        self.text = text

    def syllabify(self, hierarchy: Dict[str, int]):
        """
        Syllables may play a role in verse classification.
        """
        if len(self.long_lines) == 0:
            logger.error("No text was imported")
            self.syllabified_text = []
        else:
            syllabifier = Syllabifier(language="non", break_geminants=True)
            syllabifier.set_hierarchy(hierarchy)
            syllabified_text = []
            for i, long_line in enumerate(self.long_lines):
                syllabified_text.append([])
                for short_line in long_line:
                    assert isinstance(short_line, ShortLine) or isinstance(
                        short_line, LongLine
                    )
                    short_line.syllabify(syllabifier)
                    syllabified_text[i].append(short_line.syllabified)
            self.syllabified_text = syllabified_text

    def to_phonetics(self, with_squared_brackets=True):
        """
        Transcribing words in verse helps find alliteration.
        """
        if len(self.long_lines) == 0:
            logger.error("No text has been imported")
            self.syllabified_text = []
        else:
            transcriber = Transcriber(
                old_norse_transcription.DIPHTHONGS_IPA,
                old_norse_transcription.DIPHTHONGS_IPA_class,
                old_norse_transcription.IPA_class,
                old_norse_transcription.old_norse_rules,
            )
            transcribed_text = []
            phonological_features_text = []
            for i, long_line in enumerate(self.long_lines):
                transcribed_text.append([])
                phonological_features_text.append([])
                for short_line in long_line:
                    assert isinstance(short_line, ShortLine) or isinstance(
                        short_line, LongLine
                    )
                    short_line.to_phonetics(transcriber, with_squared_brackets)
                    transcribed_text[i].append(short_line.transcribed)
                    phonological_features_text[i].append(
                        short_line.phonological_features_text
                    )

            self.transcribed_text = transcribed_text
            self.phonological_features_text = phonological_features_text

    def find_alliteration(self):
        """
        Find alliterations in the complete verse.
        :return:
        """
        if len(self.phonological_features_text) == 0:
            logger.error("No phonological transcription found")
            raise ValueError
        else:
            first_sounds = []
            for i, line in enumerate(self.phonological_features_text):
                first_sounds.append([])
                for j, short_line in enumerate(line):
                    first_sounds[i].append([])
                    for viisuord in short_line:
                        first_sounds[i][j].append(viisuord[0])

            verse_alliterations = []
            n_alliterations_lines = []
            for i, first_sound_line in enumerate(first_sounds):
                if isinstance(self.long_lines[i][0], ShortLine) and isinstance(
                    self.long_lines[i][1], ShortLine
                ):
                    alli, counter = self.long_lines[i][0].find_alliterations(
                        self.long_lines[i][1]
                    )
                    verse_alliterations.append(alli)
                    n_alliterations_lines.append(counter)
                elif isinstance(self.long_lines[i][0], LongLine):
                    alli, counter = self.long_lines[i][0].find_alliterations()
                    verse_alliterations.append(alli)
                    n_alliterations_lines.append(counter)
            return verse_alliterations, n_alliterations_lines


class UnspecifiedStanza(Metre):
    """
    No specific structure. No find_alliteration because it makes only sense
    for long lines.
    """

    def __init__(self):
        Metre.__init__(self)

    def from_short_lines_text(self, text: str):
        """
        Example from Völsupá 28

        >>> stanza = "Ein sat hon úti,\\nþá er inn aldni kom\\nyggjungr ása\\nok í augu leit.\\nHvers fregnið mik?\\nHví freistið mín?\\nAllt veit ek, Óðinn,\\nhvar þú auga falt,\\ní inum mæra\\nMímisbrunni.\\nDrekkr mjöð Mímir\\nmorgun hverjan\\naf veði Valföðrs.\\nVituð ér enn - eða hvat?"
        >>> us = UnspecifiedStanza()
        >>> us.from_short_lines_text(stanza)
        >>> [sl.text for sl in us.short_lines]
        ['Ein sat hon úti,', 'þá er inn aldni kom', 'yggjungr ása', 'ok í augu leit.', 'Hvers fregnið mik?', 'Hví freistið mín?', 'Allt veit ek, Óðinn,', 'hvar þú auga falt,', 'í inum mæra', 'Mímisbrunni.', 'Drekkr mjöð Mímir', 'morgun hverjan', 'af veði Valföðrs.', 'Vituð ér enn - eða hvat?']
        >>> us.long_lines

        :param text: raw text
        :return:
        """
        Metre.from_short_lines_text(self, text)
        self.short_lines = [ShortLine(line) for line in text.split("\n") if line]
        self.long_lines = None

    def syllabify(self, hierarchy: Dict[str, int]):
        """
        >>> stanza = "Ein sat hon úti,\\nþá er inn aldni kom\\nyggjungr ása\\nok í augu leit.\\nHvers fregnið mik?\\nHví freistið mín?\\nAllt veit ek, Óðinn,\\nhvar þú auga falt,\\ní inum mæra\\nMímisbrunni.\\nDrekkr mjöð Mímir\\nmorgun hverjan\\naf veði Valföðrs.\\nVituð ér enn - eða hvat?"
        >>> us = UnspecifiedStanza()
        >>> us.from_short_lines_text(stanza)
        >>> us.syllabify(old_norse_syllabifier.hierarchy)
        >>> us.syllabified_text
        [[['ein'], ['sat'], ['hon'], ['út', 'i']], [['þá'], ['er'], ['inn'], ['al', 'dni'], ['kom']], [['yg', 'gjungr'], ['ás', 'a']], [['ok'], ['í'], ['aug', 'u'], ['leit']], [['hvers'], ['freg', 'nið'], ['mik']], [['hví'], ['freis', 'tið'], ['mín']], [['allt'], ['veit'], ['ek'], ['ó', 'ðinn']], [['hvar'], ['þú'], ['aug', 'a'], ['falt']], [['í'], ['i', 'num'], ['mær', 'a']], [['mí', 'mis', 'brun', 'ni']], [['drekkr'], ['mjöð'], ['mí', 'mir']], [['mor', 'gun'], ['hver', 'jan']], [['af'], ['veð', 'i'], ['val', 'föðrs']], [['vi', 'tuð'], ['ér'], ['enn'], ['eð', 'a'], ['hvat']]]

        :param hierarchy: phonetic hierarchy
        :return:
        """
        syllabifier = Syllabifier(language="non", break_geminants=True)
        syllabifier.set_hierarchy(hierarchy)
        syllabified_text = []
        for short_line in self.short_lines:
            assert isinstance(short_line, ShortLine)
            short_line.syllabify(syllabifier)
            syllabified_text.append(short_line.syllabified)
        self.syllabified_text = syllabified_text

    def to_phonetics(self, with_squared_brackets=True):
        """
        >>> stanza = "Ein sat hon úti,\\nþá er inn aldni kom\\nyggjungr ása\\nok í augu leit.\\nHvers fregnið mik?\\nHví freistið mín?\\nAllt veit ek, Óðinn,\\nhvar þú auga falt,\\ní inum mæra\\nMímisbrunni.\\nDrekkr mjöð Mímir\\nmorgun hverjan\\naf veði Valföðrs.\\nVituð ér enn - eða hvat?"
        >>> us = UnspecifiedStanza()
        >>> us.from_short_lines_text(stanza)
        >>> us.to_phonetics(False)
        >>> us.transcribed_text
        [['ɛin', 'sat', 'hɔn', 'uːti'], ['θaː', 'ɛr', 'inː', 'aldni', 'kɔm'], ['ygːjunɣr', 'aːsa'], ['ɔk', 'iː', 'ɒuɣu', 'lɛit'], ['hvɛrs', 'frɛɣnið', 'mik'], ['hviː', 'frɛistið', 'miːn'], ['alːt', 'vɛit', 'ɛk', 'oːðinː'], ['hvar', 'θuː', 'ɒuɣa', 'falt'], ['iː', 'inum', 'mɛːra'], ['miːmisbrunːi'], ['drɛkːr', 'mjœð', 'miːmir'], ['mɔrɣun', 'hvɛrjan'], ['av', 'vɛði', 'valvœðrs'], ['vituð', 'eːr', 'ɛnː', 'ɛða', 'hvat']]

        :return:
        """
        transcriber = Transcriber(
            old_norse_transcription.DIPHTHONGS_IPA,
            old_norse_transcription.DIPHTHONGS_IPA_class,
            old_norse_transcription.IPA_class,
            old_norse_transcription.old_norse_rules,
        )
        transcribed_text = []
        phonological_features_text = []
        for short_line in self.short_lines:
            assert isinstance(short_line, ShortLine) or isinstance(short_line, LongLine)
            short_line.to_phonetics(transcriber, with_squared_brackets)
            transcribed_text.append(short_line.transcribed)
            phonological_features_text.append(short_line.phonological_features_text)
        self.transcribed_text = transcribed_text
        self.phonological_features_text = phonological_features_text

    def find_alliteration(self):
        """
        Alliterations in short lines make no sense.

        >>> stanza = "Ein sat hon úti,\\nþá er inn aldni kom\\nyggjungr ása\\nok í augu leit.\\nHvers fregnið mik?\\nHví freistið mín?\\nAllt veit ek, Óðinn,\\nhvar þú auga falt,\\ní inum mæra\\nMímisbrunni.\\nDrekkr mjöð Mímir\\nmorgun hverjan\\naf veði Valföðrs.\\nVituð ér enn - eða hvat?"
        >>> us = UnspecifiedStanza()
        >>> us.from_short_lines_text(stanza)
        >>> us.to_phonetics()
        >>> us.find_alliteration()
        ([], 0)

        :return:
        """
        return [], 0


class Fornyrdhislag(Metre):
    """**Fornyrðislag** has two lifts per half line, with two or three (sometimes one)
    unstressed syllables. At least two lifts, usually three, alliterate,
    always including the main stave (the first lift of the second half-line).
    (See https://en.wikipedia.org/wiki/Alliterative_verse#Old_Norse_poetic_forms)

    """

    def __init__(self):
        Metre.__init__(self)

    def from_short_lines_text(self, text: str):
        """
        Famous example from Völsupá 1st stanza

        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> [sl.text for sl in fo.short_lines]
        ['Hljóðs bið ek allar', 'helgar kindir,', 'meiri ok minni', 'mögu Heimdallar;', 'viltu at ek, Valföðr,', 'vel fyr telja', 'forn spjöll fira,', 'þau er fremst of man.']
        >>> [[sl.text for sl in long_line] for long_line in fo.long_lines]
        [['Hljóðs bið ek allar', 'helgar kindir,'], ['meiri ok minni', 'mögu Heimdallar;'], ['viltu at ek, Valföðr,', 'vel fyr telja'], ['forn spjöll fira,', 'þau er fremst of man.']]

        :param text: raw text
        :return:
        """
        self.text = text
        self.short_lines = [ShortLine(line) for line in text.split("\n") if line]
        self.long_lines = [
            self.short_lines[2 * i : 2 * i + 2]
            for i in range(int(floor(len(self.short_lines) / 2)))
        ]

    def syllabify(self, hierarchy: Dict[str, int]):
        """
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.syllabify(old_norse_syllabifier.hierarchy)
        >>> fo.syllabified_text
        [[[['hljóðs'], ['bið'], ['ek'], ['al', 'lar']], [['hel', 'gar'], ['kin', 'dir']]], [[['meir', 'i'], ['ok'], ['min', 'ni']], [['mög', 'u'], ['heim', 'dal', 'lar']]], [[['vil', 'tu'], ['at'], ['ek'], ['val', 'föðr']], [['vel'], ['fyr'], ['tel', 'ja']]], [[['forn'], ['spjöll'], ['fir', 'a']], [['þau'], ['er'], ['fremst'], ['of'], ['man']]]]

        :param hierarchy: phonetic hierarchy
        :return:
        """
        Metre.syllabify(self, hierarchy)

    def to_phonetics(self, with_squared_brackets=True):
        """
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.to_phonetics(False)
        >>> fo.transcribed_text
        [[['hljoːðs', 'bið', 'ɛk', 'alːar'], ['hɛlɣar', 'kindir']], [['mɛiri', 'ɔk', 'minːi'], ['mœɣu', 'hɛimdalːar']], [['viltu', 'at', 'ɛk', 'valvœðr'], ['vɛl', 'fyr', 'tɛlja']], [['fɔrn', 'spjœlː', 'fira'], ['θɒu', 'ɛr', 'frɛmst', 'ɔv', 'man']]]

        :return:
        """
        Metre.to_phonetics(self, with_squared_brackets)

    def find_alliteration(self):
        """
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.to_phonetics()
        >>> fo.find_alliteration()
        ([[('hljóðs', 'helgar')], [('meiri', 'mögu'), ('minni', 'mögu')], [], [('forn', 'fremst'), ('fira', 'fremst')]], [1, 2, 0, 2])

        :return:
        """
        return Metre.find_alliteration(self)


class Ljoodhhaattr(Metre):
    """
    Ljóðaháttr is a stanzaic verse form that created four line stanzas.
    The odd numbered lines were almost standard lines of alliterative verse
    with four lifts and two or three alliterations, with cæsura;
    the even numbered lines had three lifts and two alliterations, and no cæsura.

    See https://en.wikipedia.org/wiki/Alliterative_verse#Lj%C3%B3%C3%B0ah%C3%A1ttr.

    """

    def __init__(self):
        Metre.__init__(self)

    def from_short_lines_text(self, text: str):
        """
        Famous example from Hávamál 77

        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj = Ljoodhhaattr()
        >>> lj.from_short_lines_text(text)
        >>> [sl.text for sl in lj.short_lines]
        ['Deyr fé,', 'deyja frændr,', 'deyr sjalfr it sama,', 'ek veit einn,', 'at aldrei deyr:', 'dómr um dauðan hvern.']
        >>> [[sl.text for sl in long_line] for long_line in lj.long_lines]
        [['Deyr fé,', 'deyja frændr,'], ['deyr sjalfr it sama,'], ['ek veit einn,', 'at aldrei deyr:'], ['dómr um dauðan hvern.']]

        :param text:
        :return:
        """
        Metre.from_short_lines_text(self, text)
        lines = [line for line in text.split("\n") if line]
        self.short_lines = [
            ShortLine(lines[0]),
            ShortLine(lines[1]),
            LongLine(lines[2]),
            ShortLine(lines[3]),
            ShortLine(lines[4]),
            LongLine(lines[5]),
        ]
        self.long_lines = [
            self.short_lines[0:2],
            [self.short_lines[2]],
            self.short_lines[3:5],
            [self.short_lines[5]],
        ]

    def syllabify(self, hierarchy: Dict[str, int]):
        """
        >>> lj = Ljoodhhaattr()
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj.from_short_lines_text(text)
        >>> lj.syllabify(old_norse_syllabifier.hierarchy)
        >>> lj.syllabified_text
        [[[['deyr'], ['fé']], [['deyj', 'a'], ['frændr']]], [[['deyr'], ['sjalfr'], ['it'], ['sam', 'a']]], [[['ek'], ['veit'], ['einn']], [['at'], ['al', 'drei'], ['deyr']]], [[['dómr'], ['um'], ['dau', 'ðan'], ['hvern']]]]

        :param hierarchy: phonetic hierarchy
        :return:
        """
        Metre.syllabify(self, hierarchy)

    def to_phonetics(self, with_squared_brackets=True):
        """
        >>> lj = Ljoodhhaattr()
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj.from_short_lines_text(text)
        >>> lj.to_phonetics(False)
        >>> lj.transcribed_text
        [[['dɐyr', 'feː'], ['dɐyja', 'frɛːndr']], [['dɐyr', 'sjalvr', 'it', 'sama']], [['ɛk', 'vɛit', 'ɛinː'], ['at', 'aldrɛi', 'dɐyr']], [['doːmr', 'um', 'dɒuðan', 'hvɛrn']]]

        """
        Metre.to_phonetics(self, with_squared_brackets)

    def find_alliteration(self) -> Tuple[list, list]:
        """
        >>> poem = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj = Ljoodhhaattr()
        >>> lj.from_short_lines_text(poem)
        >>> lj.to_phonetics()
        >>> verse_alliterations, n_alliterations_lines = lj.find_alliteration()
        >>> verse_alliterations
        [[('deyr', 'deyja'), ('fé', 'frændr')], [('sjalfr', 'sjalfr')], [('einn', 'aldrei')], [('dómr', 'um')]]
        >>> n_alliterations_lines
        [2, 1, 1, 1]

        :return:
        """
        return Metre.find_alliteration(self)


class MetreManager:
    """
    Handles different kinds of meter in Old Norse poetry.

    * Fornyrðislag
    * Ljóðaháttr
    """

    @staticmethod
    def is_fornyrdhislag(text: str) -> bool:
        """
        Basic check, only the number of lines matters: 8 for fornyrðislag.

        >>> text1 = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> text2 = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> MetreManager.is_fornyrdhislag(text1)
        True
        >>> MetreManager.is_fornyrdhislag(text2)
        False

        :param text:
        :return:
        """
        lines = [line for line in text.split("\n") if line]
        return len(lines) == 8

    @staticmethod
    def is_ljoodhhaattr(text: str) -> bool:
        """
        Basic check, only the number of lines matters: 6 for ljóðaháttr

        >>> text1 = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> text2 = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> MetreManager.is_ljoodhhaattr(text1)
        False
        >>> MetreManager.is_ljoodhhaattr(text2)
        True

        :param text:
        :return:
        """
        lines = [line for line in text.split("\n") if line]
        return len(lines) == 6

    @staticmethod
    def load_poem_from_paragraphs(paragraphs: List[str]):
        """
        Deals with a list of paragraphs:
        - detects its category,
        - processes it.

        >>> text1 = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> text2 = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."

        >>> paragraphs = [text1, text2]
        >>> poem = MetreManager.load_poem_from_paragraphs(paragraphs)
        >>> isinstance(poem[0], Fornyrdhislag)
        True
        >>> isinstance(poem[1], Ljoodhhaattr)
        True

        :param paragraphs: list of stanzas (list of strings)
        :return: list of Fornyrdhislag or Ljoodhhaattr instances
        """
        poem = []
        for paragraph in paragraphs:
            if MetreManager.is_fornyrdhislag(paragraph):
                fnl = Fornyrdhislag()
                fnl.from_short_lines_text(paragraph)
                fnl.syllabify(old_norse_syllabifier.hierarchy)
                fnl.to_phonetics()
                poem.append(fnl)
            elif MetreManager.is_ljoodhhaattr(paragraph):
                lh = Ljoodhhaattr()
                lh.from_short_lines_text(paragraph)
                lh.syllabify(old_norse_syllabifier.hierarchy)
                lh.to_phonetics()
                poem.append(lh)
            else:
                stanza = UnspecifiedStanza()
                stanza.from_short_lines_text(paragraph)
                stanza.syllabify(old_norse_syllabifier.hierarchy)
                stanza.to_phonetics()
                poem.append(stanza)
        return poem
