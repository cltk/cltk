                                                                                             Old Swedish
*********

Old Swedish (fornsvenska) is a language spoken in Sweden between (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Swedish>`_)


Phonology transcription
=======================

According to phonological rules a reconstructed phonology/pronunciation of Old Norse words is implemented.

<http://project2.sol.lu.se/fornsvenska/index.html>
.. code-block:: python

    In [1]: from cltk.phonology.old_swedish import transcription as old_swedish_transcription

    In [2]: sentence = ""

    In [3]: tr = old_swedish_transcription.Transcriber()

    In [4]: tr.main(sentence, old_swedish_transcription.old_swedish_rules)

    Out [4]: ""

