Ancient Egyptian
****************

The language spoken in ancient Egypt was a branch of the Afroasiatic language family. The earliest known complete written sentence in the Egyptian language has been dated to about 2690 BCE, making it one of the oldest recorded languages known, along with Sumerian. Egyptian was spoken until the late seventeenth century in the form of Coptic. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Egyptian_language>`_)


Transliterate MdC
=================

MdC (Manuel de Codage) is the standard encoding scheme and a series of conventions for transliterating egyptian texts. At first it was also conceieved as a system to represent positional relations between hieroglyphic signs. However it was soon realised that the scheme used by MdC was not really appropriate for this last task. Hence the current softwares for hieroglyphic typesetting use often slightly different schemes than MdC. For more on MdC, see `here
<https://en.wikipedia.org/wiki/Manuel_de_Codage>`_ and `here <http://www.catchpenny.org/codage/#trans>`_

Transliteration conventions proposed by MdC are widely accepted though. Since at that time the transliteration conventions of the egyptology were not covered by the unicode, MdC's all-ascii proposition made it possible to exchange at least transliterations in digital environement. It is the de facto transliteration system used by Thesaurus Linguae Aegyptiae which includes transliterations from several different scripts used in Ancient Egypt: a good discussion can be found `here <http://jsesh.qenherkhopeshef.org/fr/node/434>`_

The unicode still doesn't cover all of the transliteration conventions used within the egyptology, but there has been a lot of progress. Only three characters are now problematic and are not covered by precomposed characters of the Unicode Consortium.

* Egyptological Yod       

* Capital H4       

* Small and Capital H5: almost exclusively used for transliterating demotic script.

The function is created in the view of transliteration `font <http://www.yare.org/egypt/fonts.htm>`_ provided by CCER which maps couple of extra characters to transliterated equivalents such as '¡' or '@' for Ḥ.

There is also a q_kopf flag for choosing between the 'q' or 'ḳ' at the resulting text.

Usage:

Import the function:

.. code-block:: python

    In [1]: from cltk.corpus.egyptian.transliterate_mdc import mdc_unicode

Take a MdC encoded string (P.Berlin 3022:28-31):

.. code-block:: python

    In [1]: mdc_string = """rdi.n wi xAst n xAst
    fx.n.i r kpny Hs.n.i r qdmi
    ir.n.i rnpt wa gs im in wi amw-nnSi
    HqA pw n rtnw Hrt"""

Ensure that `mdc_string` is encoded in unicode characters (this is mostly unnecessary):

.. code-block:: python

 In [2]: mdc_string.encode().decode("utf-8")
 Out[6]: 
 ''rdi.n wi xAst n xAst\nfx.n.i r kpny Hs.n.i r qdmi\nir.n.i rnpt wa gs im in wi amw-nnSi\nHqA pw n rtnw Hrt''

Apply the function to obtain the unicode map result:

.. code-block:: python

    In [10]: unicode_string = mdc_unicode(mdc_string)
    In [11]: print(unicode_string)
    rdi҆.n wi҆ ḫꜣst n ḫꜣst
    fḫ.n.i҆ r kpny ḥs.n.i҆ r qdmi҆
    i҆r.n.i҆ rnpt wꜥ gs i҆m i҆n wi҆ ꜥmw-nnši҆
    ḥqꜣ pw n rtnw ḥrt

If you disable the option q_kopf, the result would be following:

.. code-block:: python

    In [136]: unicode_string = mdc_unicode(mdc_string, q_kopf=False)

    In [152]: print(unicode_string)
    rdi҆.n wi҆ ḫꜣst n ḫꜣst
    fḫ.n.i҆ r kpny ḥs.n.i҆ r ḳdmi҆
    i҆r.n.i҆ rnpt wꜥ gs i҆m i҆n wi҆ ꜥmw-nnši҆
    ḥḳꜣ pw n rtnw ḥrt

Notice the q -> ḳ transformation.

If you are going to pass a string object read from a file be sure to precise the encoding during the opening of the file:

.. code-block:: python

    with open("~/mdc_text.txt", "r", encoding="utf-8") as f:
        mdc_text = f.read()
        unicode_text = mdc_unicode(mdc_text)

Notice `encoding="utf-8"`.



TODO
-----

* Add support for different transliteration systems used within egyptology.
* Add an option to for i -> j transformation for facilitating computer based operations.
* Add support for the problematic characters in future.






