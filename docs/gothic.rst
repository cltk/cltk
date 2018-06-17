Gothic
******

 Gothic is an extinct East Germanic language that was spoken by the Goths. It is known primarily from the Codex Argenteus, a 6th-century copy of a 4th-century Bible translation, and is the only East Germanic language with a sizable text corpus. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Gothic_language>`_)


Phonology transcription
=======================

According to phonological rules (available at `Wikipedia - Old Norse orthography <https://en.wikipedia.org/wiki/Old_Norse_orthography>`_  and *Altnordisches Elementarbuch* by Friedrich Ranke and Dietrich Hofmann), a reconstructed pronunciation of Old Norse words is implemented.

.. code-block:: python

    In [1]: from cltk.phonology.gothic import transcription as gt

    In [2]: sentence = "Anastodeins aiwaggeljons Iesuis Xristaus sunaus gudis."

    In [3]: tr = ont.Transcriber()

    In [4]: tr.main(sentence, ont.gothic_rules)

    Out [4]:
        "[anastɔdɛins aiwagːɛljɔns iɛsuis ksristaus sunaus gudis]"