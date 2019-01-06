Corpus Readers
*****************
After a corpus has been imported into the library, users will want to access the data through a ``CorpusReader`` object.
The ``CorpusReader`` API follows the NLTK CorpusReader API paradigm.
It offers a way for users to access the documents, paragraphs, sentences, and words of all the available documents in a corpus, or a specified collection of documents.
Not every corpus will support every method, e.g. a corpus of inscriptions may not support paragraphs via a ``para`` method but the corpus provider should try to provide the interfaces that they can.

Reading a Corpus
================
Use the ``get_corpus`` method in the readers module.

.. code-block:: python

   In [1]: from cltk.corpus.readers import get_corpus_reader

   In [2]: latin_corpus = get_corpus_reader(corpus_name = 'latin_text_latin_library', language = 'latin')

   In [3]: len(list(latin_corpus.docs()))

   Out[3]: 2141

   In [4]: len(list(latin_corpus.paras()))

   Out[4]: 212130

   In [5]: len(list(latin_corpus.sents()))

   Out[5]: 1038668

   In [6]: len(list(latin_corpus.words()))

   Out[6]: 16455728


Adding a Corpus to the CLTK Reader
==================================
Modify the cltk.corpus.readers module, updating ``SUPPORTED_CORPORA``, adding your language and the specific corpus name.
In the ``get_corpus_reader`` method implement the checks and mappings to return a NLTK compliant ``CorpusReader`` API object.


Providing Metadata for Corpus Filtration
==============================================

If you're adding a Corpus to CLTK, please also consider providing a genre mapping if you corpus is large or is easily segmented into genres.
Consider creating a file containing mappings of categories to directories and files, e.g.:

.. code-block:: python

   In [1]: from cltk.corpus.latin.latin_library_corpus_types import corpus_directories_by_type

   In [2]: corpus_directories_by_type.keys()

   Out [2]: dict_keys(['republican', 'augustan', 'early_silver', 'late_silver', 'old', 'christian', 'medieval', 'renaissance', 'neo_latin', 'misc', 'early'])

   In [3]: from cltk.corpus.latin.latin_library_corpus_types import corpus_texts_by_type

   In [4]: corpus_directories_by_type.values()[:3]

   Out [4]: [['./caesar', './lucretius', './nepos', './cicero'], ['./livy', './ovid', './horace', './vergil', './hyginus']]

   In [5]: from cltk.corpus.latin.latin_library_corpus_types import corpus_texts_by_type

   In [6]: list(corpus_texts_by_type.values())[:2]

   Out [6]: [['sall.1.txt', 'sall.2.txt', 'sall.cotta.txt', 'sall.ep1.txt', 'sall.ep2.txt', 'sall.frag.txt', 'sall.invectiva.txt', 'sall.lep.txt', 'sall.macer.txt', 'sall.mithr.txt', 'sall.phil.txt', 'sall.pomp.txt', 'varro.frag.txt', 'varro.ll10.txt', 'varro.ll5.txt', 'varro.ll6.txt', 'varro.ll7.txt', 'varro.ll8.txt', 'varro.ll9.txt', 'varro.rr1.txt', 'varro.rr2.txt', 'varro.rr3.txt', 'sulpicia.txt'], ['resgestae.txt', 'resgestae1.txt', 'manilius1.txt', 'manilius2.txt', 'manilius3.txt', 'manilius4.txt', 'manilius5.txt', 'catullus.txt', 'vitruvius1.txt', 'vitruvius10.txt', 'vitruvius2.txt', 'vitruvius3.txt', 'vitruvius4.txt', 'vitruvius5.txt', 'vitruvius6.txt', 'vitruvius7.txt', 'vitruvius8.txt', 'vitruvius9.txt', 'propertius1.txt', 'tibullus1.txt', 'tibullus2.txt', 'tibullus3.txt']]


The mapping is a dictionary of genre types or periods, and the values are lists of files or directories for each type.

Helper Methods for Corpus Filtration
====================================

Users will typically construct a ``CorpusReader`` by selecting category types of directories or files.
The ``assemble_corpus`` method allows users to take a CorpusReader and filter the files used provide the data for the reader.

.. code-block:: python

   In [1]: from cltk.corpus.readers import assemble_corpus, get_corpus_reader

   In [2]: from cltk.corpus.latin.latin_library_corpus_types import corpus_texts_by_type, corpus_directories_by_type

   In [3]: latin_corpus = get_corpus_reader(corpus_name = 'latin_text_latin_library', language = 'latin')

   In [4]: filtered_reader, fileids, catgories = assemble_corpus(latin_corpus, types_requested=['republican', 'augustan'], type_dirs=corpus_directories_by_type,
   ...     type_files=corpus_texts_by_type)

   In [5]: len(list(filtered_reader.docs()))

   Out [5]: 510

   In [6]: categories

   Out [6]: {'republican', 'augustan'}

   In [7]: len(fileids)

   Out [7]: 510


