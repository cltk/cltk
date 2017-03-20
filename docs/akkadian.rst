Akkadian
********

Akkadian is an extinct East Semitic language (part of the greater Afroasiatic language family) that was spoken in ancient Mesopotamia. \
The earliest attested Semitic language, it used the cuneiform writing system, which was originally used to write the unrelated Ancient \
Sumerian, a language isolate. From the second half of the third millennium BC (ca. 2500 BC), texts fully written in Akkadian begin to \
appear. Hundreds of thousands of texts and text fragments have been excavated to date, covering a vast textual tradition of \
mythological narrative, legal texts, scientific works, correspondence, political and military events, and many other examples. \
By the second millennium BC, two variant forms of the language were in use in Assyria and Babylonia, known as Assyrian and \
Babylonian respectively. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Akkadian>`_)


Syllabifier
=========

Syllabify Akkadian words.

.. code-block:: python

   In [1]: from cltk.stem.akkadian.syllabifier import Syllabifier

   In [2]: word = "epištašu"

   In [3]: syll = Syllabifier()

   In [4]: syll.syllabify(word)
   ['e', 'piš', 'ta', 'šu']
