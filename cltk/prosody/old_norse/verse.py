"""Verse structures of Old Norse poetry"""


import re
from math import floor
from cltk.phonology.utils import Transcriber
from cltk.phonology.old_norse.transcription import Consonant, Vowel, old_norse_rules, IPA_class, \
    DIPHTHONGS_IPA_class, DIPHTHONGS_IPA, measure_old_norse_syllable
from cltk.phonology.syllabify import Syllabifier
from cltk.tokenize.word import WordTokenizer
import cltk.corpus.old_norse.syllabifier as old_norse_syllabifier
from cltk.stop.old_norse.stops import STOPS_LIST
from cltk.utils.cltk_logger import logger
from cltk.tag.pos import POSTag

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


# extension of stop words for poetry
stops_for_poetry = ["ek",
                    "it"]  # to be completed
STOPS_LIST.extend(stops_for_poetry)


def normalize(text):
    res = text.lower()
    res = re.sub(r"[\-:?;.,]", "", res)
    res = re.sub(r" +", " ", res)
    return res


class MetreManager:
    """
    * Fornyrðislag
    * Ljóðaháttr
    """
    @staticmethod
    def is_fornyrdhislag(text: str):
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
    def is_ljoodhhaattr(text: str):
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
    def load_poem_from_paragraphs(paragraphs):
        """

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


class ShortLine:
    def __init__(self, text):
        self.text = text
        self.tokenizer = WordTokenizer('old_norse')
        self.tokenized_text = self.tokenizer.tokenize(text)
        self.first_sounds = []
        self.syllabified = []
        self.transcribed = []
        self.alliterations = {}
        self.phonological_features_text = []
        self.n_alliterations = 0

        # self.syllabified_transcribed_text = []
        self.syllabified_phonological_features_text = []

    def syllabify(self, syllabifier):
        """

        :param syllabifier:
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = normalize(viisuordh)
            if word:
                self.syllabified.append(syllabifier.syllabify(word))

    def to_phonetics(self, transcriber):
        """
        Phontic transcription of the ShortLine instances.
        :param transcriber:
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = normalize(viisuordh)
            if word:
                transcribed_word = transcriber.text_to_phonetic_representation(word)
                # phonological features list, result of Transcriber.text_to_phonemes()
                pfl = transcriber.text_to_phonemes(word)

                self.transcribed.append(transcribed_word)
                self.phonological_features_text.append(pfl)
        self.get_first_sounds()

    def get_first_sounds(self):
        """
        The first first sound of each word of the ShortLine.
        :return:
        """
        self.first_sounds = []
        for viisuord in self.phonological_features_text:
            self.first_sounds.append(viisuord[0])

    def find_alliterations(self, other_short_line):
        """
        Alliterations is the repetition of a same sound pattern (usually the first sound) of important words.
        This usually excludes stop words.
        :param other_short_line:
        :return:
        """
        self.n_alliterations = 0
        self.alliterations = []
        for j, sound1 in enumerate(self.first_sounds):
            word1 = normalize(self.tokenized_text[j])
            for k, sound2 in enumerate(other_short_line.first_sounds):
                word2 = normalize(other_short_line.tokenized_text[k])
                if word1 not in STOPS_LIST and word2 not in STOPS_LIST:
                    if isinstance(sound1, Consonant) and isinstance(sound2, Consonant) and \
                            sound1.ipar == sound2.ipar:
                        self.alliterations.append((word1, word2))
                        self.n_alliterations += 1
                    elif isinstance(sound1, Vowel) and isinstance(sound2, Vowel):
                        self.alliterations.append((word1, word2))
                        self.n_alliterations += 1
        return self.alliterations, self.n_alliterations


class LongLine:
    def __init__(self, text):
        self.text = text
        self.tokenizer = WordTokenizer('old_norse')
        self.tokenized_text = self.tokenizer.tokenize(text)
        self.short_lines = None
        self.first_sounds = []
        self.syllabified = []
        self.transcribed = []
        self.alliterations = []
        self.phonological_features_text = []
        self.n_alliterations = 0
        self.syllabified_phonological_features_text = []

    def syllabify(self, syllabifier):
        """

        :param syllabifier:
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = normalize(viisuordh)
            if word:
                self.syllabified.append(syllabifier.syllabify(word))

    def to_phonetics(self, transcriber):
        """
        Phontic transcription of the ShortLine instances.
        :param transcriber:
        :return:
        """
        for viisuordh in self.tokenized_text:
            word = normalize(viisuordh)
            if word:
                transcribed_word = transcriber.text_to_phonetic_representation(word)
                pfl = transcriber.text_to_phonemes(word)

                self.transcribed.append(transcribed_word)
                self.phonological_features_text.append(pfl)
        self.get_first_sounds()

    def get_first_sounds(self):
        """
        The first first sound of each word of the ShortLine.
        :return:
        """
        self.first_sounds = []
        for viisuord in self.phonological_features_text:
            self.first_sounds.append(viisuord[0])

    def find_alliterations(self):
        """
        Alliterations is the repetition of a same sound pattern (usually the first sound) of important words.
        This usually excludes stop words.
        :return:
        """
        self.n_alliterations = 0
        self.alliterations = []
        for j, sound1 in enumerate(self.first_sounds):
            word1 = normalize(self.tokenized_text[j])
            if j < len(self.first_sounds)-1:
                for k, sound2 in enumerate(self.first_sounds[j+1:]):
                    word2 = normalize(self.tokenized_text[k])
                    if word1 not in STOPS_LIST and sound2 not in STOPS_LIST:
                        if isinstance(sound1, Consonant) and sound1.ipar == sound2.ipar:
                            self.alliterations.append((word1, word2))
                            self.n_alliterations += 1
                        elif isinstance(sound1, Vowel) and isinstance(sound2, Vowel):
                            self.alliterations.append((word1, word2))
                            self.n_alliterations += 1
        return self.alliterations, self.n_alliterations


