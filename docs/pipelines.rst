Pipelines, Processes, Docs, and Words
=====================================

The CLTK contains four important, native data types:

- :class:`cltk.core.data_types.Word`: Contains all processed information for each word token. Has attributes including ``Word.string``, ``Word.lemma``, ``Word.pos``, ``Word.governor``, and ``Word.embedding``. A ``Process`` adds data to each ``Word``.
- :class:`cltk.core.data_types.Doc`: Contains ``Doc.raw``, which is the original input string to ``NLP().analyze()``, and ``Doc.words``, which is a list of ``Word`` objects. It is the input and output of each ``Process`` and final output of ``NLP()``.
- :class:`cltk.core.data_types.Process`: Takes and returns a ``Doc``. Each process does some processing of information within the ``Doc``, then annotates each ``Word`` object at ``Doc.words``.
- :class:`cltk.core.data_types.Pipeline`: Has a list of ``Process`` objects at ``Pipeline.processes``. Predefined pipelines have been made for some languages (:doc:`languages`), while custom pipelines may be made for these languages or other, different languages altogether.


How to Customize an NLP Pipeline
--------------------------------

The following illustrate how the four data types work by demonstrating how to wrap your own NLP algorithm with a custom ``Process`` and then add it to a default ``Pipeline``.


Process
*******

If you need to add your own ``Process`` to a pipeline, first create a new ``Process``. In the following example, a trivial function (``mk_upper_case``), which makes an uppercase version of each token, is wrapped by the new ``UpperProcess()``, which stores output values at ``Word.upper``. For an illustration, see figure :any:`processGraph`.

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




.. graphviz::
   :caption: Inheritance of ``Process`` class
   :name: processGraph

   digraph Processes {
     fontname = "Bitstream Vera Sans"
     fontsize = 8

     node [
       fontname = "Bitstream Vera Sans"
       fontsize = 8
       shape = "record"
     ]

     edge [
       arrowtail = "empty"
     ]

     Process [
       label = "{Process|\l| run(): Doc}"
     ]

     EmbeddingProcess [
       label = "{EmbeddingProcess|\l|}"
     ]

     NERProcess [
       label = "{NERProcess|\l|}"
     ]

     EtcProcess [
       label = "{…|\l|}"
     ]

     LatinEmbeddingProcess [
       label = "{LatinEmbeddingProcess|\l|algorithm(): FastTextEmbeddings(\"lat\")}"
     ]

     GreekEmbeddingProcess [
       label = "{GreekEmbeddingProcess|\l|algorithm(): FastTextEmbeddings(\"grc\")}"
     ]

     EtcEmbeddingsProcess [
       label = "{…|\l|algorithm(): Callable}"
     ]

     LatinNERProcess [
       label = "{LatinNERProcess|\l|algorithm(): tag_ner(\"lat\")}"
     ]

     GreekNERProcess [
       label = "{GreekNERProcess|\l|algorithm(): tag_ner(\"grc\")}"
     ]

     EtcNERProcess [
       label = "{…|\l|algorithm(): Callable}"
     ]

     Process -> EmbeddingProcess [dir=back]
     Process -> NERProcess [dir=back]
     Process -> EtcProcess [dir=back]
     EmbeddingProcess -> LatinEmbeddingProcess [dir=back]
     EmbeddingProcess -> GreekEmbeddingProcess [dir=back]
     EmbeddingProcess -> EtcEmbeddingsProcess [dir=back]
     NERProcess -> LatinNERProcess [dir=back]
     NERProcess -> GreekNERProcess [dir=back]
     NERProcess -> EtcNERProcess [dir=back]
   }


Pipeline
********

