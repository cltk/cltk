"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.

#TODO: Add TLG & PHI text cleaners from KJ's IPython notebooks
#TODO: Add non-ascii stripper
#TODO: Add generic HTML stripper
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>', ]
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.greek.tlgu import tlgu
