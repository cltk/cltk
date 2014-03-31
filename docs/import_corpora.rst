Import Corpora
**************


PHI 5
=====

Import PHI 5
------------

If the PHI 5 files were located at ``/Users/kyle/Downloads/corpora/PHI5/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpora('phi5', '/Users/kyle/Downloads/corpora/PHI5/')


PHI 7
=====

Import PHI 7
------------

If the PHI 7 files were located at ``/Users/kyle/Downloads/corpora/PHI7/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpora('phi7', '/Users/kyle/Downloads/corpora/PHI7/')


Compile into Unicode
--------------------

.. note::

   The PHI7 is compiled but its Beta Code is not currently converted into Unicode. For this to be done, a little parser for Greek markup needs to be written.

The PHI7 may also be generated in a way similar to the TLG, only with ``c.dump_txts_phi7_files()`` (or ``c.dump_txts_phi7()``).:

.. code-block:: python

   from cltk.corpus.common.compiler import Compile
   c = Compile()
   c.dump_txts_phi7_files()
   


Rebuild Indices
---------------

The CLTK comes with pre-compiled author-file and author-work indices for the PHI7 (```` and ``auth_work.txt``, respectively). They can be found at ``cltk/corpus/classical_greek/plaintext/phi_7/``. The former is a dictionary listing of PHI_7 file names and abbreviated author names (e.g, ``'DDP0128': 'PRyl'``). The latter, ``auth_work.txt``, is a large dictionary containing metadata about authors and their writings (at ``cltk/corpus/classical_greek/plaintext/phi_7/auth_work.txt``).

To re-compile these yourself, the following two methods may be used. To create ``authtab.txt``:

.. code-block:: python

   from cltk.corpus.common.compiler import Compile
   c = Compile()
   c.make_phi7_authtab()

And to re-compile ``auth_work.txt``, do:

.. code-block:: python

   from cltk.corpus.common.compiler import Compile
   c = Compile()
   c.write_phi7_auth_works()


TLG
===

Import
------

The CLTK works soley out of the locally directory ``cltk_local``, which is created at a user's root directory. Within this are two directories, ``originals``, in which copies of outside corpora are made, and ``compiled``, in which transformed copies of the former are written.

The first step is to copy outside files into the ``originals`` directory. If the TLG files were located at ``/Users/kyle/Downloads/corpora/TLG_E/``, then the commands would be:

.. code-block:: python

   In [1]: from cltk.corpus.common.compiler import Compile
   In [2]: c = Compile()
   In [3]: c.import_corpora('tlg', '/Users/kyle/Downloads/corpora/TLG_E/')
 
Compile into Unicode
--------------------
 
Currently, the following commands all need to be run in the root of the CLTK repository. These commands need to be run as follow:

.. code-block:: python

   from cltk.corpus.common.compiler import Compile
   c = Compile()
   c.make_tlg_file_author()

In order for the CLTK to work with the TLG, its files first need to be translated from its legacy encoding into Unicode::

   convert_tlg_txt(): Reads original Beta Code files and converts to Unicode files.

This will take some time (approx. 10-20 minutes). When it is finished, you may find the .txt files in, from root, ``/cltk/corpus/classical_greek/plaintext/tlg_e/``).

A few things to note: Your TLG directory must be named ``TLG_E`` and the TLG's file names must be all uppercase (e.g., ``TLG0020.TXT``).

Rebuild Indices
---------------

You shouldn't have to do this, as the CLTK comes with these already, but the following are the methods by which the indices were build:

``make_tlg_index_file_author()``: Reads TLG's AUTHTAB.DIR and writes a dict (index_file_author.txt) to the CLTK's corpus directory. ``cltk/corpus/classical_greek/plaintext/tlg_e/index_file_author.txt``

``write_tlg_index_auth_works()``: Reads index_file_author.txt, read author file, and expand dict to include author works, index_author_works.txt. ``cltk/corpus/classical_greek/plaintext/tlg_e/index_author_works.txt``

``write_tlg_meta_index()``: Reads and writes the LSTSCDCN.DIR file. ``cltk/corpus/classical_greek/plaintext/tlg_e/meta_list.txt``

``read_tlg_author_work_titles()``: Reads a converted TLG file and returns a list of header titles within it.

.. note::

   The TLG and PHI7 both come with index files (e.g., ``BIBINDCD.BIN``, ``LIST4CLA.BIN``), though these have proven challenging to parse.