Once your custom ``Process`` has been created, you may then add it to your language's pipeline. To view a language's default pipeline, you may import it directly or access it through ``NLP().processes``. The following example imports the default Latin ``Pipeline``, appends ``UpperProcess`` to the end of it, adds the now-modified ``LatinPipeline`` to an instantiation of the ``NLP()`` class, and finally runs ``NLP().analyze()``.  For an illustration, see figure :any:`pipelineGraph`.

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
   >>> aquinas = "Adoro te devote latens deitas"
   >>> cltk_doc = cltk_nlp.analyze(aquinas)



.. graphviz::
   :caption: Inheritance of ``Pipeline`` class
   :name: pipelineGraph

   digraph Pipeline {
     fontname = "Bitstream Vera Sans"
     fontsize = 8

     node [
       fontname = "Bitstream Vera Sans"
       fontsize = 8
       shape = "record"
     ]

     edge [
       arrowtail = "empty"
     ]

     Pipeline [
       label = "{Pipeline|\l| run(): Doc}"
     ]

     LatinPipeline [
       label = "{LatinPipeline|\l|processes: [LatinStanzaProcess,\l LatinEmbeddingsProcess,\l StopsProcess,\l LatinNERProcess]}"
     ]

     GreekPipeline [
       label = "{GreekPipeline|\l|processes: [GreekStanzaProcess,\l GreekEmbeddingsProcess,\l StopsProcess,\l GreekNERProcess]}"
     ]

     EtcPipeline [
       label = "{…|\l|processes: List[Process]}"
     ]

     Pipeline -> LatinPipeline [dir=back]
     Pipeline -> GreekPipeline [dir=back]
     Pipeline -> EtcPipeline [dir=back]
   }



Doc
***

Inspecting the output ``Doc``, we can see a number of attributes and helper methods that provide processed information in a convenient manner.

.. code-block:: python

   >>> dir(cltk_doc)
   [..., 'embeddings', 'embeddings_model', 'language', 'lemmata', 'morphosyntactic_features', 'pipeline', 'pos', 'raw', 'sentences', 'sentences_strings', 'sentences_tokens', 'stanza_doc', 'stems', 'tokens', 'tokens_stops_filtered', 'words']
   >>> cltk_doc.tokens[:5]
   ['Adoro', 'te', 'devote', 'latens', 'deitas']
   >>> cltk_doc.pos[:5]
   ['VERB', 'PRON', 'ADV', 'VERB', 'NOUN']
   >>> cltk_doc.lemmata[:5]
   ['mdo', 'tu', 'devote', 'lateo', 'deitas']
   >>> cltk_doc.morphosyntactic_features[:5]
   [{'Mood': 'Ind', 'Number': 'Sing', 'Person': '2', 'Tense': 'Pres', 'VerbForm': 'Fin', 'Voice': 'Act'}, {'Case': 'Acc', 'Degree': 'Pos', 'Gender': 'Masc', 'Number': 'Sing', 'PronType': 'Prs'}, {'Degree': 'Pos'}, {'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Masc', 'Number': 'Sing', 'Tense': 'Pres', 'VerbForm': 'Part', 'Voice': 'Act'}, {'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}]
   >>> type(cltk_doc.embeddings[4])
   <class 'numpy.ndarray'>
   >>> cltk_doc.tokens_stops_filtered[:5]
   ['Adoro', 'devote', 'latens', 'deitas']
   >>> cltk_doc.sentences_strings
   ['Adoro te devote latens deitas']


Word
****

Looking directly at ``Doc.words``, we see a list of ``Word`` types.

.. code-block:: python

   >>> type(cltk_doc.words[2])
   <class 'cltk.core.data_types.Word'>
   >>> cltk_doc.words[2]
   Word(index_char_start=None, index_char_stop=None, index_token=2, index_sentence=0, string='devote', pos='ADV', lemma='devote', stem=None, scansion=None, xpos='L2|modM|tem4|grp1|casG', upos='ADV', dependency_relation='advmod', governor=3, features={'Degree': 'Pos'}, embedding=array([-4.2728e-01, ...], dtype=float32), stop=False, named_entity=False)
   >>> cltk_doc.words[2].upper
   'DEVOTE'

