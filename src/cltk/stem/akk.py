"""Stemmer for Akkadian.

Get the stem of a word, given a declined form and its gender.
"""

__author__ = ["M. Willis Monroe <willismonroe@gmail.com>"]
__license__ = "MIT License. See LICENSE."

ENDINGS = {
    "m": {
        "singular": {"nominative": "um", "accusative": "am", "genitive": "im"},
        "dual": {"nominative": "ān", "oblique": "īn"},
        "plural": {"nominative": "ū", "oblique": "ī"},
    },
    "f": {
        "singular": {"nominative": "tum", "accusative": "tam", "genitive": "tim"},
        "dual": {"nominative": "tān", "oblique": "tīn"},
        "plural": {
            "nominative": ["ātum", "ētum", "ītum"],
            "oblique": ["ātim", "ētim", "ītum"],
        },
    },
}


class AkkadianStemmer:
    """Stem Akkadian words with a simple algorithm based on Huehnergard"""

    def get_stem(self, noun: str, gender: str, mimation: bool =True) -> str:
        """Return the stem of a noun, given its gender"""
        stem = ""

        if mimation and noun[-1:] == "m":
            # noun = noun[:-1]
            # TODO what should we do here?
            pass
        
        # Take off ending
        if gender == "m":
            if noun[-2:] in list(self.endings["m"]["singular"].values()) + list(
                self.endings["m"]["dual"].values()
            ):
                stem = noun[:-2]
            elif noun[-1] in list(self.endings["m"]["plural"].values()):
                stem = noun[:-1]
            else:
            	# we don't recognize the ending, so return the noun.
               	stem = noun
        elif gender == "f":
            if (
                noun[-4:]
                in self.endings["f"]["plural"]["nominative"]
                + self.endings["f"]["plural"]["oblique"]
            ):
                stem = noun[:-4] + "t"
            elif noun[-3:] in list(self.endings["f"]["singular"].values()) + list(
                self.endings["f"]["dual"].values()
            ):
                stem = noun[:-3] + "t"
            elif noun[-2:] in list(self.endings["m"]["singular"].values()) + list(
                self.endings["m"]["dual"].values()
            ):
                stem = noun[:-2]
            else:
                # we don't recognize the ending, so return the noun.
                stem = noun
        else:
            stem = noun
        return stem


