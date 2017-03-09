Telugu
********
Telugu (English pronunciation: /ˈtɛlᵿɡuː/telugu, IPA: [t̪el̪uɡu]) is a Dravidian language native to India. It stands alongside Hindi, English, and Bengali as one of the few languages with official status in more than one Indian state; it is the primary language in the states of Andhra Pradesh, Telangana, and in the town of Yanam, Puducherry. It is also spoken by significant minorities in the Andaman and Nicobar Islands, Chhattisgarh, Karnataka, Maharashtra, Odisha, Tamil Nadu, and by the Sri Lankan Gypsy people. It is one of six languages designated a classical language of India by the Government of India.Telugu ranks third by the number of native speakers in India (74 million, 2001 census),fifteenth in the Ethnologue list of most-spoken languages worldwide and is the most widely spoken Dravidian language. It is one of the twenty-two scheduled languages of the Republic of India.SOURCE:<a href="https://en.wikipedia.org/wiki/Telugu_language">Wikipedia</a>

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``telugu_``) to discover available Telugu corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('telugu')

   In [3]: c.list_corpora
   Out[3]:
   ['telugu_text_wikisource']
