"""Old Norse runes, Unicode block: 16A0–16FF.
Source: *Viking Language 1*, Jessie L. Byock

TODO: Document and test better.
"""

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]

from enum import Enum, auto

POINT = "᛫"
SEMI_COLUMN = "\u16EC"


class AutoName(Enum):
    def _generate_next_value_(name, a, b, d):
        return name


class RunicAlphabetName(AutoName):
    elder_futhark = auto()
    younger_futhark = auto()
    short_twig_younger_futhark = auto()


class Rune:
    """
    >>> Rune(RunicAlphabetName.elder_futhark, "\u16BA", "h", "h", "haglaz")
    ᚺ
    >>> Rune.display_runes(ELDER_FUTHARK)
    ['ᚠ', 'ᚢ', 'ᚦ', 'ᚨ', 'ᚱ', 'ᚲ', 'ᚷ', 'ᚹ', 'ᚺ', 'ᚾ', 'ᛁ', 'ᛃ', 'ᛇ', 'ᛈ', 'ᛉ', 'ᛊ', 'ᛏ', 'ᛒ', 'ᛖ', 'ᛗ', 'ᛚ', 'ᛜ', 'ᛟ', 'ᛞ']
    """

    def __init__(
        self,
        runic_alphabet: RunicAlphabetName,
        form: str,
        sound: str,
        transcription: str,
        name: str,
    ):
        """

        :param runic_alphabet: RunicAlphabetName
        :param form: str
        :param sound: str
        :param transcription: str
        :param name: str
        """
        self.runic_alphabet = runic_alphabet
        self.form = form
        self.sound = sound
        self.transcription = transcription
        self.name = name

    @staticmethod
    def display_runes(runic_alphabet: list):
        """
        Displays the given runic alphabet.
        :param runic_alphabet: list
        :return: list
        """
        return [rune.form for rune in runic_alphabet]

    @staticmethod
    def from_form_to_transcription(form: str, runic_alphabet: list):
        """

        :param form:
        :param runic_alphabet:
        :return: conventional transcription of the rune
        """
        d_form_transcription = {
            rune.form: rune.transcription for rune in runic_alphabet
        }
        return d_form_transcription[form]

    def __repr__(self):
        return self.form

    def __str__(self):
        return self.form

    def __eq__(self, other):
        return self.form == other


class Transcriber:
    """
    >>> little_jelling_stone = "᛬ᚴᚢᚱᛘᛦ᛬ᚴᚢᚾᚢᚴᛦ᛬ᚴ(ᛅᚱ)ᚦᛁ᛬ᚴᚢᛒᛚ᛬ᚦᚢᛋᛁ᛬ᛅ(ᚠᛏ)᛬ᚦᚢᚱᚢᛁ᛬ᚴᚢᚾᚢ᛬ᛋᛁᚾᛅ᛬ᛏᛅᚾᛘᛅᚱᚴᛅᛦ᛬ᛒᚢᛏ᛬"
    >>> Transcriber.transcribe(little_jelling_stone, YOUNGER_FUTHARK)
    '᛫kurmR᛫kunukR᛫k(ar)þi᛫kubl᛫þusi᛫a(ft)᛫þurui᛫kunu᛫sina᛫tanmarkaR᛫but᛫'
    """

    def __init__(self):
        pass

    @staticmethod
    def from_form_to_transcription(runic_alphabet: list):
        """
        Make a dictionary whose keys are forms of runes and values their transcriptions.
        Used by transcribe method.
        :param runic_alphabet:
        :return: dict
        """
        return {rune.form: rune.transcription for rune in runic_alphabet}

    @staticmethod
    def transcribe(rune_sentence: str, runic_alphabet: list):
        """
        From a runic inscription, the transcribe method gives a conventional transcription.
        :param rune_sentence: str, elements of this are from runic_alphabet or are punctuations
        :param runic_alphabet: list
        :return:
        """
        res = []
        d_form_transcription = Transcriber.from_form_to_transcription(runic_alphabet)
        for c in rune_sentence:
            if c in runic_alphabet:
                res.append(d_form_transcription[c])
            elif c in "()":
                res.append(c)
            else:
                res.append(POINT)
        return "".join(res)


# ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ ᛉ ᛊ ᛏ ᛒ ᛖ ᛗ ᛚ ᛜ ᛟ ᛞ
ELDER_FUTHARK = [
    Rune(RunicAlphabetName.elder_futhark, "\u16A0", "f", "f", "fehu"),
    Rune(RunicAlphabetName.elder_futhark, "\u16A2", "u", "u", "uruz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16A6", "θ", "þ", "þuriaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16A8", "a", "a", "ansuz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16B1", "r", "r", "raido"),
    Rune(RunicAlphabetName.elder_futhark, "\u16B2", "k", "k", "kaunan"),
    Rune(RunicAlphabetName.elder_futhark, "\u16B7", "g", "g", "gyfu"),
    Rune(RunicAlphabetName.elder_futhark, "\u16B9", "w", "w", "wynn"),
    Rune(RunicAlphabetName.elder_futhark, "\u16BA", "h", "h", "haglaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16BE", "n", "n", "naudiz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16C1", "i", "i", "isaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16C3", "j", "j", "jeran"),
    Rune(RunicAlphabetName.elder_futhark, "\u16C7", "æ", "E", "eiwaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16C8", "p", "p", "peorð"),
    Rune(RunicAlphabetName.elder_futhark, "\u16C9", "ʀ", "r", "algiz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16CA", "s", "s", "sowilo"),
    Rune(RunicAlphabetName.elder_futhark, "\u16CF", "t", "t", "tiwaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16D2", "b", "b", "berkanan"),
    Rune(RunicAlphabetName.elder_futhark, "\u16D6", "e", "e", "ehwaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16D7", "m", "m", "mannaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16DA", "l", "l", "laguz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16DC", "ŋ", "ng", "ingwaz"),
    Rune(RunicAlphabetName.elder_futhark, "\u16DF", "ø", "œ", "odal"),
    Rune(RunicAlphabetName.elder_futhark, "\u16DE", "d", "d", "dagaz"),
]

# ᚠ ᚢ ᚦ ᚭ ᚱ ᚴ ᚼ ᚾ ᛁ ᛅ ᛋ ᛏ ᛒ ᛖ ᛘ ᛚ ᛦ
YOUNGER_FUTHARK = [
    Rune(RunicAlphabetName.younger_futhark, "\u16A0", "f", "f", "fehu"),
    Rune(RunicAlphabetName.younger_futhark, "\u16A2", "u", "u", "uruz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16A6", "θ", "þ", "þuriaz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16AD", "a", "a", "ansuz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16B1", "r", "r", "raido"),
    Rune(RunicAlphabetName.younger_futhark, "\u16B4", "k", "k", "kaunan"),
    Rune(RunicAlphabetName.younger_futhark, "\u16BC", "h", "h", "haglaz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16BE", "n", "n", "naudiz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16C1", "i", "i", "isaz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16C5", "a", "a", "jeran"),
    Rune(RunicAlphabetName.younger_futhark, "\u16CB", "s", "s", "sowilo"),
    Rune(RunicAlphabetName.younger_futhark, "\u16CF", "t", "t", "tiwaz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16D2", "b", "b", "berkanan"),
    Rune(RunicAlphabetName.younger_futhark, "\u16D6", "e", "e", "ehwaz"),
    Rune(
        RunicAlphabetName.younger_futhark, "\u16D8", "m", "m", "mannaz"
    ),  # also \u16D9
    Rune(RunicAlphabetName.younger_futhark, "\u16DA", "l", "l", "laguz"),
    Rune(RunicAlphabetName.younger_futhark, "\u16E6", "r", "R", "algiz"),
]

# ᚠ ᚢ ᚦ ᚭ ᚱ ᚴ ᚽ ᚿ ᛁ ᛅ ᛌ ᛐ ᛓ ᛖ ᛙ ᛚ ᛧ
SHORT_TWIG_YOUNGER_FUTHARK = [
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16A0", "f", "f", "fehu"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16A2", "u", "u", "uruz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16A6", "θ", "þ", "þuriaz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16AD", "a", "a", "ansuz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16B1", "r", "r", "raido"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16B4", "k", "k", "kaunan"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16BD", "h", "h", "haglaz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16BF", "n", "n", "naudiz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16C1", "i", "i", "isaz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16C5", "a", "a", "jeran"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16CC", "s", "s", "sowilo"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16D0", "t", "t", "tiwaz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16D3", "b", "b", "berkanan"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16D6", "e", "e", "ehwaz"),
    Rune(
        RunicAlphabetName.short_twig_younger_futhark, "\u16D9", "m", "m", "mannaz"
    ),  # also \u16D9
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16DA", "l", "l", "laguz"),
    Rune(RunicAlphabetName.short_twig_younger_futhark, "\u16E7", "r", "R", "algiz"),
]