class Metre:
    """
    Verse, strophe or stanza. This is here a regular set of meters.
    'Abstract' class which implements global methods on verse.
    """
    def __init__(self):
        """

        """
        self.text = ""
        self.short_lines = []  # list of minimal lines
        self.long_lines = []  # list of long lines
        self.syllabified_text = []  # each word is replaced by a list of its syllables
        self.transcribed_text = []  # each line is replaced by its phonetic transcription
        self.phonological_features_text = []
        self.syllabified_phonological_features_text = []

    def from_short_lines_text(self, text: str):
        """
        Only implemented in daughter classes.
        :type text: str
        """
        self.text = text

    def syllabify(self, hierarchy):
        """
        Syllables may play a role in verse classification.
        """
        if len(self.long_lines) == 0:
            logger.error("No text was imported")
            self.syllabified_text = []
        else:
            syllabifier = Syllabifier(language="old_norse", break_geminants=True)
            syllabifier.set_hierarchy(hierarchy)
            syllabified_text = []
            for i, long_line in enumerate(self.long_lines):
                syllabified_text.append([])
                for short_line in long_line:
                    assert isinstance(short_line, ShortLine) or isinstance(short_line, LongLine)
                    short_line.syllabify(syllabifier)
                    syllabified_text[i].append(short_line.syllabified)
            self.syllabified_text = syllabified_text

    def to_phonetics(self):
        """
        Transcribing words in verse helps find alliteration.
        """
        if len(self.long_lines) == 0:
            logger.error("No text was imported")
            self.syllabified_text = []
        else:
            transcriber = Transcriber(DIPHTHONGS_IPA, DIPHTHONGS_IPA_class, IPA_class, old_norse_rules)
            transcribed_text = []
            phonological_features_text = []
            for i, long_line in enumerate(self.long_lines):
                transcribed_text.append([])
                phonological_features_text.append([])
                for short_line in long_line:
                    assert isinstance(short_line, ShortLine) or isinstance(short_line, LongLine)
                    short_line.to_phonetics(transcriber)
                    transcribed_text[i].append(short_line.transcribed)
                    phonological_features_text[i].append(short_line.phonological_features_text)

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
                if isinstance(self.long_lines[i][0], ShortLine) and isinstance(self.long_lines[i][1], ShortLine):
                    self.long_lines[i][0].get_first_sounds()
                    self.long_lines[i][1].get_first_sounds()
                    alli, counter = self.long_lines[i][0].find_alliterations(self.long_lines[i][1])
                    verse_alliterations.append(alli)
                    n_alliterations_lines.append(counter)
                elif isinstance(self.long_lines[i][0], LongLine):
                    self.long_lines[i][0].get_first_sounds()
                    alli, counter = self.long_lines[i][0].find_alliterations()
                    verse_alliterations.append(alli)
                    n_alliterations_lines.append(counter)
            return verse_alliterations, n_alliterations_lines


