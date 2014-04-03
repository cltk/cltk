Classical Latin
************************


Text Processing
===============

Filter Stopwords
----------------

::

   import nltk.tokenize
   from cltk.stop.classical_latin.stops import STOPS_LIST

   SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'
   lowered = SENTENCE.lower()
   tokens = nltk.word_tokenize(lowered)
   filtered = [w for w in tokens if not w in STOPS_LIST]
   
   print(filtered)
   
Convert J to I, V to U
----------------------

::

   from cltk.stem.classical_latin.j_and_v_converter import JVReplacer

   j = JVReplacer()
   replaced = j.replace('vem jam')

   print(replaced)
