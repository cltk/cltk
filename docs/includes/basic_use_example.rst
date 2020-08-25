:class:`cltk.nlp.NLP()` has pre-configured processing pipelines for a number of :ref:`Languages`_. Executing :meth:`cltk.nlp.NLP.analyze()` returns a :obj:`cltk.core.data_types.Doc` object, which contains all processed information.

To process text:

.. code-block:: python

   >>> from cltk import NLP
   >>> vitruvius = "Architecti est scientia pluribus disciplinis et variis eruditionibus ornata, quae ab ceteris artibus perficiuntur. Opera ea nascitur et fabrica et ratiocinatione."
   >>> cltk_nlp = NLP(language="lat")
   >>> cltk_doc = cltk_nlp.analyze(text=vitruvius)

You may then inspect the output object:

.. code-block:: python

   >>> cltk_doc.tokens[:5]
   ['Architecti', 'est', 'scientia', 'pluribus', 'disciplinis']
   >>> cltk_doc.words[1].string
   'est'
   >>> cltk_doc.words[1].stop
   True
   >>> cltk_doc.words[4].string
   'disciplinis'
   >>> cltk_doc.words[4].stop
   False
   >>> cltk_doc.words[4].lemma
   'disciplina'
   >>> cltk_doc.words[4].pos
   'NOUN'
   >>> cltk_doc.words[4].xpos
   'A1|grn1|casO|gen2'
   >>> cltk_doc.words[4].governor
   8
   >>> cltk_doc.words[8].string
   'ornata'
   >>> cltk_doc.words[4].dependency_relation
   'obl'
   >>> cltk_doc.words[4].embedding[:5]
   array([-0.10924 , -0.048127,  0.15953 , -0.19465 ,  0.17935 ],
         dtype=float32)
   >>> cltk_doc.words[5].index_sentence
   0
   >>> cltk_doc.words[20].index_sentence
   1


For more, see :ref:`Pipelines, Processes, Docs, and Words`_.