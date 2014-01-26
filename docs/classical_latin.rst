H1 -- Classical Latin
************************


H2 -- Functionality
===================
Filter Stopwords::

   import nltk.tokenize

   from cltk.stop.classical_latin.stops import STOPS_LIST

   SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'

   lowered = SENTENCE.lower()

   tokens = nltk.word_tokenize(lowered)

   filtered = [w for w in tokens if not w in STOPS_LIST]

   print(filtered)
   


.. H3 -- Subsection
   ----------------

.. H4 -- Subsubsection
   +++++++++++++++++++
