Gothic
******

 Gothic is an extinct East Germanic language that was spoken by the Goths. It is known primarily from the Codex Argenteus, a 6th-century copy of a 4th-century Bible translation, and is the only East Germanic language with a sizable text corpus. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Gothic_language>`_)


Phonological transcription
==========================

.. code-block:: python



    In [1]: from cltk.phonology.gothic import transcription as gt

    In [2]: sentence = "Anastodeins aiwaggeljons Iesuis Xristaus sunaus gudis."

    In [3]: tr = ut.Transcriber(gt.DIPHTHONGS_IPA, gt.DIPHTHONGS_IPA_class, gt.IPA_class, gt.gothic_rules)

    In [4]: tr.main(sentence, gt.gothic_rules)

    Out [4]:
        "[anastoːðiːns ɛwaŋgeːljoːns jeːsuis kristɔs sunɔs guðis]"