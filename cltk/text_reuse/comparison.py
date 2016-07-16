
"""
A comparison class to help with tracking string comparison values
"""

from cltk.utils.cltk_logger import logger


__author__ = 'Luke Hollis <lukehollis@gmail.com>'
__license__ = 'MIT License. See LICENSE.'


class Comparison:
    """A class to increase ease of working with text reuse data."""


    def __init__(self, str_a, str_b, distance_ratio):
        """
        Initialize class with compared strings and ratio of comparison
        :param str_a: str
        :param str_b: str
        :param distance_ratio: float

        """

        self.str_a = str_a
        self.str_b = str_b
        self.ratio = distance_ratio

        # The authors related to the compared string values
        self.author_a = None
        self.author_b = None

        # The works related to the compared string values
        self.work_a = None
        self.work_b = None

        # The subworks related to the compared string values
        self.subwork_a = None
        self.subwork_b = None

        # The text numbers related to the compared string values
        # e.g. 10 (for line 10) or 3 (for paragraph 3)
        self.text_n_a = None
        self.text_n_b = None

        # Languages of strings being compared
        self.language_a = None
        self.language_b = None

        return

    def set_ref_a(self, text_ref):
        """
        Set the reference values related to the str_a compared string
        :param text_info: dict
                    -- author: str
                    -- work: str
                    -- subwork: str
                    -- text_n: str (a string instead of integer for variations in numbering systems that may inlude integers and alpha characters (e.g. '101b'))
        :return: void
        """

        if 'author' in text_ref:
            self.author_a = text_ref['author']
        if 'work' in text_ref:
            self.work_a = text_ref['work']
        if 'subwork' in text_ref:
            self.subwork_a = text_ref['subwork']
        if 'text_n' in text_ref:
            self.text_n_a = text_ref['text_n']
        if 'language' in text_ref:
            self.language_a = text_ref['language']

        return

    def set_ref_b(self, text_ref):
        """
        Set the reference values related to the str_b compared string
        :param text_info: dict
                    -- author: str
                    -- work: str
                    -- subwork: str
                    -- text_n: str (a string instead of integer for variations in numbering systems that may inlude integers and alpha characters (e.g. '101b'))
        :return: void
        """

        if 'author' in text_ref:
            self.author_b = text_ref['author']
        if 'work' in text_ref:
            self.work_b = text_ref['work']
        if 'subwork' in text_ref:
            self.subwork_b = text_ref['subwork']
        if 'text_n' in text_ref:
            self.text_n_b = text_ref['text_n']
        if 'language' in text_ref:
            self.language_b = text_ref['language']

        return
