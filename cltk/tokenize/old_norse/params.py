""" Params: Old Norse
"""

__author__ = ['Clément Besnier <clemsciences@aol.com>',
              'Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

# As far as I know, hyphens were never used for compounds, so the tokenizer treats all hyphens as line-breaks
OldNorseTokenizerPatterns = [(r"\'", r"' "),
                             (r"(?<=.)(?=[.!?)(\";:,«»\-])", " ")
                            ]
