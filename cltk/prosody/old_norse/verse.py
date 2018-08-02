"""Verse structures of Old Norse poetry"""

from math import floor
from cltk.phonology.old_norse.transcription import Transcriber,  old_norse_rules, IPA_class, DIPHTHONGS_IPA_class, \
    DIPHTHONGS_IPA
from cltk.phonology.syllabify import Syllabifier
from cltk.tokenize.word import tokenize_old_norse_words
from cltk.utils.cltk_logger import logger

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


class VerseManager:
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
        >>> VerseManager.is_fornyrdhislag(text1)
        True
        >>> VerseManager.is_fornyrdhislag(text2)
        False

        :param text:
        :return:
        """
        l = [line for line in text.split("\n") if line != ""]
        return len(l) == 8

    @staticmethod
    def is_ljoodhhaattr(text: str):
        """
        Basic check, only the number of lines matters: 6 for ljóðaháttr

        >>> text1 = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> text2 = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> VerseManager.is_ljoodhhaattr(text1)
        False
        >>> VerseManager.is_ljoodhhaattr(text2)
        True

        :param text:
        :return:
        """
        l = [line for line in text.split("\n") if line != ""]
        return len(l) == 6
    
    # @staticmethod
    # def extract_verse(text: str):
    #    """
    #    From text to the corresponding verse structure
    #    :return : verse or None
    #    """
    #    if Verse.is_fornyrdhislag(text):            
    #        fo = Fornyrdhislag()
    #        fo.from_short_lines_text(text)
    #        return fo
    #    elif Verse.is_ljoodhhaattr(text):
    #        lj = Ljoodhhaattr()
    #        lj.from_short_lines_text(text)
    #        return lj
    #    else:
    #        return None


class Verse:
    """
    Verse, strophe or stanza. This is here a regular set of meters.
    'Abstract' class which implements global methods on verse.
    """
    def __init__(self):
        """

        """
        self.short_lines = []  # list of minimal lines
        self.long_lines = []  # list of long lines  
        self.syllabified_text = []  # each word is replaced by a list of its syllables
        self.transcribed_text = []  # each line is replaced by its phonetical transcription

    def from_short_lines_text(self, text: str):
        """
        Only implemented in daughter classes.
        """
        pass

    def syllabify(self):
        """
        Syllables may play a role in verse classification.
        """
        if len(self.long_lines) == 0:
            logger.error("No text was imported")
            self.syllabified_text = []
        else:
            syllabifier = Syllabifier(language="old_norse", break_geminants=True)
            syllabified_text = []
            for i, line in enumerate(self.long_lines):
                syllabified_text.append([])
                for j, viisuordh in enumerate(line):
                    syllabified_text[i].append([])
                    words = []
                    for word in tokenize_old_norse_words(viisuordh):
                        # punctuation is not necessary here
                        word = word.replace(",", "")
                        word = word.replace(".", "")
                        word = word.replace(";", "")
                        word = word.replace("!", "")
                        word = word.replace("?", "")
                        word = word.replace("-", "")
                        word = word.replace(":", "")
                        if word != '':
                            words.append(syllabifier.syllabify(word.lower()))
                    syllabified_text[i][j].append(words)
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
            for i, line in enumerate(self.long_lines):
                transcribed_text.append([])
                for viisuordh in line:
                    transcribed_text[i].append(transcriber.main(viisuordh))
            self.transcribed_text = transcribed_text


