Classical Latin
************************


Use
===================

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

Compile PHI5
------------
The PHI5 can be compiled into one big JSON file or into individual plaintext files, much as they originally came on the disk. For the call to ``Compile``, the first argument is to the directory just below where your PHI5 corpus is found, and the second is the path to the corpus directory of your cltk project::

   from cltk.corpus.common.compiler import Compile

   c = Compile('/home/kyle/Downloads/project_dir/corps', '/home/kyle/cltk/cltk/corpus')

To make into one file, the run::

   c.dump_txts_phi5()

or into multiple files::

   c.dump_txts_phi5_files()

The PHI7 may also be generated in the same way, only with ``c.dump_txts_phi7()`` or ``c.dump_txts_phi7_files()``. Note that the CLTK by default puts all PHI7 files into the classical_greek directory.

.. H3 -- Subsection
   ----------------

.. H4 -- Subsubsection
   +++++++++++++++++++
