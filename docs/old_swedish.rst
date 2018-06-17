Old Swedish
*********

 (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Norse>`_)


Phonology transcription
=======================

According to phonological rules (available at `Wikipedia - Old Norse orthography <https://en.wikipedia.org/wiki/Old_Norse_orthography>`_  and *Altnordisches Elementarbuch* by Friedrich Ranke and Dietrich Hofmann), a reconstructed pronunciation of Old Norse words is implemented.

.. code-block:: python

    In [1]: from cltk.phonology.old_swedish import transcription as old_swedish_transcription

    In [2]: sentence = ""

    In [3]: tr = old_swedish_transcription.Transcriber()

    In [4]: tr.main(sentence, old_swedish_transcription.old_swedish_rules)

    Out [4]: ""

