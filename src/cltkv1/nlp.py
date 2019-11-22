"""Primary module for CLTK pipeline."""

from typing import List

from cltkv1.languages.glottolog import get_lang
from cltkv1.utils.data_types import Doc, Language, Pipeline, Type
from cltkv1.utils.exceptions import UnknownLanguageError
from cltkv1.utils.pipelines import (
    DefaultPipeline,
    GothicPipeline,
    GreekPipeline,
    LatinPipeline,
    OCSPipeline,
    OldFrenchPipeline,
)


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
        cltkv1.utils.exceptions.UnknownLanguageError: Unknown language 'xxx'. Use ISO 639-3 languages.
        >>> from cltkv1.utils.data_types import Pipeline
        >>> from cltkv1.tokenizers import LatinTokenizationProcess
        >>> from cltkv1.languages.glottolog import LANGUAGES
        >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess], language=LANGUAGES["lat"])
        >>> NLP(language="lat", custom_pipeline=a_pipeline)
        Traceback (most recent call last):
          ...
        NotImplementedError: Custom pipelines not implemented yet.
        """
        try:
            self.language = get_lang(language)  # type: Language
        except UnknownLanguageError:
            raise UnknownLanguageError(
                f"Unknown language '{language}'. Use ISO 639-3 languages."
            )
        if custom_pipeline:
            raise NotImplementedError("Custom pipelines not implemented yet.")
        self.pipeline = self._get_pipeline()  # type: Pipeline

    def _get_pipeline(self) -> Type[Pipeline]:
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.data_types import Pipeline
        >>> cltk_nlp = NLP(language="lat")
        >>> lat_pipeline = cltk_nlp._get_pipeline()
        >>> issubclass(cltk_nlp.pipeline, Pipeline)
        True
        >>> issubclass(lat_pipeline, Pipeline)
        True
        >>> cltk_nlp = NLP(language="axm")
        >>> from cltkv1.utils.pipelines import DefaultPipeline
        >>> cltk_nlp.pipeline is DefaultPipeline
        True
        """

        if self.language.iso_639_3_code == "lat":
            current_pipeline = LatinPipeline
        elif self.language.iso_639_3_code == "grc":
            current_pipeline = GreekPipeline
        elif self.language.iso_639_3_code == "chu":
            current_pipeline = OCSPipeline
        elif self.language.iso_639_3_code == "fro":
            current_pipeline = OldFrenchPipeline
        elif self.language.iso_639_3_code == "got":
            current_pipeline = GothicPipeline
        else:
            current_pipeline = DefaultPipeline
        return current_pipeline

    def analyze(self, text: str) -> Doc:
        """The primary method for the NLP object, to which raw text strings are passed.

        TODO: Run the OF example and then log the FileNotFoundError inside the `stanford.py` module

        TODO: Add Gothic language ("got") to StanfordNLP

        >>> from cltkv1 import NLP
        >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
        >>> from cltkv1.utils.data_types import Doc
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_obj = cltk_nlp.analyze(text=EXAMPLE_TEXTS["lat"])
        >>> isinstance(cltk_obj, Doc)
        True
        >>> cltk_obj.words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Gallia', pos='A1|grn1|casA|gen2|stAM', lemma='aallius', scansion=None, xpos='A1|grn1|casA|gen2|stAM', upos='NOUN', dependency_relation='nsubj', governor=4, parent_token=<Token index=1;words=[<Word index=1;text=Gallia;lemma=aallius;upos=NOUN;xpos=A1|grn1|casA|gen2|stAM;feats=Case=Nom|Degree=Pos|Gender=Fem|Number=Sing;governor=4;dependency_relation=nsubj>]>, feats='Case=Nom|Degree=Pos|Gender=Fem|Number=Sing')

        >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
        >>> cltk_nlp = NLP(language="grc")
        >>> cltk_obj = cltk_nlp.analyze(text=EXAMPLE_TEXTS["grc"])
        >>> cltk_obj.words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='ὅτι', pos='Df', lemma='ὅτι#1', scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=13, parent_token=<Token index=1;words=[<Word index=1;text=ὅτι;lemma=ὅτι#1;upos=ADV;xpos=Df;feats=_;governor=13;dependency_relation=advmod>]>, feats='_')

        >>> cltk_nlp = NLP(language="chu")
        >>> cltk_obj = cltk_nlp.analyze(text=EXAMPLE_TEXTS["chu"])
        >>> cltk_obj.words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='отьчє', pos='Nb', lemma='отьць', scansion=None, xpos='Nb', upos='NOUN', dependency_relation='nsubj', governor=6, parent_token=<Token index=1;words=[<Word index=1;text=отьчє;lemma=отьць;upos=NOUN;xpos=Nb;feats=Case=Nom|Gender=Masc|Number=Sing;governor=6;dependency_relation=nsubj>]>, feats='Case=Nom|Gender=Masc|Number=Sing')

        >>> cltk_nlp = NLP(language="fro")
        >>> cltk_obj = cltk_nlp.analyze(text=EXAMPLE_TEXTS["fro"])
        >>> cltk_obj.words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='Une', pos='DETndf', lemma='Une', scansion=None, xpos='DETndf', upos='DET', dependency_relation='det', governor=2, parent_token=<Token index=1;words=[<Word index=1;text=Une;lemma=Une;upos=DET;xpos=DETndf;feats=Definite=Ind|PronType=Art;governor=2;dependency_relation=det>]>, feats='Definite=Ind|PronType=Art')

        >>> cltk_nlp = NLP(language="got")
        >>> cltk_obj = cltk_nlp.analyze(text=EXAMPLE_TEXTS["got"])
        >>> cltk_obj.words[0]
        Word(index_char_start=None, index_char_stop=None, index_token=1, index_sentence=0, string='swa', pos='Df', lemma='swa', scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=2, parent_token=<Token index=1;words=[<Word index=1;text=swa;lemma=swa;upos=ADV;xpos=Df;feats=_;governor=2;dependency_relation=advmod>]>, feats='_')
        """
        # TODO: Figure out if I can avoid having to call the dataclass Pipeline
        a_pipeline = self.pipeline()
        doc = Doc(language=self.language.iso_639_3_code)
        for process in a_pipeline.processes:
            process_stanford = process(
                data_input=text, language=self.language.iso_639_3_code
            )
            cltk_words = process_stanford.words

            # TODO: Write fn which annotates ``doc.words``, not just writing over what is in there
            doc = Doc(language=self.language.iso_639_3_code, words=cltk_words)

        return doc
