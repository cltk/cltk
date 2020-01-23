"""Primary module for CLTK pipeline."""

from typing import List

from cltkv1.core.data_types import Doc, Language, Pipeline, Type
from cltkv1.core.exceptions import UnimplementedLanguageError, UnknownLanguageError
from cltkv1.languages.pipelines import (
    GothicPipeline,
    GreekPipeline,
    LatinPipeline,
    OCSPipeline,
    OldFrenchPipeline,
)
from cltkv1.languages.utils import get_lang

pipelines = {
    "lat": LatinPipeline,
    "grc": GreekPipeline,
    "chu": OCSPipeline,
    "fro": OldFrenchPipeline,
    "got": GothicPipeline,
}


class NLP:
    """NLP class for default processing."""

    def __init__(self, language: str, custom_pipeline: Pipeline = None) -> None:
        """Constructor for CLTK class.

        >>> from cltkv1 import NLP
        >>> cltk_nlp = NLP(language="lat")
        >>> isinstance(cltk_nlp, NLP)
        True
        >>> NLP(language="xxx")
        Traceback (most recent call last):
          ...
        cltkv1.core.exceptions.UnknownLanguageError: Unknown language 'xxx'. Use ISO 639-3 languages.
        >>> from cltkv1.core.data_types import Pipeline
        >>> from cltkv1.tokenizers import LatinTokenizationProcess
        >>> from cltkv1.languages.utils import get_lang
        >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess], language=get_lang("lat"))
        >>> nlp = NLP(language="lat", custom_pipeline=a_pipeline)
        >>> nlp.pipeline is a_pipeline
        True
        """
        try:
            self.language = get_lang(language)  # type: Language
        except UnknownLanguageError:
            raise UnknownLanguageError(
                f"Unknown language '{language}'. Use ISO 639-3 languages."
            )
        self.pipeline = custom_pipeline if custom_pipeline else self._get_pipeline()

    def _get_pipeline(self) -> Pipeline:
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.

        >>> from cltkv1 import NLP
        >>> from cltkv1.core.data_types import Pipeline
        >>> cltk_nlp = NLP(language="lat")
        >>> lat_pipeline = cltk_nlp._get_pipeline()
        >>> isinstance(cltk_nlp.pipeline, Pipeline)
        True
        >>> isinstance(lat_pipeline, Pipeline)
        True
        >>> cltk_nlp = NLP(language="axm")
        Traceback (most recent call last):
          ...
        cltkv1.core.exceptions.UnimplementedLanguageError: axm
        """
        try:
            return pipelines[self.language.iso_639_3_code]()
        except KeyError:
            raise UnimplementedLanguageError(self.language.iso_639_3_code)

    def analyze(self, text: str) -> Doc:
        """The primary method for the NLP object, to which raw text strings are passed.

        TODO: Run the OF example and then log the FileNotFoundError inside the `stanford.py` module


        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import get_example_text
        >>> from cltkv1.core.data_types import Doc
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> isinstance(cltk_doc, Doc)
        True
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None, xpos='A1|grn1|casA|gen2|stAM', upos='NOUN', dependency_relation='nsubj', governor=..., parent=..., features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=None)

        >>> from cltkv1.utils.example_texts import get_example_text
        >>> cltk_nlp = NLP(language="grc")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("grc"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='ὅτι', pos='Df', lemma='ὅτι#1', scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=..., parent=..., features={}, embedding=None)

        >>> cltk_nlp = NLP(language="chu")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("chu"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='отьчє', pos='Nb', lemma='отьць', scansion=None, xpos='Nb', upos='NOUN', dependency_relation='nsubj', governor=..., parent=..., features={'Case': 'Nom', 'Gender': 'Masc', 'Number': 'Sing'}, embedding=None)

        >>> cltk_nlp = NLP(language="fro")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("fro"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Une', pos='DETndf', lemma='Une', scansion=None, xpos='DETndf', upos='DET', dependency_relation='det', governor=..., parent=..., features={'Definite': 'Ind', 'PronType': 'Art'}, embedding=None)

        >>> cltk_nlp = NLP(language="got")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("got"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='swa', pos='Df', lemma='swa', scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=..., parent=..., features={}, embedding=None)
        >>> len(cltk_doc.sentences)
        4
        """
        doc = Doc(language=self.language.iso_639_3_code, raw=text)

        for process in self.pipeline.processes:
            a_process = process(input_doc=doc, language=self.language.iso_639_3_code)
            a_process.run()
            doc = a_process.output_doc

        return doc
