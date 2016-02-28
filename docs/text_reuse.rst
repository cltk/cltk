Text Reuse
*****
The text reuse module offers few tools to get started with studying text reuse between documents in the CLTK corpora.

The major goals of this module are to leverage conventional text reuse strategies and libraries to create comparison methods designed specifically for the languages of the corpora included in the CLTK.

This module is under active development, so if you experience a bug or have a suggestion for something to include, please create an issue on Github.

Levenshtein distance calculation
=========================

The Levenshtein distance comparison is a commonly-used method for fuzzy string comparison.  The CLTK Levenshtein class offers a few helps for getting started with creating comparisons from documents in the CLTK corpora.

This simple example compares a line from Vergil's Georgics with a line from Propertius (Elegies III.13.41):

.. code-block:: python

   In [1]: from cltk.reuse.levenshtein import Levenshtein

   In [2]: l = Levenshtein()

   In [3]: l.ratio("dique deaeque omnes, studium quibus arua tueri,", "dique deaeque omnes, quibus est tutela per agros,")
   Out[3]: 0.71