class Fornyrdhislag(Verse):
    """
    # Fornyrðislag :

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
        Verse.__init__(self)
        self.text = ""
        self.long_lines = []
        self.short_lines = []

    def from_short_lines_text(self, text: str):
        """
        Famous example from Völsupá 1
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.short_lines
        ['Hljóðs bið ek allar', 'helgar kindir,', 'meiri ok minni', 'mögu Heimdallar;', 'viltu at ek, Valföðr,', 'vel fyr telja', 'forn spjöll fira,', 'þau er fremst of man.']
        >>> fo.long_lines
        [['Hljóðs bið ek allar', 'helgar kindir,'], ['meiri ok minni', 'mögu Heimdallar;'], ['viltu at ek, Valföðr,', 'vel fyr telja'], ['forn spjöll fira,', 'þau er fremst of man.']]

        :param text:
        :return:
        """
        self.text = text
        self.short_lines = [line for line in text.split("\n") if line != ""]
        self.long_lines = [self.short_lines[2*i:2*i+2] for i in range(int(floor(len(self.short_lines)/2)))]

    def syllabify(self):
        """
        >>> text = "Hljóðs bið ek allar\\nhelgar kindir,\\nmeiri ok minni\\nmögu Heimdallar;\\nviltu at ek, Valföðr,\\nvel fyr telja\\nforn spjöll fira,\\nþau er fremst of man."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.syllabify()
        >>> fo.syllabified_text
        [[[[['hljóðs'], ['bið'], ['ek'], ['al', 'lar']]], [[['hel', 'gar'], ['kin', 'dir']]]], [[[['meir', 'i'], ['ok'], ['min', 'ni']]], [[['mög', 'u'], ['heim', 'dal', 'lar']]]], [[[['vil', 'tu'], ['at'], ['ek'], ['val', 'föðr']]], [[['vel'], ['fyr'], ['tel', 'ja']]]], [[[['forn'], ['spjöll'], ['fir', 'a']]], [[['þau'], ['er'], ['fremst'], ['of'], ['man']]]]]

        :return:
        """
        Verse.syllabify(self)

    def to_phonetics(self):
        """
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> fo = Fornyrdhislag()
        >>> fo.from_short_lines_text(text)
        >>> fo.to_phonetics()
        >>> fo.transcribed_text
        [['[dɐyr feː]', '[dɐyja frɛːndr]'], ['[dɐyr sjalvr it sama]', '[ɛk vɛit ɛinː]'], ['[at aldrɛi dɐyr]', '[doːmr um dɒuðan hvɛrn]']]

        :return:
        """
        Verse.to_phonetics(self)


class Ljoodhhaattr(Verse):
    """
    Ljóðaháttr
    """
    def __init__(self):
        Verse.__init__(self)
        self.text = ""
        self.long_lines = []
        self.short_lines = []
        self.syllabified_text = []

    def from_short_lines_text(self, text: str):
        """
        Famous example from Hávamál 77
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj = Ljoodhhaattr()
        >>> lj.from_short_lines_text(text)
        >>> lj.short_lines
        ['Deyr fé,', 'deyja frændr,', 'deyr sjalfr it sama,', 'ek veit einn,', 'at aldrei deyr:', 'dómr um dauðan hvern.']
        >>> lj.long_lines
        [['Deyr fé,', 'deyja frændr,'], ['deyr sjalfr it sama,'], ['ek veit einn,', 'at aldrei deyr:'], ['dómr um dauðan hvern.']]

        :param text:
        :return:
        """
        self.text = text
        self.short_lines = [line for line in text.split("\n") if line != ""]
        self.long_lines = [self.short_lines[0:2], [self.short_lines[2]], self.short_lines[3:5], [self.short_lines[5]]]

    def syllabify(self):
        """
        >>> lj = Ljoodhhaattr()
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."

        >>> lj.from_short_lines_text(text)
        >>> lj.syllabify()
        >>> lj.syllabified_text
        [[[[['deyr'], ['fé']]], [[['deyj', 'a'], ['frændr']]]], [[[['deyr'], ['sjalfr'], ['it'], ['sam', 'a']]]], [[[['ek'], ['veit'], ['einn']]], [[['at'], ['al', 'drei'], ['deyr']]]], [[[['dómr'], ['um'], ['dau', 'ðan'], ['hvern']]]]]


        :return:
        """
        Verse.syllabify(self)

    def to_phonetics(self):
        """
        >>> lj = Ljoodhhaattr()
        >>> text = "Deyr fé,\\ndeyja frændr,\\ndeyr sjalfr it sama,\\nek veit einn,\\nat aldrei deyr:\\ndómr um dauðan hvern."
        >>> lj.from_short_lines_text(text)
        >>> lj.to_phonetics()
        >>> lj.transcribed_text
        [['[dɐyr feː]', '[dɐyja frɛːndr]'], ['[dɐyr sjalvr it sama]'], ['[ɛk vɛit ɛinː]', '[at aldrɛi dɐyr]'], ['[doːmr um dɒuðan hvɛrn]']]

        """
        Verse.to_phonetics(self)

