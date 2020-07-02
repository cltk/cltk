"""Primary module for CLTK pipeline.

.. graphviz::

   digraph foo {
      "bar" -> "baz";
   }

"""

from cltk.core.data_types import Doc, Language, Pipeline
from cltk.core.exceptions import UnimplementedAlgorithmError
from cltk.languages.pipelines import (
    AkkadianPipeline,
    ArabicPipeline,
    AramaicPipeline,
    ChinesePipeline,
    CopticPipeline,
    GothicPipeline,
    GreekPipeline,
    HindiPipeline,
    LatinPipeline,
    MHGPipeline,
    MiddleEnglishPipeline,
    MiddleFrenchPipeline,
    OCSPipeline,
    OldEnglishPipeline,
    OldFrenchPipeline,
    OldNorsePipeline,
    PaliPipeline,
    PanjabiPipeline,
    SanskritPipeline,
)
from cltk.languages.utils import get_lang

iso_to_pipeline = {
    "akk": AkkadianPipeline,
    "ang": OldEnglishPipeline,
    "arb": ArabicPipeline,
    "arc": AramaicPipeline,
    "chu": OCSPipeline,
    "cop": CopticPipeline,
    "enm": MiddleEnglishPipeline,
    "frm": MiddleFrenchPipeline,
    "fro": OldFrenchPipeline,
    "gmh": MHGPipeline,
    "got": GothicPipeline,
    "grc": GreekPipeline,
    "hin": HindiPipeline,
    "lat": LatinPipeline,
    "lzh": ChinesePipeline,
    "non": OldNorsePipeline,
    "pan": PanjabiPipeline,
    "pli": PaliPipeline,
    "san": SanskritPipeline,
}


class NLP:
    """NLP class for default processing."""

    def __init__(self, language: str, custom_pipeline: Pipeline = None) -> None:
        """Constructor for CLTK class.

        Args:
            language: ISO code
            custom_pipeline: Optional ``Pipeline`` for processing text.


        >>> from cltk import NLP
        >>> cltk_nlp = NLP(language="lat")
        >>> isinstance(cltk_nlp, NLP)
        True
        >>> from cltk.core.data_types import Pipeline
        >>> from cltk.tokenizers import LatinTokenizationProcess
        >>> from cltk.languages.utils import get_lang
        >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess], language=get_lang("lat"))
        >>> nlp = NLP(language="lat", custom_pipeline=a_pipeline)
        >>> nlp.pipeline is a_pipeline
        True
        """
        self.language = get_lang(language)  # type: Language
        self.pipeline = custom_pipeline if custom_pipeline else self._get_pipeline()

    def analyze(self, text: str) -> Doc:
        """The primary method for the NLP object, to which raw text strings are passed.

        Args:
            text: Input text string.

        Returns:
            CLTK ``Doc`` containing all processed information.

        >>> from cltk import NLP
        >>> from cltk.languages.example_texts import get_example_text
        >>> from cltk.core.data_types import Doc
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> isinstance(cltk_doc, Doc)
        True
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos='NOUN', lemma='mallis', scansion=None, xpos='A1|grn1|casA|gen2', upos='NOUN', dependency_relation='nsubj', governor=3, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=..., stop=False, named_entity=True)
        """
        doc = Doc(language=self.language.iso_639_3_code, raw=text)

        for process in self.pipeline.processes:
            a_process = process(input_doc=doc, language=self.language.iso_639_3_code)
            a_process.run()
            doc = a_process.output_doc

        return doc

    def _get_pipeline(self) -> Pipeline:
        """Select appropriate pipeline for given language. If custom
        processing is requested, ensure that user-selected choices
        are valid, both in themselves and in unison.

        >>> from cltk import NLP
        >>> from cltk.core.data_types import Pipeline
        >>> cltk_nlp = NLP(language="lat")
        >>> lat_pipeline = cltk_nlp._get_pipeline()
        >>> isinstance(cltk_nlp.pipeline, Pipeline)
        True
        >>> isinstance(lat_pipeline, Pipeline)
        True
        >>> cltk_nlp = NLP(language="axm")
        Traceback (most recent call last):
          ...
        cltk.core.exceptions.UnimplementedAlgorithmError: Valid ISO language code, however this algorithm is not available for ``axm``.
        """
        try:
            return iso_to_pipeline[self.language.iso_639_3_code]()
        except KeyError:
            raise UnimplementedAlgorithmError(
                f"Valid ISO language code, however this algorithm is not available for ``{self.language.iso_639_3_code}``."
            )

    def __call__(self, text: str) -> Doc:
        return self.analyze(text)


if __name__ == "__main__":
    from cltk.languages.example_texts import get_example_text

    langs = [
        "lat",
        # "grc",
        # "got",
        # "arb",
        # "arc",
        # "pli",
        # "san",
        # "ang",
        # "akk",  # TODO: turn List[Tuple[str, str]] into List[str]
        # "non",
        # "gmh",
        # "fro",
        # "frm",
        # "enm",
        # "pan",
        # "hin",
    ]
    for lang in langs:
        cltk_nlp = NLP(language=lang)
        print(f"Did NLP() for {lang} load fast? It should.")
        example_text = get_example_text(iso_code=lang)
        print(example_text[:50])
        cltk_doc = cltk_nlp.analyze(example_text)
        print(cltk_doc.tokens[:10])
        a_word = cltk_doc.words[4]
        # print(a_word)
        # input()
        print(a_word.string, a_word.index_token, a_word.embedding, a_word.pos)
        print(f"Done with {lang}.")
        # print(cltk_doc)
        print("")
