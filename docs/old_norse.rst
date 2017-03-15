Old Norse
*********

Old Norse was a North Germanic language that was spoken by inhabitants of Scandinavia and inhabitants of their overseas settlements during about the 9th to 13th centuries. The Proto-Norse language developed into Old Norse by the 8th century, and Old Norse began to develop into the modern North Germanic languages in the mid- to late 14th century, ending the language phase known as Old Norse. These dates, however, are not absolute, since written Old Norse is found well into the 15th century. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Norse>`_)

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``old_norse_``) to discover available Old_norse corpora.

.. code-block:: python
   In [1]: from cltk.corpus.utils.importer import CorpusImporter as ci

   In [2]: i=ci("old_norse")

   In [3]: i.list_corpora
   Out[3]: ['old_norse_text_perseus']
