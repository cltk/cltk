Malayalam
*********

Malayalam is a language spoken in India, predominantly in the state of Kerala. Malayalam originated from Middle Tamil (Sen-Tamil) in the 7th century. An alternative theory proposes a split in even more ancient times.Malayalam incorporated many elements from Sanskrit through the ages. Many medieval liturgical texts were written in an admixture of Sanskrit and early Malayalam, called Manipravalam.The oldest literary work in Malayalam, distinct from the Tamil tradition, is dated from between the 9th and 11th centuries. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Malayalam>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``malayalam_``) to discover available Malayalam corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('malayalam')

   In [3]: c.list_corpora
   Out[3]:
   ['malayalam_text_gretil']
