Classical Latin
************************


Usage
===================
Filter Stopwords::

   import nltk.tokenize
   from cltk.stop.classical_latin.stops import STOPS_LIST

   SENTENCE = 'Quo usque tandem abutere, Catilina, patientia nostra?'
   lowered = SENTENCE.lower()
   tokens = nltk.word_tokenize(lowered)
   filtered = [w for w in tokens if not w in STOPS_LIST]
   
   print(filtered)
   
Convert J to I, V to U::

   from cltk.stem.classical_latin.j_and_v_converter import JVReplacer

   j = JVReplacer()
   replaced = j.replace('vem jam')

   print(replaced)

Compile PHI5::

   from cltk.corpus.common.compiler import Compile

   c = Compile('/home/kyle/Downloads/project_dir/corps', '/home/kyle/Downloads/project_dir')
   c.dump_txts_phi5()

The PHI7 may be compiled with ``c.dump_txts_phi7()``.


.. H3 -- Subsection
   ----------------

.. H4 -- Subsubsection
   +++++++++++++++++++