class UnspecifiedStanza(Metre):
    """
    No specific structure. No find_alliteration because it makes only sense for long lines.
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

        :param text:
        :return:
        """
        Metre.from_short_lines_text(self, text)
        self.short_lines = [ShortLine(line) for line in text.split("\n") if line]
        self.long_lines = None

    def syllabify(self, hierarchy):
        """
        >>> stanza = "Ein sat hon úti,\\nþá er inn aldni kom\\nyggjungr ása\\nok í augu leit.\\nHvers fregnið mik?\\nHví freistið mín?\\nAllt veit ek, Óðinn,\\nhvar þú auga falt,\\ní inum mæra\\nMímisbrunni.\\nDrekkr mjöð Mímir\\nmorgun hverjan\\naf veði Valföðrs.\\nVituð ér enn - eða hvat?"
        >>> us = UnspecifiedStanza()
        >>> us.from_short_lines_text(stanza)
        >>> us.syllabify(old_norse_syllabifier.hierarchy)
        >>> us.syllabified_text
        [[['ein'], ['sat'], ['hon'], ['út', 'i']], [['þá'], ['er'], ['inn'], ['al', 'dni'], ['kom']], [['yg', 'gjungr'], ['ás', 'a']], [['ok'], ['í'], ['aug', 'u'], ['leit']], [['hvers'], ['freg', 'nið'], ['mik']], [['hví'], ['freis', 'tið'], ['mín']], [['allt'], ['veit'], ['ek'], ['ó', 'ðinn']], [['hvar'], ['þú'], ['aug', 'a'], ['falt']], [['í'], ['i', 'num'], ['mær', 'a']], [['mí', 'mis', 'brun', 'ni']], [['drekkr'], ['mjöð'], ['mí', 'mir']], [['mor', 'gun'], ['hver', 'jan']], [['af'], ['veð', 'i'], ['val', 'föðrs']], [['vi', 'tuð'], ['ér'], ['enn'], ['eð', 'a'], ['hvat']]]

        :param hierarchy:
        :return:
        """
        syllabifier = Syllabifier(language="old_norse", break_geminants=True)
        syllabifier.set_hierarchy(hierarchy)
        syllabified_text = []
        for short_line in self.short_lines:
            assert isinstance(short_line, ShortLine)
            short_line.syllabify(syllabifier)
            syllabified_text.append(short_line.syllabified)
        self.syllabified_text = syllabified_text

    def to_phonetics(self):
        """
        >>> stanza = "Ein sat hon úti,\\nþá er inn aldni kom\\nyggjungr ása\\nok í augu leit.\\nHvers fregnið mik?\\nHví freistið mín?\\nAllt veit ek, Óðinn,\\nhvar þú auga falt,\\ní inum mæra\\nMímisbrunni.\\nDrekkr mjöð Mímir\\nmorgun hverjan\\naf veði Valföðrs.\\nVituð ér enn - eða hvat?"
        >>> us = UnspecifiedStanza()
        >>> us.from_short_lines_text(stanza)
        >>> us.to_phonetics()
        >>> us.transcribed_text
        [['[ɛin]', '[sat]', '[hɔn]', '[uːti]'], ['[θaː]', '[ɛr]', '[inː]', '[aldni]', '[kɔm]'], ['[ygːjunɣr]', '[aːsa]'], ['[ɔk]', '[iː]', '[ɒuɣu]', '[lɛit]'], ['[hvɛrs]', '[frɛɣnið]', '[mik]'], ['[hviː]', '[frɛistið]', '[miːn]'], ['[alːt]', '[vɛit]', '[ɛk]', '[oːðinː]'], ['[hvar]', '[θuː]', '[ɒuɣa]', '[falt]'], ['[iː]', '[inum]', '[mɛːra]'], ['[miːmisbrunːi]'], ['[drɛkːr]', '[mjœð]', '[miːmir]'], ['[mɔrɣun]', '[hvɛrjan]'], ['[av]', '[vɛði]', '[valvœðrs]'], ['[vituð]', '[eːr]', '[ɛnː]', '[ɛða]', '[hvat]']]

        :return:
        """
        transcriber = Transcriber(DIPHTHONGS_IPA, DIPHTHONGS_IPA_class, IPA_class, old_norse_rules)
        transcribed_text = []
        phonological_features_text = []
        for short_line in self.short_lines:
            assert isinstance(short_line, ShortLine) or isinstance(short_line, LongLine)
            short_line.to_phonetics(transcriber)
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
    """
    Fornyrðislag :

    short lines:
    --------
    --------
    --------
    --------
    --------
    --------
    --------

    long lines:
    -------- --------
    -------- --------
    -------- --------
    -------- --------

    """
    def __init__(self):
        Metre.__init__(self)

    def from_short_lines_text(self, text: str):
        """
        Famous example from Völsupá 1
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> [sl.text for sl in fo.short_lines]
        ['Hljóðs bið ek allar', 'helgar kindir,', 'meiri ok minni', 'mögu Heimdallar;', 'viltu at ek, Valföðr,', 'vel fyr telja', 'forn spjöll fira,', 'þau er fremst of man.']
        >>> [[sl.text for sl in long_line] for long_line in fo.long_lines]
        [['Hljóðs bið ek allar', 'helgar kindir,'], ['meiri ok minni', 'mögu Heimdallar;'], ['viltu at ek, Valföðr,', 'vel fyr telja'], ['forn spjöll fira,', 'þau er fremst of man.']]

        :param text:
        :return:
        """
        self.text = text
        self.short_lines = [ShortLine(line) for line in text.split("\n") if line]
        self.long_lines = [self.short_lines[2*i:2*i+2] for i in range(int(floor(len(self.short_lines)/2)))]

    def syllabify(self, hierarchy):
        """
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.syllabify(old_norse_syllabifier.hierarchy)
        >>> fo.syllabified_text
        [[[['hljóðs'], ['bið'], ['ek'], ['al', 'lar']], [['hel', 'gar'], ['kin', 'dir']]], [[['meir', 'i'], ['ok'], ['min', 'ni']], [['mög', 'u'], ['heim', 'dal', 'lar']]], [[['vil', 'tu'], ['at'], ['ek'], ['val', 'föðr']], [['vel'], ['fyr'], ['tel', 'ja']]], [[['forn'], ['spjöll'], ['fir', 'a']], [['þau'], ['er'], ['fremst'], ['of'], ['man']]]]

        :return:
        """
        Metre.syllabify(self, hierarchy)

    def to_phonetics(self):
        """
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.to_phonetics()
        >>> fo.transcribed_text
        [[['[hljoːðs]', '[bið]', '[ɛk]', '[alːar]'], ['[hɛlɣar]', '[kindir]']], [['[mɛiri]', '[ɔk]', '[minːi]'], ['[mœɣu]', '[hɛimdalːar]']], [['[viltu]', '[at]', '[ɛk]', '[valvœðr]'], ['[vɛl]', '[fyr]', '[tɛlja]']], [['[fɔrn]', '[spjœlː]', '[fira]'], ['[θɒu]', '[ɛr]', '[frɛmst]', '[ɔv]', '[man]']]]

        :return:
        """
        Metre.to_phonetics(self)

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
    Ljóðaháttr

    Short lines:
    --------
    --------
    ----------------
    --------
    --------
    ----------------

    Long lines :
    -------- --------
    ----------------
    -------- --------
    ----------------
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
        self.short_lines = [ShortLine(lines[0]), ShortLine(lines[1]), LongLine(lines[2]), ShortLine(lines[3]),
                            ShortLine(lines[4]), LongLine(lines[5])]
        self.long_lines = [self.short_lines[0:2], [self.short_lines[2]], self.short_lines[3:5], [self.short_lines[5]]]

    def syllabify(self, hierarchy):
        """
        >>> lj = Ljoodhhaattr()
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj.from_short_lines_text(text)
        >>> lj.syllabify(old_norse_syllabifier.hierarchy)
        >>> lj.syllabified_text
        [[[['deyr'], ['fé']], [['deyj', 'a'], ['frændr']]], [[['deyr'], ['sjalfr'], ['it'], ['sam', 'a']]], [[['ek'], ['veit'], ['einn']], [['at'], ['al', 'drei'], ['deyr']]], [[['dómr'], ['um'], ['dau', 'ðan'], ['hvern']]]]

        :return:
        """
        Metre.syllabify(self, hierarchy)

    def to_phonetics(self):
        """
        >>> lj = Ljoodhhaattr()
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj.from_short_lines_text(text)
        >>> lj.to_phonetics()
        >>> lj.transcribed_text
        [[['[dɐyr]', '[feː]'], ['[dɐyja]', '[frɛːndr]']], [['[dɐyr]', '[sjalvr]', '[it]', '[sama]']], [['[ɛk]', '[vɛit]', '[ɛinː]'], ['[at]', '[aldrɛi]', '[dɐyr]']], [['[doːmr]', '[um]', '[dɒuðan]', '[hvɛrn]']]]

        """
        Metre.to_phonetics(self)

    def find_alliteration(self):
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


