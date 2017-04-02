Coptic
******
Coptic or Coptic Egyptian is the latest stage of the Egyptian language, a northern Afroasiatic language spoken in Egypt until at least the 17th century. Egyptian began to be written in the Coptic alphabet, an adaptation of the Greek alphabet with the addition of six or seven signs from demotic to represent Egyptian sounds the Greek language did not have, in the first century AD. Coptic flourished as a literary language from the second to thirteenth centuries, and its Bohairic dialect continues to be the liturgical language of the Coptic Orthodox Church of Alexandria. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Coptic_language>`_)

Coptic is the latest stage of the Egyptian language, a northern Afroasiatic language spoken in Egypt until at least the 17th century. Coptic flourished as a literary language from the second to thirteenth centuries, and its Bohairic dialect continues to be the liturgical language of the Coptic Orthodox Church of Alexandria. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Coptic_language>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``coptic_``) to discover available Coptic corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('coptic')

   In [3]: c.list_corpora
   Out[3]: ['coptic_text_scriptorium']
