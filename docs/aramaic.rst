Aramaic
********

Aramaic is a language or group of languages 
belonging to the Semitic subfamily of the Afroasiatic language family. More
specifically, it is part of the Northwest Semitic group, which also includes
the Canaanite languages such as Hebrew and Phoenician. The Aramaic alphabet
was widely adopted for other languages and is ancestral to the Hebrew, Syriac
and Arabic alphabets. During its approximately 3,100 years of written
history, Aramaic has served variously as a language of administration of
empires, as a language of divine worship and religious study, and as the
spoken tongue of a number of Semitic peoples from the Near East. (Source:
`Wikipedia <https://en.wikipedia.org/wiki/Aramaic>`_)


Transliterate Square Script To Imperial Aramaic
===============================================

Unicode recently included a separate code block for encoding characters in
Imperial Aramaic. Traditionally documents written in Imperial Aramaic are
taught and shared using square script. Here is a small function for converting
a string written in square script to its Imperial Aramaic version.

Usage:

Import the function:

.. code-block:: python

    In [1]: from cltk.corpus.aramaic.transliterate import square_to_imperial

Take a string written in square script:

.. code-block:: python

    In [2]: mystring = "פדי בר דג[נ]מלך לאחא בר חפיו נתנת לך"

Convert it to Imperial Aramaic by passing it to our function

.. code-block:: python

    In [3]: square_to_imperial(mystring)
    Out[3]: "𐡐𐡃𐡉 𐡁𐡓 𐡃𐡂[𐡍]𐡌𐡋𐡊 𐡋𐡀𐡇𐡀 𐡁𐡓 𐡇𐡐𐡉𐡅 𐡍𐡕𐡍𐡕 𐡋𐡊"
