"""Wrapper for the Python StanfordNLP package ``stanfordnlp``.
About: https://github.com/stanfordnlp/stanfordnlp.
"""

import os
from typing import Dict, Optional

import stanfordnlp  # type: ignore
from cltkv1.utils import UnknownLanguageError, file_exists, suppress_stdout


class StanfordNLPWrapper:
    """CLTK's wrapper for the StanfordNLP project."""

    def __init__(self, language: str, treebank: Optional[str] = None) -> None:
        """Constructor for ``stanford`` wrapper class.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        >>> isinstance(stanford_wrapper, StanfordNLPWrapper)
        True
        >>> stanford_wrapper.language
        'greek'
        >>> stanford_wrapper.treebank
        'grc_proiel'

        >>> stanford_wrapper_perseus = StanfordNLPWrapper(language='greek', treebank='grc_perseus')
        >>> isinstance(stanford_wrapper_perseus, StanfordNLPWrapper)
        True
        >>> stanford_wrapper_perseus.language
        'greek'
        >>> stanford_wrapper_perseus.treebank
        'grc_perseus'

        >>> xen_anab = "Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι."
        >>> xen_anab_nlp = stanford_wrapper.parse(xen_anab)

        >>> stanford_nlp_obj_bad = StanfordNLPWrapper(language='BADLANG')
        Traceback (most recent call last):
          ...
        cltkv1.utils.exceptions.UnknownLanguageError: Language 'BADLANG' either not in scope for CLTK or not supported by StanfordNLP.
        """
        self.language = language
        self.treebank = treebank

        # Setup language
        self.map_langs_cltk_stanford = dict(
            greek="Ancient_Greek",
            latin="Latin",
            old_church_slavonic="Old_Church_Slavonic",
            old_french="Old_French",
        )

        self.wrapper_available = self.is_wrapper_available()  # type: bool
        if not self.wrapper_available:
            raise UnknownLanguageError(
                "Language '{}' either not in scope for CLTK or not supported by StanfordNLP.".format(
                    self.language
                )
            )
        self.stanford_code = self._get_stanford_code()

        # Setup optional treebank if specified
        self.map_code_treebanks = dict(
            grc=["grc_proiel", "grc_perseus"], la=["la_perseus", "la_proiel"]
        )
        # if not specified, will use the default treebank of stanfordnlp
        if self.treebank:
            valid_treebank = self._is_valid_treebank()
            if not valid_treebank:
                raise UnknownLanguageError(
                    "Invalid treebank '{0}' for language '{1}'.".format(
                        self.treebank, self.language
                    )
                )
        else:
            self.treebank = self._get_default_treebank()

        # check if model present
        # this fp is just to confirm that some model has already been downloaded. This is a weak check for the models actually being downloaded and valid
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
        """Run all ``stanfordnlp`` parsing on input text.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        >>> xen_anab = "Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι."
        >>> xen_anab_nlp = stanford_wrapper.parse(xen_anab)
        >>> isinstance(xen_anab_nlp, stanfordnlp.pipeline.doc.Document)
        True

        >>> nlp_xen_anab_first_sent = xen_anab_nlp.sentences[0]
        >>> nlp_xen_anab_first_sent.tokens[0].index
        '1'
        >>> nlp_xen_anab_first_sent.tokens[0].text
        'Δαρείου'
        >>> first_word = nlp_xen_anab_first_sent.tokens[0].words[0]
        >>> first_word.dependency_relation
        'iobj'
        >>> first_word.feats
        'Case=Gen|Gender=Masc|Number=Sing'
        >>> first_word.governor
        4
        >>> first_word.index
        '1'
        >>> first_word.lemma
        'Δαρεῖος'
        >>> first_word.pos
        'Ne'
        >>> first_word.text
        'Δαρείου'
        >>> first_word.upos
        'PROPN'
        >>> first_word.xpos
        'Ne'
        """
        parsed_text = self.nlp(text)
        return parsed_text

    def _load_pipeline(self):
        """Instantiate `stanfordnlp.Pipeline()`.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        >>> with suppress_stdout():    nlp_obj = stanford_wrapper._load_pipeline()
        >>> isinstance(nlp_obj, stanfordnlp.pipeline.core.Pipeline)
        True
        """
        models_dir = os.path.expanduser("~/stanfordnlp_resources/")
        nlp = stanfordnlp.Pipeline(
            processors="tokenize,mwt,pos,lemma,depparse",  # these are the default processors
            lang=self.stanford_code,
            models_dir=models_dir,
            treebank=self.treebank,
            use_gpu=True,  # default, won't fail if GPU not present
        )
        return nlp

    def _is_model_present(self) -> bool:
        """Checks if the model is already downloaded.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        >>> stanford_wrapper._is_model_present()
        True
        """
        if file_exists(self.model_path):
            return True
        else:
            return False

    def _download_model(self):
        """Interface with the `stanfordnlp` model downloader.

        TODO: Figure out why doctests here hang. Presumably because waiting for user input, but prompt shouldn't arise if models already present.

        # >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        # >>> stanford_wrapper._download_model()
        # True
        """
        # prompt user to DL the stanford models
        print("")
        print("")
        print("Α" * 80)
        print("")
        print(
            "CLTK message: The part of the CLTK that you are using depends upon the Stanford NLP library (`stanfordnlp`). What follows are several question prompts coming from it. (More at: <https://github.com/stanfordnlp/stanfordnlp>.) Answer with defaults."
        )
        print("")
        print("Ω" * 80)
        print("")
        print("")
        stanfordnlp.download(self.treebank)
        # if file model still not available after attempted DL, then raise error
        if not file_exists(self.model_path):
            raise FileNotFoundError(
                "Missing required models for `stanfordnlp` at `{0}`.".format(
                    self.model_path
                )
            )
        pass

    def _get_default_treebank(self) -> str:
        """Return name of a language's default treebank if none
        supplied.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
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

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek', treebank='grc_proiel')
        >>> stanford_wrapper._is_valid_treebank()
        True
        """
        possible_treebanks = self.map_code_treebanks[self.stanford_code]
        if self.treebank in possible_treebanks:
            return True
        else:
            return False

    def is_wrapper_available(self) -> bool:
        """Maps CLTK's internal language term (e.g., ``latin``) to
        that used by ``stanfordnlp`` (``la``); confirms that this is
        a language the CLTK supports (i.e., is it pre-modern or not).

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
        >>> stanford_wrapper.is_wrapper_available()
        True
        """
        if self.language in self.map_langs_cltk_stanford:
            return True
        else:
            return False

    def _get_stanford_code(self) -> str:
        """Using known-supported language, use the CLTK's
        internal code to look up the code used by StanfordNLP.

        >>> stanford_wrapper = StanfordNLPWrapper(language='greek')
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


if __name__ == "__main__":

    stanford_nlp_obj = StanfordNLPWrapper(language="latin")
    print(stanford_nlp_obj.language == "latin")

    stanford_nlp_obj = StanfordNLPWrapper(language="greek", treebank="grc_perseus")
    print(stanford_nlp_obj.language == "greek")
    print(stanford_nlp_obj.treebank == "grc_perseus")
    print(stanford_nlp_obj.wrapper_available == True)

    stanford_nlp_obj = StanfordNLPWrapper(language="greek")
    print(stanford_nlp_obj.language == "greek")
    print(stanford_nlp_obj.treebank == "grc_proiel")
    print(stanford_nlp_obj.wrapper_available == True)
    fp_model = stanford_nlp_obj.model_path
    print(os.path.split(fp_model)[1] == "grc_proiel_tokenizer.pt")
    print(isinstance(stanford_nlp_obj.nlp, stanfordnlp.pipeline.core.Pipeline))

    xen_anab = "Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι."
    xen_anab_nlp = stanford_nlp_obj.parse(xen_anab)

    nlp_xen_anab_first_sent = xen_anab_nlp.sentences[0]
    # print(dir(nlp_xen_anab_first_sent))  # build_dependencies', 'dependencies', 'print_dependencies', 'print_tokens', 'print_words', 'tokens', 'words'
    print(nlp_xen_anab_first_sent.tokens[0].index == "1")
    print(nlp_xen_anab_first_sent.tokens[0].text == "Δαρείου")
    first_word = nlp_xen_anab_first_sent.tokens[0].words[
        0
    ]  # 'dependency_relation', 'feats', 'governor', 'index', 'lemma', 'parent_token', 'pos', 'text', 'upos', 'xpos'
    print(first_word.dependency_relation == "iobj")
    print(first_word.feats == "Case=Gen|Gender=Masc|Number=Sing")
    print(first_word.governor == 4)
    print(first_word.index == "1")
    print(first_word.lemma == "Δαρεῖος")
    print(first_word.pos == "Ne")
    print(first_word.text == "Δαρείου")
    print(first_word.upos == "PROPN")
    print(first_word.xpos == "Ne")
    # print(first_word.parent_token)  # <Token index=1;words=[<Word index=1;text=Δαρείου;lemma=Δαρεῖος;upos=PROPN;xpos=Ne;feats=Case=Gen|Gender=Masc|Number=Sing;governor=4;dependency_relation=iobj>]>

    try:
        stanford_nlp_obj_bad = StanfordNLPWrapper(language="FAKELANG")
    except UnknownLanguageError as err:
        print(isinstance(err, UnknownLanguageError))
