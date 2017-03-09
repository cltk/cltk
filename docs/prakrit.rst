Prakrit
*******

About
=======

A Prakrit is any of several Middle Indo-Aryan languages.

The Ardhamagadhi ("half-Magadhi") Prakrit, which was used extensively to write the scriptures of Jainism, is often considered to be the definitive form of Prakrit, while others are considered variants thereof. Prakrit grammarians would give the full grammar of Ardhamagadhi first, and then define the other grammars with relation to it. For this reason, courses teaching "Prakrit" are often regarded as teaching Ardhamagadhi.Pali, the Prakrit used in Theravada Buddhism, tends to be treated as a special exception from the variants of the Ardhamagadhi language, as Classical Sanskrit grammars do not consider it as a Prakrit per se, presumably for sectarian rather than linguistic reasons. Other Prakrits are reported in old historical sources but are not attested, such as Paiśācī. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Prakrit>`_)

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``prakrit_``) to discover available Prakrit corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('prakrit')

   In [3]: c.list_corpora
   Out[3]: ['prakrit_texts_gretil']