class PoetryTools:
    """
    Class which gathers tools necessary for poem analysis:
    * a syllabifier
    * a phonetic transcriber
    * a parts-of-speech tagger
    """
    def __init__(self):
        self.syllabifier = Syllabifier(language="old_norse_ipa")
        self.tr = Transcriber(DIPHTHONGS_IPA, DIPHTHONGS_IPA_class, IPA_class, old_norse_rules)
        self.tagger = POSTag('old_norse')


class PoeticWord:
    """
    This class helps extract all relevant features of a poem word at once.
    Features are:
    * the raw text
    * the syllabified word
    * the syllable length of the word
    * stress of syllables
    * the parts-of-speech of the word

    """
    def __init__(self, text):
        self.text = text
        self.syl = []
        self.length = []
        self.stress = []
        self.ipa_transcription = []

    def parse_word_with(self, poetry_tools: PoetryTools):
        """
        Compute the phonetic transcription of the word with IPA representation
        Compute the syllables of the word
        Compute the length of each syllable
        Compute if a syllable is stress of noe
        Compute the POS category the word is in

        :param poetry_tools: instance of PoetryTools
        :return:
        """
        phonemes = poetry_tools.tr.text_to_phonemes(self.text)
        self.syl = poetry_tools.syllabifier.syllabify_phonemes(phonemes)
        for i, syllable in enumerate(self.syl):
            self.ipa_transcription.append([])
            syl_len = measure_old_norse_syllable(syllable).value
            syl_stress = 1 if i == 0 else 0

            self.length.append(syl_len)
            self.stress.append(syl_stress)
            for c in syllable:
                self.ipa_transcription[i].append(c.ipar)
