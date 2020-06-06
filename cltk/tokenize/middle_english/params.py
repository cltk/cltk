""" Params: Middle English
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>', ]
__license__ = 'MIT License.'

MiddleEnglishTokenizerPatterns = [(r'-', r' - '),
                                  (r'\n', r' '),
                                  (r'(?<=.)(?=[\.\";\,\:\[\]\(\)!&?])', r' '),
                                  (r'(?<=[\.\";\,\:\[\]\(\)!&?])(?=.)', r' '),
                                  (r'\s+', r' ')
                                  ]
