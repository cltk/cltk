"""Configuration class for specifying scansion constants."""

__author__ = ["Todd Cook <todd.g.cook@gmail.com>"]
__license__ = "MIT License"


class ScansionConstants:
    """
    Constants containing strings have characters in upper and lower case since they will
    often be used in regular expressions, and used to preserve/a verse's original case.

    This class also allows users to customizing scansion constants and scanner behavior.

    >>> constants = ScansionConstants(unstressed="U",stressed= "-", optional_terminal_ending="X")
    >>> print(constants.DACTYL)
    -UU

    >>> smaller_constants = ScansionConstants(
    ... unstressed="˘",stressed= "¯", optional_terminal_ending="x")
    >>> print(smaller_constants.DACTYL)
    ¯˘˘
    """

    # pylint: disable=invalid-name
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods

    def __init__(
        self, unstressed="U", stressed="-", optional_terminal_ending="X", separator="|"
    ):
        self.UNSTRESSED = unstressed
        self.STRESSED = stressed
        self.OPTIONAL_ENDING = optional_terminal_ending
        self.FOOT_SEPARATOR = separator
        self.IAMB = unstressed + stressed
        self.TROCHEE = stressed + unstressed
        self.SPONDEE = stressed + stressed
        self.ANAPEST = unstressed + unstressed + stressed
        self.DACTYL = stressed + unstressed + unstressed
        self.AMPHIBRACH = unstressed + stressed + unstressed
        self.PYRRHIC = unstressed + unstressed
        self.HEXAMETER_ENDING = stressed + optional_terminal_ending
        """The following two constants are not offical scansion terms, but invalid in hexameters"""
        self.INVERTED_AMPHIBRACH = stressed + unstressed + stressed
        self.INVALID_HEXAMETER_COMBO = stressed + stressed + unstressed
        self.CONSONANTS = "bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ"
        self.CONSONANTS_WO_H = "bcdfgjklmnpqrstvwxzBCDFGJKLMNPQRSTVWXZ"

        # Vowels and accented vowels should be kept the same length & position for easy dict map
        self.VOWELS = "aeiouyAEIOUYäÄëËïÏöÖüÜÿŸ"
        self.ACCENTED_VOWELS = "āēīōūȳĀĒĪŌŪȲäÄëËïÏöÖüÜÿŸ"
        self.VOWELS_WO_I = "aeouAEOUYāēōūȳĀĒŌŪȲäÄëËöÖüÜÿŸ"
        self.VOWELS_TO_ACCENTS = dict(
            zip(list(self.VOWELS), list(self.ACCENTED_VOWELS))
        )
        self.ACCENTS_TO_VOWELS = dict(
            zip(list(self.ACCENTED_VOWELS), list(self.VOWELS))
        )

        self.DIPTHONGS = [
            "ae",
            "au",
            "ei",
            "eu",
            "oe",
            "ui",
            "Ui",
            "uī",
            # because the last vowel can be accented by position: potuisse
            "Ae",
            "Au",
            "Ei",
            "Eu",
            "Oe",
        ]
        self.UI_EXCEPTIONS = {
            "cui": ["cui"],
            "Cui": ["Cui"],
            "hui": ["hui"],
            "Hui": ["Hui"],
            "huic": ["huic"],
            "Huic": ["Huic"],
        }
        self.stress_accent_dict = dict(
            zip(
                list(self.VOWELS + self.ACCENTED_VOWELS),
                list(self.ACCENTED_VOWELS + self.ACCENTED_VOWELS),
            )
        )
        self.LIQUIDS = "lmnrLMNR"
        self.MUTES = "bcdfgptBCDFGPT"
        self.DOUBLED_CONSONANTS = [letter + letter for letter in self.CONSONANTS]
        """Prefix order not arbitrary; one will want to match on extra before ex"""
        self.PREFIXES = [
            "contrā",
            "contra",
            "subter",
            "circum",
            "trans",
            "extro",
            "suprā",
            "extrā",
            "ultra",
            "iuxta",
            "super",
            "supra",
            "intro",
            "inter",
            "ultrā",
            "extra",
            "retrō",
            "intrō",
            "retro",
            "trāns",
            "quasi",
            "īnfrā",
            "juxtā",
            "infra",
            "ante",
            "ambi",
            "tran",
            "dein",
            "prae",
            "post",
            "sine",
            "sed",
            "pre",
            "sin",
            "per",
            "pro",
            "abs",
            "sub",
            "dis",
            "dīs",
            "con",
            "dif",
            "non",
            "sīn",
            "prō",
            "com",
            "tra",
            "red",
            "sur",
            "nōn",
            "ob",
            "ēr",
            "de",
            "ex",
            "dī",
            "ēf",
            "ad",
            "ne",
            "ac",
            "in",
            "rē",
            "nē",
            "āb",
            "ef",
            "ēx",
            "di",
            "se",
            "īn",
            "en",
            "co",
            "ab",
            "er",
            "dē",
            "re",
            "ēn",
            "ōb",
            "sē",
        ]

        self.ASPIRATES = ["pt", "Pt", "ch", "th", "Ch", "Th"]
        self.NOTE_MAP: dict = dict(
            (
                ("positionally", "Valid by positional stresses."),
                ("inverted", "Inverted amphibrachs corrected."),
                ("invalid start", "Corrected invalid start."),
                ("invalid 5th", "Corrected invalid fifth foot."),
                ("invalid foot", "invalid foot converted to spondee."),
                ("invalid syllables", "invalid syllables; corrupt text?"),
                ("optional i to j", "Transformed i to j aggressively."),
                ("17", "All dactyls according to syllable count."),
                ("12", "All spondees according to syllable count."),
                ("< 12", "Incomplete hexameter; not enough syllables."),
                ("5th dactyl", "13 syllables; probable dactyl at 5th foot."),
                ("> 17", "Invalid hexameter; too many syllables."),
                ("closest match", "Scansion matched to closest valid pattern."),
                ("dactyl smoothing", "Dactyl chain smoothing."),
                ("antepenult chain", "antepenult foot onward normalized."),
                ("penultimate dactyl chain", "penultimate foot onward normalized."),
                (
                    "> 11",
                    "Invalid hendecasyllables; more than eleven syllables detected",
                ),
                (
                    "< 11",
                    "Invalid hendecasyllables; less than eleven syllables detected",
                ),
                ("< 12p", "Invalid pentameter; too few syllables"),
                ("12p", "Spondaic pentameter"),
                ("14p", "Dactylic pentameter"),
                ("> 14", "Invalid pentameter; too many syllables"),
            )
        )
