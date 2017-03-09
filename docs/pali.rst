Pali
****
Pali (Pāli) is a Prakrit language native to the Indian subcontinent. It is widely studied because it is the language of much of the earliest extant literature of Buddhism as collected in the Pāli Canon or Tipiṭaka and is the sacred language of Theravāda Buddhism.
Source: `Wikipedia 
<https://en.wikipedia.org/wiki/Pali>`_.

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``pali_``) to discover available Pali corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('pali')

   In [3]: c.list_corpora
   Out[3]: ['pali_text_ptr_tipitaka']

