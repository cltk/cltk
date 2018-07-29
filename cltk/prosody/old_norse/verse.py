

from math import floor

__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


class VerseManager:
    """

    """
    def is_fornyrdhislag(self, text):
        """
        Basic check
        :param text:
        :return:
        """
        l = [line for line in text.split("\n") if line != ""]
        return len(l) == 8

    def is_ljoodhhaattr(self, text):
        l = [line for line in text.split("\n") if line != ""]
        return len(l) == 6


class Fornyrdhislag:
    def __init__(self):
        self.text = ""
        self.long_lines = []
        self.short_lines = []

    def from_short_lines_text(self, text: str):
        """
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


class Ljoodhhaatr:
    def __init__(self):
        self.text = ""
        self.long_lines = []
        self.short_lines = []

    def from_short_lines_text(self, text: str):
        """


        :param text:
        :return:
        """
        self.text = text
        self.short_lines = [line for line in text.split("\n") if line != ""]
        self.long_lines = [self.short_lines[2 * i:2 * i + 2] if i % 3 != 2 else self.short_lines[2 * i]
                           for i in range(int(floor(len(self.short_lines) / 2)))]
