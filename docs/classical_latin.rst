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

In order for the CLTK to work with the PHI5, its files first need to be translated from its legacy encoding into Unicode. For the arguments to ``Compile``, the first is the path to the directory just below where your PHI5 corpus is found, and the second is the path to the corpus directory of your CLTK project. For example, on a POSIX system, if one's home directory is ``/home/kyle``, and the CLTK project is installed at ``/home/kyle/cltk``, then the CLTK corpus directory would reside at ``/home/kyle/cltk/cltk/corpus``::

   from cltk.corpus.common.compiler import Compile

   c = Compile('/home/kyle/Downloads/project_dir/corps', '/home/kyle/cltk/cltk/corpus')

   c.dump_txts_phi5_files()

A few things to note: Your PHI5 directory must be named ``PHI5`` and the PHI5's file names must be all uppercase (e.g., ``LAT0660.TXT``).

The CLTK compiler can also output the entirety of the PHI5 into a single JSON object. Outputting this into one file (with ``c.dump_txts_phi5()``) is probably inadvisable, since it would be too large for efficient reading, but this code would only need a little modification to insert into a `document-oriented database <http://en.wikipedia.org/wiki/Document-oriented_database>`_ (such as MongoDB).

Compile Author-Works Indices
----------------------------

After the PHI5 corpus has been compiled by the CLTK, it can generate indices for the works contained within each author file. Essentially, it looks in each author's file (e.g., ``LAT0660.txt``) and scans its contents looking for title tags (i.e., ``{1Comment. in Vergilium}1``).

After the CLTK generates an author-work index, a file called ``auth_work.txt`` will be added to the phi_5 directory (i.e., ``cltk/corpus/classical_latin/plaintext/phi_5/auth_work.txt``). To generate::

   from cltk.corpus.common.compiler import Compile

   c = Compile('/home/kyle/Downloads/project_dir/corps', '/home/kyle/cltk/cltk/corpus')

   c.write_phi5_auth_works()

.. important::

   A version of the auth_work.txt files come with the CLTK, though it might not catch every title within every file. This is due to some inconsistent markup within the original corpora. There remains to be written and tested additional regular expressions to catch all titles.
