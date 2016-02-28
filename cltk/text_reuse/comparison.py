
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
        # e.g. 10 (for line 10) or 3 (for paragraph 3)
        self.author_a = ""
        self.author_b = ""

        # The works related to the compared string values
        # e.g. 10 (for line 10) or 3 (for paragraph 3)
        self.work_a = ""
        self.work_b = ""

        # The subworks related to the compared string values
        # e.g. 10 (for line 10) or 3 (for paragraph 3)
        self.subwork_a = ""
        self.subwork_b = ""

        # The text numbers related to the compared string values
        # e.g. 10 (for line 10) or 3 (for paragraph 3)
        self.text_n_a = None
        self.text_n_b = None

        return

    def set_ref_a(author, work, subwork, text_n):
        """
        Set the reference values related to the str_a compared string
        :param author: str
        :param work: str
        :param subwork: str
        :param text_n: str (a string instead of integer for variations in numbering systems that may inlude integers and alpha characters (e.g. '101b'))
        :return: void
        """
        self.author_a = author
        self.work_a = work
        self.subwork_a = subwork
        self.text_n_a = text_n

        return

    def set_ref_b(author, work, subwork, text_n):
        """
        Set the reference values related to the str_b compared string
        :param author: str
        :param work: str
        :param subwork: str
        :param text_n: str (a string instead of integer for variations in numbering systems that may inlude integers and alpha characters (e.g. '101b'))
        :return: void
        """
        self.author_b = author
        self.work_b = work
        self.subwork_b = subwork
        self.text_n_b = text_n

        return
