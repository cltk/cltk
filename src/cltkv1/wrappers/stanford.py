"""Wrapper for the Python StanfordNLP package.
About: https://github.com/stanfordnlp/stanfordnlp.
"""

import logging
import os
from typing import Dict, Optional

import stanfordnlp  # type: ignore

from cltkv1.utils import (
    UnimplementedLanguageError,
    UnknownLanguageError,
    example_texts,
    file_exists,
    suppress_stdout,
)
from cltkv1.utils.example_texts import EXAMPLE_TEXTS

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


class StanfordNLPWrapper:
    """CLTK's wrapper for the StanfordNLP project."""

    nlps = {}

    def __init__(self, language: str, treebank: Optional[str] = None) -> None:
        """Constructor for ``get_stanfordnlp_models`` wrapper class.

        TODO: Do tests for all langs and available models for each

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        >>> isinstance(stanford_wrapper, StanfordNLPWrapper)
        True
        >>> stanford_wrapper.language
        'grc'
        >>> stanford_wrapper.treebank
        'grc_proiel'

        >>> stanford_wrapper = StanfordNLPWrapper(language="grc", treebank="grc_perseus")
        >>> isinstance(stanford_wrapper, StanfordNLPWrapper)
        True
        >>> stanford_wrapper.language
        'grc'
        >>> stanford_wrapper.treebank
        'grc_perseus'
        >>> from cltkv1.utils.example_texts import EXAMPLE_TEXTS
        >>> snlp_doc = stanford_wrapper.parse(EXAMPLE_TEXTS["grc"])

        >>> StanfordNLPWrapper(language="xxx")
        Traceback (most recent call last):
          ...
        cltkv1.utils.exceptions.UnknownLanguageError: Language 'xxx' either not in scope for CLTK or not supported by StanfordNLP.

        >>> stanford_wrapper = StanfordNLPWrapper(language="grc", treebank="grc_proiel")
        >>> snlp_doc = stanford_wrapper.parse(EXAMPLE_TEXTS["grc"])

        >>> stanford_wrapper = StanfordNLPWrapper(language="lat", treebank="la_perseus")
        >>> snlp_doc = stanford_wrapper.parse(EXAMPLE_TEXTS["lat"])

        >>> stanford_wrapper = StanfordNLPWrapper(language="lat", treebank="la_proiel")
        >>> snlp_doc = stanford_wrapper.parse(EXAMPLE_TEXTS["lat"])

        >>> stanford_wrapper = StanfordNLPWrapper(language="chu")
        >>> snlp_doc = stanford_wrapper.parse(EXAMPLE_TEXTS["chu"])
        """
        self.language = language
        self.treebank = treebank

        # Setup language
        self.map_langs_cltk_stanford = {
            "grc": "Ancient_Greek",
            "lat": "Latin",
            "chu": "Old_Church_Slavonic",
            "fro": "Old_French",
            "got": "Gothic",
        }

        self.wrapper_available = self.is_wrapper_available()  # type: bool
        if not self.wrapper_available:
            raise UnknownLanguageError(
                "Language '{}' either not in scope for CLTK or not supported by StanfordNLP.".format(
                    self.language
                )
            )
        self.stanford_code = self._get_stanford_code()

        # Setup optional treebank if specified
        # TODO: Write tests for all treebanks
        self.map_code_treebanks = dict(
            grc=["grc_proiel", "grc_perseus"], la=["la_perseus", "la_proiel", "la_ittb"]
        )
        # if not specified, will use the default treebank chosen by stanfordnlp
        if self.treebank:
            valid_treebank = self._is_valid_treebank()
            if not valid_treebank:
                raise UnimplementedLanguageError(
                    "Invalid treebank '{0}' for language '{1}'.".format(
                        self.treebank, self.language
                    )
                )
        else:
            self.treebank = self._get_default_treebank()

        # check if model present
        # this fp is just to confirm that some model has already been downloaded.
        # TODO: This is a weak check for the models actually being downloaded and valid
        # TODO: Use ``models_dir`` var from below and make self. or global to module
        self.model_path = os.path.expanduser(
            "~/stanfordnlp_resources/{0}_models/{0}_tokenizer.pt".format(self.treebank)
        )
        if not self._is_model_present():
            # download model if necessary
            self._download_model()

        # instantiate actual stanfordnlp class
        # Note: `suppress_stdout` is used to prevent `stanfordnlp`
        # from printing a long log of its parameters to screen.
        # Though we should capture these, within `_load_pipeline()`,
        # for the log file.
        with suppress_stdout():
            self.nlp = self._load_pipeline()

    def parse(self, text: str):
        """Run all available ``stanfordnlp`` parsing on input text.

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        >>> greek_nlp = stanford_wrapper.parse(EXAMPLE_TEXTS["grc"])
        >>> isinstance(greek_nlp, stanfordnlp.pipeline.doc.Document)
        True

        >>> nlp_greek_first_sent = greek_nlp.sentences[0]
        >>> nlp_greek_first_sent.tokens[0].index
        '1'
        >>> nlp_greek_first_sent.tokens[0].text
        'ὅτι'
        >>> first_word = nlp_greek_first_sent.tokens[0].words[0]
        >>> first_word.dependency_relation
        'advmod'
        >>> first_word.feats
        '_'
        >>> first_word.governor
        13
        >>> first_word.index
        '1'
        >>> first_word.lemma
        'ὅτι#1'
        >>> first_word.pos
        'Df'
        >>> first_word.text
        'ὅτι'
        >>> first_word.upos
        'ADV'
        >>> first_word.xpos
        'Df'
        """
        parsed_text = self.nlp(text)
        return parsed_text

    def _load_pipeline(self):
        """Instantiate ``stanfordnlp.Pipeline()``.

        TODO: Make sure that logging captures what it should from the default stanfordnlp printout.
        TODO: Make note that full lemmatization is not possible for Old French

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        >>> with suppress_stdout():    nlp_obj = stanford_wrapper._load_pipeline()
        >>> isinstance(nlp_obj, stanfordnlp.pipeline.core.Pipeline)
        True
        >>> stanford_wrapper = StanfordNLPWrapper(language='fro')
        >>> with suppress_stdout():    nlp_obj = stanford_wrapper._load_pipeline()
        >>> isinstance(nlp_obj, stanfordnlp.pipeline.core.Pipeline)
        True
        """
        models_dir = os.path.expanduser("~/stanfordnlp_resources/")
        # Note: To prevent FileNotFoundError (``~/stanfordnlp_resources/fro_srcmf_models/fro_srcmf_lemmatizer.pt``) for Old French
        # Background: https://github.com/stanfordnlp/stanfordnlp/issues/157
        lemma_use_identity = False
        if self.language == "fro":
            lemma_use_identity = True
        nlp = stanfordnlp.Pipeline(
            processors="tokenize,mwt,pos,lemma,depparse",  # these are the default processors
            lang=self.stanford_code,
            models_dir=models_dir,
            treebank=self.treebank,
            use_gpu=True,  # default, won't fail if GPU not present
            lemma_use_identity=lemma_use_identity,
        )
        return nlp

    def _is_model_present(self) -> bool:
        """Checks if the model is already downloaded.

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        >>> stanford_wrapper._is_model_present()
        True
        """
        if file_exists(self.model_path):
            return True
        return False

    def _download_model(self) -> None:
        """Interface with the `stanfordnlp` model downloader.

        TODO: (old) Figure out why doctests here hang. Presumably because waiting for user op_input, but prompt shouldn't arise if models already present.

        # >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        # >>> stanford_wrapper._download_model()
        # True
        """
        # prompt user to DL the get_stanfordnlp_models models
        print("")  # pragma: no cover
        print("")  # pragma: no cover
        print("Α" * 80)  # pragma: no cover
        print("")  # pragma: no cover
        print(  # pragma: no cover
            "CLTK message: The part of the CLTK that you are using depends upon the Stanford NLP library (`stanfordnlp`). What follows are several question prompts coming from it. (More at: <https://github.com/stanfordnlp/stanfordnlp>.) Answer with defaults."
        )  # pragma: no cover
        print("")  # pragma: no cover
        print("Ω" * 80)  # pragma: no cover
        print("")  # pragma: no cover
        print("")  # pragma: no cover
        stanfordnlp.download(self.treebank)
        # if file model still not available after attempted DL, then raise error
        if not file_exists(self.model_path):
            raise FileNotFoundError(
                "Missing required models for ``stanfordnlp`` at ``{0}``.".format(
                    self.model_path
                )
            )

    def _get_default_treebank(self) -> str:
        """Return description of a language's default treebank if none
        supplied.

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        >>> stanford_wrapper._get_default_treebank()
        'grc_proiel'
        """
        stanford_default_treebanks = (
            stanfordnlp.utils.resources.default_treebanks
        )  # type: Dict[str, str]
        return stanford_default_treebanks[self.stanford_code]

    def _is_valid_treebank(self) -> bool:
        """Check whether for chosen language, optional
        treebank value is valid.

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc', treebank='grc_proiel')
        >>> stanford_wrapper._is_valid_treebank()
        True
        >>> stanford_wrapper.language = "xxx"
        >>>
        """
        possible_treebanks = self.map_code_treebanks[self.stanford_code]
        if self.treebank in possible_treebanks:
            return True
        return False

    def is_wrapper_available(self) -> bool:
        """Maps an ISO 639-3 language id (e.g., ``lat`` for Latin) to
        that used by ``stanfordnlp`` (``la``); confirms that this is
        a language the CLTK supports (i.e., is it pre-modern or not).

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        >>> stanford_wrapper.is_wrapper_available()
        True
        """
        if self.language in self.map_langs_cltk_stanford:
            return True
        return False

    def _get_stanford_code(self) -> str:
        """Using known-supported language, use the CLTK's
        internal code to look up the code used by StanfordNLP.

        >>> stanford_wrapper = StanfordNLPWrapper(language='grc')
        >>> stanford_wrapper._get_stanford_code()
        'grc'
        """
        try:
            stanford_lang_name = self.map_langs_cltk_stanford[self.language]
        except KeyError:
            raise KeyError
        stanford_lang_code = (
            stanfordnlp.models.common.constant.lang2lcode
        )  # type: Dict[str, str]
        try:
            return stanford_lang_code[stanford_lang_name]
        except KeyError:
            raise KeyError

    @classmethod
    def get_nlp(cls, language: str, treebank: Optional[str] = None) -> stanfordnlp.Pipeline:
        if language in cls.nlps:
            return cls.nlps[language]
        else:
            nlp = cls(language, treebank)
            cls.nlps[language] = nlp
            return nlp
