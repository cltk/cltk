""" Params: Middle English
"""

__author__ = ['Clément Besnier <clemsciences@gmail.com>',
              'Patrick J. Burns <patrick@diyclassics.org']
__license__ = 'MIT License.'

MiddleEnglishTokenizerPatterns = [(r'\n', r' '),
                                  (r'(?<=.)(?=[\.\";\,\:\[\]\(\)!&?])', r' '),
                                  (r'(?<=[\.\";\,\:\[\]\(\)!&?])(?=.)', r' '), 
                                  (r'\s+', r' ')
                                 ]
