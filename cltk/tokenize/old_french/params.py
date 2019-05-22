""" Params: Old French
"""

__author__ = ['Natasha Voake <natashavoake@gmail.com>',
              'Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

OldFrenchTokenizerPatterns = [(r"’", r"'"),
                              (r"\'", r"' "),
                              (r"(?<=.)(?=[.!?)(\";:,«»\-])", " ")
                             ]
