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

Compile Author-Works Indices
----------------------------

.. important::

   A version of the auth_work.txt files come with the CLTK, though it might not catch every title within every file. This is due to some inconsistent markup within the original corpora. There remains to be written and tested additional regular expressions to catch all titles.

After the PHI5 corpus has been compiled by the CLTK, it can generate indices for the works contained within each author file. Essentially, it looks in each author's file (e.g., ``LAT0660.txt``) and scans its contents looking for title tags (i.e., ``{1Comment. in Vergilium}1``).

After the CLTK generates an author-work index, a file called ``auth_work.txt`` will be added to the phi_5 directory (i.e., ``cltk/corpus/classical_latin/plaintext/phi_5/auth_work.txt``). To generate::

   from cltk.corpus.common.compiler import Compile

   c = Compile('/home/kyle/Downloads/project_dir/corps', '/home/kyle/cltk/cltk/corpus')

   c.write_phi5_auth_works()
