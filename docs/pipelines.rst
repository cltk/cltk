Pipelines, Processes, Docs, and Words
=====================================

.. tip::

   See notebook `<https://github.com/cltk/cltk/blob/master/notebooks/CLTK%20data%20types.ipynb>`_ for a detailed walkthrough of CLTK data types.


The CLTK contains four important, native data types:

- :class:`cltk.core.data_types.Word`: Contains all processed information for each word token. Has attributes including ``Word.string``, ``Word.lemma``, ``Word.pos``, ``Word.governor``, and ``Word.embedding``. A ``Process`` adds data to each ``Word``. See notebook `<https://github.com/cltk/cltk/blob/master/notebooks/CLTK%20Demonstration.ipynb>`_ for a full demonstration of what kind of information is stored in ``Word``.
- :class:`cltk.core.data_types.Sentence`: Contains ``sentence_embeddings`` a weighted average of the word embeddings of the sentence.
- :class:`cltk.core.data_types.Doc`: Contains ``Doc.raw``, which is the original input string to ``NLP().analyze()``, and ``Doc.words``, which is a list of ``Word`` objects. It is the input and output of each ``Process`` and final output of ``NLP()``. See notebook `<https://github.com/cltk/cltk/blob/master/notebooks/CLTK%20Demonstration.ipynb>`_ for a full demonstration of what kind of information is stored in ``Doc``
- :class:`cltk.core.data_types.Process`: Takes and returns a ``Doc``. Each process does some processing of information within the ``Doc``, then annotates each ``Word`` object at ``Doc.words``.
- :class:`cltk.core.data_types.Pipeline`: Has a list of ``Process`` objects at ``Pipeline.processes``. Predefined pipelines have been made for some languages (:doc:`languages`), while custom pipelines may be created for these languages or other, different languages. See notebook `<https://github.com/cltk/cltk/blob/master/notebooks/Make%20custom%20Process%20and%20add%20to%20Pipeline.ipynb>`_ for an example creating a new ``Process`` and adding it to a custom ``Pipeline``. For an illustration of how ``Process`` objects inherit from one another, see figure :any:`pipelineGraph`.



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
