
"""
A comparison class to help with tracking string comparison values
"""

from cltk.utils.cltk_logger import logger


__author__ = 'Luke Hollis <lukehollis@gmail.com>'
__license__ = 'MIT License. See LICENSE.'


class Comparison:
    """A class to increase ease of working with text reuse data."""


    def __init__(self, str_a, str_b, distance_ratio):
        """Initialize class object with necessary values"""

        self.str_a = str_a
        self.str_b = str_b
        self.ratio = distance_ratio

        return
