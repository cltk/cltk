""" Params: Middle High German
"""

__author__ = ['Clément Besnier <clemsciences@gmail.com>',
              'Patrick J. Burns <patrick@diyclassics.org']
__license__ = 'MIT License.'

# As far as I know, hyphens were never used for compounds, so the tokenizer treats all hyphens as line-breaks
MiddleHighGermanTokenizerPatterns = [(r'-\n',r'-'),
                                     (r'\n', r' '),
                                     (r'(?<=.)(?=[\.\";\,\:\[\]\(\)!&?])', r' '),
                                     (r'(?<=[\.\";\,\:\[\]\(\)!&?])(?=.)', r' '),
                                     (r'\s+', r' ')
                                    ]
