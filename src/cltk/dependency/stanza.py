"""Wrapper for the Python Stanza package.
About: `<https://github.com/stanfordnlp/stanza>`_.
"""

import logging
import os
from typing import Dict, Optional

import stanza  # type: ignore
from stanza.models.common.constant import lang2lcode  # Dict[str, str]
from stanza.resources.prepare_resources import default_treebanks  # Dict[str, str]

from cltk.core.exceptions import (
    CLTKException,
    UnimplementedAlgorithmError,
    UnknownLanguageError,
)
from cltk.utils import file_exists, query_yes_no, suppress_stdout

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


MAP_LANGS_CLTK_STANZA = {
    "chu": "Old_Church_Slavonic",
    "cop": "Coptic",
    "fro": "Old_French",
    "grc": "Ancient_Greek",
    "got": "Gothic",
    "lat": "Latin",
    "lzh": "Classical_Chinese",
}


class StanzaWrapper:
    """CLTK's wrapper for the Stanza project."""

    nlps = {}

    def __init__(
        self,
        language: str,
        treebank: Optional[str] = None,
        stanza_debug_level="ERROR",
        interactive: bool = True,
        silent: bool = False,
    ) -> None:
        """Constructor for ``get_stanza_models`` wrapper class.

        >>> stanza_wrapper = StanzaWrapper(language="grc", stanza_debug_level="INFO", interactive=False, silent=True)
        >>> isinstance(stanza_wrapper, StanzaWrapper)
        True
        >>> stanza_wrapper.language
        'grc'
        >>> stanza_wrapper.treebank
        'proiel'

        >>> stanza_wrapper = StanzaWrapper(language="grc", treebank="perseus", stanza_debug_level="INFO", interactive=False, silent=True)
        >>> isinstance(stanza_wrapper, StanzaWrapper)
        True
        >>> stanza_wrapper.language
        'grc'
        >>> stanza_wrapper.treebank
        'perseus'
        >>> from cltk.languages.example_texts import get_example_text
        >>> stanza_doc = stanza_wrapper.parse(get_example_text("grc"))

        >>> StanzaWrapper(language="xxx", stanza_debug_level="INFO", interactive=False, silent=True)
        Traceback (most recent call last):
          ...
        cltk.core.exceptions.UnknownLanguageError: Language 'xxx' either not in scope for CLTK or not supported by Stanza.

        >>> stanza_wrapper = StanzaWrapper(language="grc", treebank="proiel", stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_doc = stanza_wrapper.parse(get_example_text("grc"))

        >>> stanza_wrapper = StanzaWrapper(language="lat", treebank="perseus", stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_doc = stanza_wrapper.parse(get_example_text("lat"))

        >>> stanza_wrapper = StanzaWrapper(language="lat", treebank="proiel", stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_doc = stanza_wrapper.parse(get_example_text("lat"))

        >>> stanza_wrapper = StanzaWrapper(language="chu", stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_doc = stanza_wrapper.parse(get_example_text("chu"))

        >>> stanza_wrapper = StanzaWrapper(language="cop", stanza_debug_level="INFO", interactive=False, silent=True)  # doctest: +SKIP
        >>> stanza_doc = stanza_wrapper.parse(get_example_text("cop"))  # doctest: +SKIP

        >>> stanza_wrapper = StanzaWrapper(language="lzh", stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_doc = stanza_wrapper.parse(get_example_text("lzh"))

        >>> stanza_wrapper = StanzaWrapper(language="lat", treebank="xxx", stanza_debug_level="INFO", interactive=False, silent=True)
        Traceback (most recent call last):
          ...
        cltk.core.exceptions.UnimplementedAlgorithmError: Invalid treebank 'xxx' for language 'lat'.
        """
        self.language = language
        self.treebank = treebank
        self.stanza_debug_level = stanza_debug_level
        self.interactive = interactive
        self.silent = silent

        if self.interactive and self.silent:
            raise ValueError(
                "``interactive`` and ``silent`` options are not compatible with each other."
            )

        self.wrapper_available = self.is_wrapper_available()  # type: bool
        if not self.wrapper_available:
            raise UnknownLanguageError(
                "Language '{}' either not in scope for CLTK or not supported by Stanza.".format(
                    self.language
                )
            )
        self.stanza_code = self._get_stanza_code()

        # Setup optional treebank if specified
        # TODO: Write tests for all treebanks
        self.map_code_treebanks = dict(
            grc=["proiel", "perseus"], la=["perseus", "proiel", "ittb"]
        )
        # if not specified, will use the default treebank chosen by stanza
        if self.treebank:
            valid_treebank = self._is_valid_treebank()
            if not valid_treebank:
                raise UnimplementedAlgorithmError(
                    f"Invalid treebank '{self.treebank}' for language '{self.language}'."
                )
        else:
            self.treebank = self._get_default_treebank()

        # check if model present
        # this fp is just to confirm that some model has already been downloaded.
        # TODO: This is a weak check for the models actually being downloaded and valid
        # TODO: Use ``models_dir`` var from below and make self. or global to module
        self.model_path = os.path.expanduser(
            f"~/stanza_resources/{self.stanza_code}/tokenize/{self.treebank}.pt"
        )
        if not self._is_model_present():
            # download model if necessary
            self._download_model()

        # instantiate actual stanza class
        # Note: `suppress_stdout` is used to prevent `stanza`
        # from printing a long log of its parameters to screen.
        # Though we should capture these, within `_load_pipeline()`,
        # for the log file.
        with suppress_stdout():
            self.nlp = self._load_pipeline()

    def parse(self, text: str):
        """Run all available ``stanza`` parsing on input text.

        >>> from cltk.languages.example_texts import get_example_text
        >>> stanza_wrapper = StanzaWrapper(language='grc', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> greek_nlp = stanza_wrapper.parse(get_example_text("grc"))
        >>> from stanza.models.common.doc import Document, Token
        >>> isinstance(greek_nlp, Document)
        True

        >>> nlp_greek_first_sent = greek_nlp.sentences[0]
        >>> isinstance(nlp_greek_first_sent.tokens[0], Token)
        True
        >>> nlp_greek_first_sent.tokens[0].text
        'ὅτι'
        >>> nlp_greek_first_sent.tokens[0].words
        [{
          "id": 1,
          "text": "ὅτι",
          "lemma": "ὅτι",
          "upos": "ADV",
          "xpos": "Df",
          "head": 13,
          "deprel": "advmod",
          "start_char": 0,
          "end_char": 3
        }]
        >>> nlp_greek_first_sent.tokens[0].start_char
        0
        >>> nlp_greek_first_sent.tokens[0].end_char
        3
        >>> nlp_greek_first_sent.tokens[0].misc
        >>> nlp_greek_first_sent.tokens[0].pretty_print()
        '<Token id=1;words=[<Word id=1;text=ὅτι;lemma=ὅτι;upos=ADV;xpos=Df;head=13;deprel=advmod>]>'
        >>> nlp_greek_first_sent.tokens[0].to_dict()
        [{'id': 1, 'text': 'ὅτι', 'lemma': 'ὅτι', 'upos': 'ADV', 'xpos': 'Df', 'head': 13, 'deprel': 'advmod', 'start_char': 0, 'end_char': 3}]

        >>> first_word = nlp_greek_first_sent.tokens[0].words[0]
        >>> first_word.id
        1
        >>> first_word.text
        'ὅτι'
        >>> first_word.lemma
        'ὅτι'
        >>> first_word.upos
        'ADV'
        >>> first_word.xpos
        'Df'
        >>> first_word.feats
        >>> first_word.head
        13
        >>> first_word.parent
        [
          {
            "id": 1,
            "text": "ὅτι",
            "lemma": "ὅτι",
            "upos": "ADV",
            "xpos": "Df",
            "head": 13,
            "deprel": "advmod",
            "start_char": 0,
            "end_char": 3
          }
        ]
        >>> first_word.misc
        >>> first_word.deprel
        'advmod'
        >>> first_word.pos
        'ADV'
        """
        parsed_text = self.nlp(text)
        return parsed_text

    def _load_pipeline(self):
        """Instantiate ``stanza.Pipeline()``.

        TODO: Make sure that logging captures what it should from the default stanza printout.
        TODO: Make note that full lemmatization is not possible for Old French

        >>> stanza_wrapper = StanzaWrapper(language='grc', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> with suppress_stdout():    nlp_obj = stanza_wrapper._load_pipeline()
        >>> isinstance(nlp_obj, stanza.pipeline.core.Pipeline)
        True
        >>> stanza_wrapper = StanzaWrapper(language='fro', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> with suppress_stdout():    nlp_obj = stanza_wrapper._load_pipeline()
        >>> isinstance(nlp_obj, stanza.pipeline.core.Pipeline)
        True
        """
        models_dir = os.path.expanduser(
            "~/stanza_resources/"
        )  # TODO: Mv this a self. var or maybe even global
        processors = "tokenize,mwt,pos,lemma,depparse"
        lemma_use_identity = False
        if self.language == "fro":
            processors = "tokenize,pos,lemma,depparse"
            lemma_use_identity = True
        if self.language in ["chu", "got", "grc", "lzh"]:
            # Note: MWT not available for several languages
            processors = "tokenize,pos,lemma,depparse"
        nlp = stanza.Pipeline(
            lang=self.stanza_code,
            dir=models_dir,
            package=self.treebank,
            processors=processors,  # these are the default processors
            logging_level=self.stanza_debug_level,
            use_gpu=True,  # default, won't fail if GPU not present
            lemma_use_identity=lemma_use_identity,
        )
        return nlp

    def _is_model_present(self) -> bool:
        """Checks if the model is already downloaded.

        >>> stanza_wrapper = StanzaWrapper(language='grc', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_wrapper._is_model_present()
        True
        """
        if file_exists(self.model_path):
            return True
        return False

    def _download_model(self) -> None:
        """Interface with the `stanza` model downloader."""
        if not self.interactive:
            if not self.silent:
                print(
                    f"CLTK message: Going to download required Stanza models to ``{self.model_path}`` ..."
                )  # pragma: no cover
            stanza.download(lang=self.stanza_code, package=self.treebank)
        else:
            print(  # pragma: no cover
                "CLTK message: This part of the CLTK depends upon the Stanza NLP library."
            )  # pragma: no cover
            dl_is_allowed = query_yes_no(
                f"CLTK message: Allow download of Stanza models to ``{self.model_path}``?"
            )  # type: bool
            if dl_is_allowed:
                stanza.download(lang=self.stanza_code, package=self.treebank)
            else:
                raise CLTKException(
                    f"Download of necessary Stanza model declined for '{self.language}'. Unable to continue with Stanza's processing."
                )
        # if file model still not available after attempted DL, then raise error
        if not file_exists(self.model_path):
            raise FileNotFoundError(
                "Missing required models for ``stanza`` at ``{0}``.".format(
                    self.model_path
                )
            )

    def _get_default_treebank(self) -> str:
        """Return description of a language's default treebank if none
        supplied.

        >>> stanza_wrapper = StanzaWrapper(language='grc', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_wrapper._get_default_treebank()
        'proiel'
        """
        stanza_default_treebanks = default_treebanks  # type: Dict[str, str]
        return stanza_default_treebanks[self.stanza_code]

    def _is_valid_treebank(self) -> bool:
        """Check whether for chosen language, optional
        treebank value is valid.

        >>> stanza_wrapper = StanzaWrapper(language='grc', treebank='proiel', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_wrapper._is_valid_treebank()
        True
        """
        possible_treebanks = self.map_code_treebanks[self.stanza_code]
        if self.treebank in possible_treebanks:
            return True
        return False

    def is_wrapper_available(self) -> bool:
        """Maps an ISO 639-3 language id (e.g., ``lat`` for Latin) to
        that used by ``stanza`` (``la``); confirms that this is
        a language the CLTK supports (i.e., is it pre-modern or not).

        >>> stanza_wrapper = StanzaWrapper(language='grc', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_wrapper.is_wrapper_available()
        True
        """
        if self.language in MAP_LANGS_CLTK_STANZA:
            return True
        return False

    def _get_stanza_code(self) -> str:
        """Using known-supported language, use the CLTK's
        internal code to look up the code used by Stanza.

        >>> stanza_wrapper = StanzaWrapper(language='grc', stanza_debug_level="INFO", interactive=False, silent=True)
        >>> stanza_wrapper._get_stanza_code()
        'grc'
        >>> stanza_wrapper.language = "xxx"
        >>> stanza_wrapper._get_stanza_code()
        Traceback (most recent call last):
          ...
        KeyError: 'Somehow ``StanzaWrapper.language`` got renamed to something invalid. This should never happen.'
        """
        try:
            stanza_lang_name = MAP_LANGS_CLTK_STANZA[self.language]
        except KeyError:
            raise KeyError(
                "Somehow ``StanzaWrapper.language`` got renamed to something invalid. This should never happen."
            )
        # {'Afrikaans': 'af', 'Ancient_Greek': 'grc', ...}
        stanza_lang_code: Dict[str, str] = lang2lcode
        try:
            return stanza_lang_code[stanza_lang_name]
        except KeyError:
            raise KeyError("The CLTK's map of ISO-to-Stanza is out of sync.")

    @classmethod
    def get_nlp(cls, language: str, treebank: Optional[str] = None):
        if language in cls.nlps:
            return cls.nlps[language]
        else:
            nlp = cls(language, treebank)
            cls.nlps[language] = nlp
            return nlp
