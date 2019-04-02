Middle Low German
*****************
Middle Low German or Middle Saxon is a language that is the descendant of Old Saxon and the ancestor of modern Low German. It served as the international lingua franca of the Hanseatic League. It was spoken from about 1100 to 1600, or 1200 to 1650.
(Source: `Wikipedia <https://en.wikipedia.org/wiki/Middle_Low_German>`_)

POS Tagging
===========

The POS taggers were trained by NLTK's models on the `ReN <https://corpora.uni-hamburg.de/hzsk/de/islandora/object/text-corpus:ren-0.6>`_ training set.

1–2–gram backoff tagger
-----------------------

.. code-block:: python

  In [1]: from cltk.tag.pos import POSTag

  In [2]: tagger = POSTag('middle_low_german')

  In [3]: tagger.tag_ngram_12_backoff('Jck  Johannes  Veghe  preister  verwarer  vnde  voirs tender  des  Juncfrouwen  kloisters  to Mariendale')
  Out[3]: [('Jck', 'PPER'),
         ('Johannes', 'NE'),
         ('Veghe', 'NE'),
         ('preister', 'NA'),
         ('verwarer', 'NA'),
         ('vnde', 'KON'),
         ('voirs', 'NA'),
         ('tender', 'NA'),
         ('des', 'DDARTA'),
         ('Juncfrouwen', 'NA'),
         ('kloisters', 'NA'),
         ('to', 'APPR'),
         ('Mariendale', 'NE')]
