Hebrew
******

Hebrew is a language native to Israel, spoken by over 9 million people worldwide, of whom over 5 million are in Israel. Historically, it is regarded as the language of the Israelites and their ancestors, although the language was not referred to by the name Hebrew in the Tanakh. The earliest examples of written Paleo-Hebrew date from the 10th century BCE. Hebrew belongs to the West Semitic branch of the Afroasiatic language family. The Hebrew language is the only living Canaanite language left. Hebrew had ceased to be an everyday spoken language somewhere between 200 and 400 CE, declining since the aftermath of the Bar Kokhba revolt. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Hebrew_language>`_)


Corpora
=======

Use ``CorpusImporter`` or browse the `CLTK Github repository <http://github.com/cltk>`_ (anything beginning with ``hebrew_``) to discover available Hebrew corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter
   In [2]: corpus_importer = CorpusImporter('hebrew')
   In [3]: corpus_importer.list_corpora
   Out[3]:
   ['hebrew_text_sefaria']

