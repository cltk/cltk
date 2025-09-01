Quickstart
==========

Installation
------------

Install via Pip:

.. code-block:: bash

   $ pip install cltk


Use
---

:class:`cltk.nlp.NLP()` has pre-configured processing pipelines for a number of :doc:`languages`. Executing :meth:`cltk.nlp.NLP.analyze()` returns a :obj:`cltk.core.data_types.Doc` object, which contains all processed information.

To process text:

.. code-block:: python

   >>> from cltk import NLP
   >>> vitruvius = "Architecti est scientia pluribus disciplinis et variis eruditionibus ornata, quae ab ceteris artibus perficiuntur. Opera ea nascitur et fabrica et ratiocinatione."
   >>> cltk_nlp = NLP(language="lat")
   ‎𐤀 CLTK version '1.0.11'.
   Pipeline for language 'Latin' (ISO: 'lat'): `LatinNormalizeProcess`, `LatinStanzaProcess`, `LatinEmbeddingsProcess`, `StopsProcess`, `LatinNERProcess`, `LatinLexiconProcess`.
   >>> cltk_doc = cltk_nlp.analyze(text=vitruvius)

Some NLP ``Process`` require downloaded models, which you will be prompted to download. You may then inspect the output ``Doc``, which contains the information produced by each ``Process`` step:

.. code-block:: python

   >>> cltk_doc.tokens[:5]
   ['Architecti', 'est', 'scientia', 'pluribus', 'disciplinis']
   >>> cltk_doc.lemmata[:5]
   ['mrchiteo', 'sum', 'scientia', 'multus', 'disciplina']
   >>> cltk_doc.morphosyntactic_features[2]  # 'scientia'
   {Case: [nominative], Degree: [positive], Gender: [feminine], Number: [singular]}
   >>> cltk_doc.pos[:5]
   ['VERB', 'AUX', 'NOUN', 'ADJ', 'NOUN']
   >>> cltk_doc.sentences_tokens
   [['Architecti', 'est', 'scientia', 'pluribus', 'disciplinis', ...], ...]


Most processes add their information to a list of ``Word`` objects at ``Doc.words``:

   >>> cltk_doc.words[1].string
   'est'
   >>> cltk_doc.words[1].stop
   True
   >>> cltk_doc.words[1].lemma
   'sum'
   >>> cltk_doc.words[4].definition[:200]
   'disciplīna\n\n\n ae, \nf\n\ndiscipulus, \ninstruction, tuition, teaching, training, education\n: puerilis: adulescentīs in disciplinam ei tradere:\n                te in disciplinam meam tradere: in disciplina'
   >>> cltk_doc.words[4].pos
   'NOUN'
   >>> cltk_doc.words[4].category
   {F: [neg], N: [pos], V: [neg]}
   >>> cltk_doc.words[4].features
   {Case: [ablative], Degree: [positive], Gender: [feminine], Number: [plural]}
   >>> cltk_doc.words[4].dependency_relation
   'obl'
   >>> cltk_doc.words[4].governor  # this word's "parent"
   8
   >>> cltk_doc.words[8].string  # looking at this word
   'ornata'
   >>> cltk_doc.words[4].embedding[:5]
   array([-0.10924 , -0.048127,  0.15953 , -0.19465 ,  0.17935 ],
         dtype=float32)
   >>> cltk_doc.words[2].embedding[:5]  # 'scientia'
   array([-0.28462 ,  0.64238 , -0.40037 ,  0.39382 ,  0.060418],
         dtype=float32)
   >>> cltk_doc.words[5].index_sentence  # sentence to which a token belongs
   0
   >>> cltk_doc.words[20].index_sentence
   1


For more, see :doc:`pipelines`.


Tutorials
---------

Demonstration notebooks available at `<https://github.com/cltk/cltk/blob/master/notebooks>`_.
