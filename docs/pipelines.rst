Pipelines, Processes, Docs, and Words
=====================================

.. todo::

   Add here summary of all three and how they work. maybe svg graphic


The CLTK comes with pre-configured pipelines of for many :ref:`languages`.


Processes
---------

If you need to add your own ``Process`` to this a pipeline, first create a new ``Process``. In the follow example, a trivial function (``mk_upper_case``), which makes an uppercase version of each token, is wrapped by the new ``UpperProcess()``, which stores the output value at at ``Word.upper``.

.. code-block:: python

   >>> from copy import deepcopy
   >>> from cltk.core.data_types import Doc, Process, Word
   >>> def mk_upper_case(word: str) -> str:
   ...    return word.upper()
   >>> class UpperProcess(Process):
   ...     def run(self, input_doc: Doc) -> Doc:
   ...         stem = self.algorithm
   ...         output_doc = deepcopy(input_doc)
   ...         for word in output_doc.words:
   ...             word.upper = mk_upper_case(word.string)
   ...         return output_doc
   ...
   ...     @staticmethod
   ...     def algorithm(word: str) -> str:
   ...         return mk_upper_case(word)
   >>> cltk_doc = Doc(language="lat", raw="arma virmque cano", words=[
   ...     Word(string="arma"), Word(string="virumque"), Word(string="cano")
   ... ])
   >>> cltk_doc.words[0].string
   'arma'
   >>> custom_process_mk_upper = UpperProcess()
   >>> cltk_doc_processed = custom_process_mk_upper.run(input_doc=cltk_doc)
   >>> cltk_doc_processed.words[0].string
   'arma'
   >>> cltk_doc_processed.words[0].upper
   'ARMA'



Pipelines
---------

Once your custom ``Process`` has been created, you may then add it to your language's pipeline. To view a language's default pipeline, you may import it directly or access it through ``NLP().processes``. The following example imports the default Latin ``Pipeline``, appends the above custom ``UpperProcess`` to the end of the ``Pipeline``, adds the now-modified ``LatinPipeline`` to an instantiation of the ``NLP()`` class, and finally runs it.

.. code-block:: python

   >>> from cltk.languages.pipelines import LatinPipeline
   >>> lat_pipeline = LatinPipeline()
   >>> lat_pipeline.processes
   [<class 'cltk.dependency.processes.LatinStanzaProcess'>, <class 'cltk.embeddings.processes.LatinEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.LatinNERProcess'>]
   >>> lat_pipeline.add_process(UpperProcess)
   >>> lat_pipeline.processes
   [<class 'cltk.dependency.processes.LatinStanzaProcess'>, <class 'cltk.embeddings.processes.LatinEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.LatinNERProcess'>]

   >>> from cltk import NLP
   >>> cltk_nlp = NLP(language="lat")
   >>> cltk_nlp.pipeline = lat_pipeline
   >>> cltk_nlp.pipeline.processes
   [<class 'cltk.dependency.processes.LatinStanzaProcess'>, <class 'cltk.embeddings.processes.LatinEmbeddingsProcess'>, <class 'cltk.stops.processes.StopsProcess'>, <class 'cltk.ner.processes.LatinNERProcess'>, <class '__main__.CustomProcess'>]
   >>> >>> aquinas = "Adoro te devote latens deitas"
   >>> cltk_doc = cltk_nlp.analyze(aquinas)
   >>> >>> cltk_doc.words[0].upper
   'ADORO'


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
