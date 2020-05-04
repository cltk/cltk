"""Primary module for CLTK pipeline."""

from cltkv1.core.data_types import Doc, Language, Pipeline
from cltkv1.core.exceptions import UnimplementedAlgorithmError
from cltkv1.languages.pipelines import (
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
from cltkv1.languages.utils import get_lang

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

        >>> from cltkv1 import NLP
        >>> cltk_nlp = NLP(language="lat")
        >>> isinstance(cltk_nlp, NLP)
        True
        >>> from cltkv1.core.data_types import Pipeline
        >>> from cltkv1.tokenizers import LatinTokenizationProcess
        >>> from cltkv1.languages.utils import get_lang
        >>> a_pipeline = Pipeline(description="A custom Latin pipeline", processes=[LatinTokenizationProcess], language=get_lang("lat"))
        >>> nlp = NLP(language="lat", custom_pipeline=a_pipeline)
        >>> nlp.pipeline is a_pipeline
        True
        """
        self.language = get_lang(language)  # type: Language
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
        cltkv1.core.exceptions.UnimplementedAlgorithmError: Valid ISO language code, however this algorithm is not available for ``axm``.
        """
        try:
            return iso_to_pipeline[self.language.iso_639_3_code]()
        except KeyError:
            raise UnimplementedAlgorithmError(
                f"Valid ISO language code, however this algorithm is not available for ``{self.language.iso_639_3_code}``."
            )

    def analyze(self, text: str) -> Doc:
        """The primary method for the NLP object, to which raw text strings are passed.

        >>> from cltkv1 import NLP
        >>> from cltkv1.languages.example_texts import get_example_text
        >>> from cltkv1.core.data_types import Doc
        >>> cltk_nlp = NLP(language="lat")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lat"))
        >>> isinstance(cltk_doc, Doc)
        True
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Gallia', pos='NOUN', lemma='mallis', scansion=None, xpos='A1|grn1|casA|gen2', upos='NOUN', dependency_relation='nsubj', governor=3, features={'Case': 'Nom', 'Degree': 'Pos', 'Gender': 'Fem', 'Number': 'Sing'}, embedding=..., stop=False, named_entity=True)

        >>> from cltkv1.languages.example_texts import get_example_text
        >>> cltk_nlp = NLP(language="grc")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("grc"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='ὅτι', pos='ADV', lemma='ὅτι', scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=6, features={}, embedding=..., stop=True, named_entity=False)

        >>> cltk_nlp = NLP(language="chu")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("chu"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='отьчє', pos='NOUN', lemma='отьць', scansion=None, xpos='Nb', upos='NOUN', dependency_relation='vocative', governor=7, features={'Case': 'Voc', 'Gender': 'Masc', 'Number': 'Sing'}, embedding=None, stop=None, named_entity=None)

        >>> cltk_nlp = NLP(language="fro")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("fro"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='Une', pos='DET', lemma=None, scansion=None, xpos='DETndf', upos='DET', dependency_relation=None, governor=-1, features={'Definite': 'Ind', 'PronType': 'Art'}, embedding=None, stop=False, named_entity=False)

        >>> cltk_nlp = NLP(language="got")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("got"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='swa', pos='ADV', lemma='swa', scansion=None, xpos='Df', upos='ADV', dependency_relation='advmod', governor=1, features={}, embedding=..., stop=None, named_entity=None)
        >>> len(cltk_doc.sentences)
        3

        >>> cltk_nlp = NLP(language="cop")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("cop"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='ⲧⲏⲛ', pos='VERB', lemma='ⲧⲏⲛ', scansion=None, xpos='VSTAT', upos='VERB', dependency_relation='root', governor=-1, features={'VerbForm': 'Fin'}, embedding=None, stop=None, named_entity=None)

        >>> cltk_nlp = NLP(language="lzh")
        >>> cltk_doc = cltk_nlp.analyze(text=get_example_text("lzh"))
        >>> cltk_doc.words[0] # doctest: +ELLIPSIS
        Word(index_char_start=None, index_char_stop=None, index_token=0, index_sentence=0, string='黃', pos='NOUN', lemma='黃', scansion=None, xpos='n,名詞,描写,形質', upos='NOUN', dependency_relation='nmod', governor=1, features={}, embedding=None, stop=None, named_entity=None)
        """
        doc = Doc(language=self.language.iso_639_3_code, raw=text)

        for process in self.pipeline.processes:
            a_process = process(input_doc=doc, language=self.language.iso_639_3_code)
            a_process.run()
            doc = a_process.output_doc

        return doc

    def __call__(self, text: str) -> Doc:
        return self.analyze(text)


if __name__ == "__main__":
    from cltkv1.languages.example_texts import get_example_text

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
