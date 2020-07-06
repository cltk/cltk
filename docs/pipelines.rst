Pipelines, Processes, Docs, and Words
=====================================

Pipelines
---------

When :class:`cltk.nlp.NLP()` is initialized with a language, that \
language's pre-configured ``Process`` is fetched and stored at \
``NLP().pipeline.processes``.

.. code-block:: python

   >>> from cltk import NLP
   >>> cltk_nlp = NLP(language="lat")
   >>> cltk_nlp.pipeline.processes
   [<class 'cltk.dependency.processes.LatinStanzaProcess'>, <class 'cltk.embeddings.processes.LatinEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.LatinNERProcess'>]


Processes
---------

In this case of Latin, the ``Process``es do the following:

- :class:`cltk.dependency.processes.LatinStanzaProcess()`: Tokenize words, split sentences, tag POS, parse dependency syntax
- :class:`cltk.embeddings.processes.LatinEmbeddingsProcess()`: Look up word embedding vector for each token
- :class:`cltk.stops.processes.StopsProcess()`: Annotate whether a word is a stopword.
- :class:`cltk.ner.processes.LatinNERProcess()`: Annotate whether a word is a named entity.


When ``NLP().analyze`` is called, the input text is sent through the each \
``Process`` in succession (i.e., from first to last) and all information is \
stored in a :class:`cltk.core.data_types.Doc`.

.. code-block:: python

   >>> vitruvius = "Architecti est scientia pluribus disciplinis et variis eruditionibus ornata, quae ab ceteris artibus perficiuntur. Opera ea nascitur et fabrica et ratiocinatione."
   >>> cltk_doc = cltk_nlp.analyze(text=vitruvius)
   >>> type(cltk_doc)
   <class 'cltk.core.data_types.Doc'>


Docs
----

The instantiated ``Doc`` contains a number of helper methods which provide \
processed information in a convenient manner.

.. code-block:: python

   >>> dir(cltk_doc)
   [..., 'embeddings', 'embeddings_model', 'language', 'lemmata', 'morphosyntactic_features', 'pipeline', 'pos', 'raw', 'sentences', 'sentences_strings', 'sentences_tokens', 'stanza_doc', 'tokens', 'tokens_stops_filtered', 'words']
   >>> cltk_doc.tokens[:10]
   ['Architecti', 'est', 'scientia', 'pluribus', 'disciplinis', 'et', 'variis', 'eruditionibus', 'ornata', ',']
   >>> cltk_doc.pos[:10]
   ['VERB', 'AUX', 'NOUN', 'ADJ', 'NOUN', 'CCONJ', 'ADJ', 'NOUN', 'VERB', 'PUNCT']
   >>> cltk_doc.lemmata[:10]
   ['mrchiteo', 'sum', 'scientia', 'multus', 'disciplina', 'et', 'varius', 'eruditio', 'orno', ',']
   >>> cltk_doc.morphosyntactic_features[:10]
   [{'Aspect': 'Perf', 'Case': 'Gen', 'Degree': 'Pos', 'Gender': 'Masc', 'Number': 'Sing', 'Tense': 'Past', 'VerbForm': 'Part', 'Voice': 'Pass'}, {'Mood': 'Ind', 'Number': 'Sing', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Act'}, {'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, {'Case': 'Abl', 'Degree': 'Cmp', 'Gender': 'Fem', 'Number': 'Plur'}, {'Case': 'Abl', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur'}, {}, {'Case': 'Abl', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur'}, {'Case': 'Abl', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Plur'}, {'Aspect': 'Perf', 'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing', 'Tense': 'Past', 'VerbForm': 'Part', 'Voice': 'Pass'}, {}]
   >>> type(cltk_doc.embeddings[0])
   <class 'numpy.ndarray'>
   >>> cltk_doc.tokens_stops_filtered[:10]
   ['Architecti', 'scientia', 'pluribus', 'disciplinis', 'variis', 'eruditionibus', 'ornata', ',', 'ceteris', 'artibus']
   >>> cltk_doc.sentences_strings
   ['Architecti est scientia pluribus disciplinis et variis eruditionibus ornata , quae ab ceteris artibus perficiuntur .', 'Opera ea nascitur et fabrica et ratiocinatione .']


Words
-----

A helper method works by looking into the attribute ``Doc.words``, \
which contains a list of :class:`cltk.core.data_types.Word` objects, \
one for each token.

.. code-block:: python

   >>> len(cltk_doc.tokens)
   24
   >>> len(cltk_doc.words)
   24
   >>> type(cltk_word)
   <class 'cltk.core.data_types.Word'>
   >>> dir(cltk_word)
   [..., 'dependency_relation', 'embedding', 'features', 'governor', 'index_char_start', 'index_char_stop', 'index_sentence', 'index_token', 'lemma', 'named_entity', 'pos', 'scansion', 'stop', 'string', 'upos', 'xpos']
   >>> cltk_word.string
   'disciplinis'
   >>> cltk_word.lemma
   'disciplina'
   >>> cltk_word.stop
   False
   >>> cltk_word.pos
   'NOUN'
   >>> cltk_word.xpos
   'A1|grn1|casO|gen2'
   >>> cltk_word.embedding[:5]
   array([-0.10924 , -0.048127,  0.15953 , -0.19465 ,  0.17935 ],
         dtype=float32)


Modifying pipelines
-------------------

.. todo::

   Illustrate removing a process.


Custom processes
----------------

The CLTK contains many functions for which a ``Process`` is not written. \
And a user may choose define his own NLP algorithm and write a custom Process \
for it.

.. todo::

   Illustrate format of new Process.


New pipeline
------------

.. todo::
   Illustrate writing Pipeline for a new language.
