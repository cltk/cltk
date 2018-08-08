Old Swedish
***********

Old Swedish (fornsvenska) is a language spoken in Sweden between (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Swedish>`_)


Phonological transcription
==========================

According to phonological rules, a reconstructed phonology/pronunciation of Old Swedish words is implemented.

.. code-block:: python

    In [1]: from cltk.phonology.old_swedish import transcription as old_swedish

    In [2]: from cltk.phonology import utils as ut

    In [3]: sentence = "Far man kunu oc dör han för en hun far barn. oc sigher hun oc hænnæ frændær."

    In [4]:  tr = ut.Transcriber(old_swedish.DIPHTHONGS_IPA, old_swedish.DIPHTHONGS_IPA_class, old_swedish.IPA_class,
                            old_swedish.old_swedish_rules)

    In [5]: tr.main(sentence)

    Out [5]: "[far man kunu ok dør han før ɛn hun far barn ok siɣɛr hun ok hɛnːɛ frɛndɛr]"


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``old_swedish_``) to discover available Old Swedish corpora.

.. code-block:: python

    In [1]: from cltk.corpus.utils.importer import CorpusImporter

    In [2]: corpus_importer = CorpusImporter("old_swedish")

    In [3]: corpus_importer.list_corpora

    Out [3]: ['old_swedish_texts', ]
