Marathi
********
Marathi is an Indian language spoken predominantly by the Marathi people of Maharashtra.
It is the official language and co-official language in the Maharashtra and Goa states of Western India, respectively,
and is one of the 22 scheduled languages of India. There were 73 million speakers in 2007; Marathi ranks 19th in the list of most spoken languages in the world.
Marathi has the fourth largest number of native speakers in India, after Hindi, Bengali and Telugu in that order.Marathi has some of the oldest literature of all modern Indo-Aryan languages, dating from about 900 AD.
The major dialects of Marathi are Standard Marathi and the Varhadi dialect. Malvani Konkani has been heavily influenced by Marathi varieties. The earliest example of the existence of Marathi as an independent language dates back to more than 2,000 years.

Source: `Wikipedia
https://en.wikipedia.org/wiki/Marathi_language`_.

Corpora
=======
Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``marathi_``) to discover available Marathi corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('marathi')

   In [3]: c.list_corpora
   Out[3]:
   ['marathi_text_wikisource']

Tokenizer
=========
This tool can help break up a sentence into smaller constituents.

.. code-block:: python

   In [1]: from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex as i_word

   In [2]: sentence = "आतां विश्वात्मके देवे, येणे वाग्यज्ञे तोषावे, तोषोनि मज द्यावे, पसायदान हे "

   In [3]: marathi_text_tokenize = i_word(sentence)

   In [4]: marathi_text_tokenize
   ['आतां', 'विश्वात्मके', 'देवे,', 'येणे', 'वाग्यज्ञे', 'तोषावे,', 'तोषोनि', 'मज', 'द्यावे,', 'पसायदान', 'हे']



