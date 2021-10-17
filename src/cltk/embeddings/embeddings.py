"""Module for accessing pre-trained `fastText word embeddings
<https://fasttext.cc/>`_ and `Word2Vec embeddings from NLPL
<http://vectors.nlpl.eu/repository/>`_. Two sets of models are available
from fastText, one being trained only on corpora taken from
Wikipedia (`249 languages
<https://fasttext.cc/docs/en/pretrained-vectors.html>`_) and
the other being a combination of Wikipedia and Common Crawl
(`157 languages, a subset of the former
<https://fasttext.cc/docs/en/crawl-vectors.html>`_).

The Word2Vec models are in two versions, ``txt`` and ``bin``, with the
``txt`` being approximately twice the size and containing information
for retraining.

# TODO: Classes ``Word2VecEmbeddings`` and ``FastTextEmbeddings`` contain duplicative code. Consider combining them.

# TODO: Instead of returning `None`, return an empty numpy array of correct len.
"""

import os
from typing import List
from zipfile import ZipFile

from gensim import models  # type: ignore

from cltk.core.exceptions import CLTKException, UnimplementedAlgorithmError
from cltk.languages.utils import get_lang
from cltk.utils import CLTK_DATA_DIR, get_file_with_progress_bar, query_yes_no

MAP_NLPL_LANG_TO_URL = dict(
    arb="http://vectors.nlpl.eu/repository/20/31.zip",
    chu="http://vectors.nlpl.eu/repository/20/60.zip",
    grc="http://vectors.nlpl.eu/repository/20/30.zip",
    lat="http://vectors.nlpl.eu/repository/20/56.zip",
)

MAP_LANGS_CLTK_FASTTEXT = {
    "ang": "ang",  # Anglo-Saxon
    "arb": "ar",  # Arabic
    "arc": "arc",  # Aramaic
    "got": "got",  # Gothic
    "lat": "la",  # Latin
    "pli": "pi",  # Pali
    "san": "sa",  # Sanskrit
}


class Word2VecEmbeddings:
    """Wrapper for Word2Vec embeddings. Note: For models
    provided by fastText, use class ``FastTextEmbeddings``.
    """

    def __init__(
        self,
        iso_code: str,
        model_type: str = "txt",
        interactive: bool = True,
        silent: bool = False,
        overwrite: bool = False,
    ):
        """Constructor for  ``Word2VecEmbeddings`` class."""
        self.iso_code = iso_code
        self.model_type = model_type
        self.interactive = interactive
        self.silent = silent
        self.overwrite = overwrite

        if self.interactive and self.silent:
            raise ValueError(
                "``interactive`` and ``silent`` options are not compatible with each other."
            )

        self._check_input_params()

        # load model after all checks OK
        self.fp_zip = self._build_zip_filepath()
        self.fp_model = self._build_nlpl_filepath()
        self.fp_model_dirs = os.path.split(self.fp_zip)[0]  # type: str
        if not self._is_nlpl_model_present() or self.overwrite:
            self._download_nlpl_models()
            self._unzip_nlpl_model()
        elif self._is_nlpl_model_present() and not self.overwrite:
            # message = f"Model for '{self.iso_code}' / '{self.model_type}' already present at '{self.fp_model}' and ``overwrite=False``."
            # print(message)
            # TODO: Log message
            pass
        self.model: models.keyedvectors.Word2VecKeyedVectors = self._load_model()

    def get_word_vector(self, word: str):
        """Return embedding array."""
        try:
            return self.model.get_vector(word)
        except KeyError:
            return None

    def get_embedding_length(self) -> int:
        """Return the embedding length for selected model."""
        return self.model.vector_size

    def get_sims(self, word: str):
        """Get similar words."""
        return self.model.most_similar(word)

    def _check_input_params(self) -> None:
        """Confirm that input parameters are valid and in a
        valid configuration.
        """
        # 1. check if lang valid
        get_lang(self.iso_code)  # check if iso_code valid

        # 2. check if any fasttext embeddings for this lang
        if self.iso_code not in MAP_NLPL_LANG_TO_URL:
            available_embeddings_str = "', '".join(MAP_NLPL_LANG_TO_URL.keys())
            raise UnimplementedAlgorithmError(
                f"No embedding available for language '{self.iso_code}'. Word2Vec models available for: '{available_embeddings_str}'."
            )

        # 3. assert that model type is valid
        valid_types = ["bin", "txt"]
        if self.model_type not in valid_types:
            unavailable_types_str = "', '".join(valid_types)
            raise ValueError(
                f"Invalid ``model_type`` {self.model_type}. Valid model types: {unavailable_types_str}."
            )

    def _build_zip_filepath(self) -> str:
        """Create filepath where .zip file will be saved."""
        url_frag = MAP_NLPL_LANG_TO_URL[self.iso_code].split(".")[-2]  # type: str
        nlpl_id = int(url_frag.split("/")[-1])  # str
        fp_zip = os.path.join(
            CLTK_DATA_DIR, f"{self.iso_code}/embeddings/nlpl/{nlpl_id}.zip"
        )  # type: str
        return fp_zip

    def _build_nlpl_filepath(self) -> str:
        """Create filepath where chosen language should be found."""
        model_dir = os.path.join(
            CLTK_DATA_DIR, f"{self.iso_code}/embeddings/nlpl/"
        )  # type: str
        return os.path.join(model_dir, f"model.{self.model_type}")

    def _is_nlpl_model_present(self) -> bool:
        """Check if model in an otherwise valid filepath."""

        if os.path.isfile(self.fp_model):
            return True
        else:
            return False

    def _download_nlpl_models(self) -> None:
        """Perform complete download of Word2Vec models and save
        them in appropriate ``cltk_data`` dir.
        """
        model_url = MAP_NLPL_LANG_TO_URL[self.iso_code]
        if not self.interactive:
            if not self.silent:
                print(
                    f"CLTK message: Going to download file '{model_url}' to '{self.fp_zip} ..."
                )  # pragma: no cover
            get_file_with_progress_bar(model_url=model_url, file_path=self.fp_zip)
        else:
            print(  # pragma: no cover
                "CLTK message: This part of the CLTK depends upon word embedding models from the NLPL project."
            )  # pragma: no cover
            dl_is_allowed = query_yes_no(
                f"Do you want to download file '{model_url}' to '{self.fp_zip}'?"
            )  # type: bool
            if dl_is_allowed:
                get_file_with_progress_bar(model_url=model_url, file_path=self.fp_zip)
            else:
                raise CLTKException(
                    f"Download of necessary Stanza model declined for '{self.language}'. Unable to continue with Stanza's processing."
                )

    def _unzip_nlpl_model(self) -> None:
        """Unzip model"""
        with ZipFile(self.fp_zip, "r") as zipfile_obj:
            zipfile_obj.extractall(path=self.fp_model_dirs)

    def _load_model(self) -> models.keyedvectors.Word2VecKeyedVectors:
        """Load model into memory.

        TODO: When testing show that this is a Gensim type
        TODO: Suppress Gensim info printout from screen
        """
        # KJ added these two checks because NLPL embeddings
        # began erring in Gensim (Oct 2021)
        is_binary: bool = False
        unicode_errors: str = "strict"
        if self.fp_model.endswith(".txt"):
            unicode_errors = "ignore"
        if self.fp_model.endswith(".bin"):
            is_binary = True
        try:
            return models.KeyedVectors.load_word2vec_format(
                self.fp_model,
                binary=is_binary,
                unicode_errors=unicode_errors,
            )
        except UnicodeDecodeError:
            msg = f"Cannot open file '{self.fp_model}' with Gensim 'load_word2vec_format'."
            print(msg)
            raise UnicodeDecodeError


class FastTextEmbeddings:
    """Wrapper for fastText embeddings."""

    def __init__(
        self,
        iso_code: str,
        training_set: str = "wiki",
        model_type: str = "vec",
        interactive: bool = True,
        overwrite: bool = False,
        silent: bool = False,
    ):
        """Constructor for  ``FastTextEmbeddings`` class."""
        self.iso_code = iso_code
        self.training_set = training_set
        self.model_type = model_type
        self.interactive = interactive
        self.silent = silent
        self.overwrite = overwrite

        if self.interactive and self.silent:
            raise ValueError(
                "``interactive`` and ``silent`` options are not compatible with each other."
            )

        self._check_input_params()

        # load model after all checks OK
        self.model_fp = self._build_fasttext_filepath()
        if not self._is_model_present() or self.overwrite:
            self.download_fasttext_models()
        elif self._is_model_present() and not self.overwrite:
            message = f"Model for '{self.iso_code}' / '{self.training_set}' / '{self.model_type}' already present at '{self.model_fp}' and ``overwrite=False``."
            # TODO: Log message
        self.model = self._load_model()

    def get_word_vector(self, word: str):
        """Return embedding array."""
        try:
            return self.model.get_vector(word)
        except KeyError:
            # TODO: To get an embedding from an OOV for sub-words, load the ``.bin`` file, too: `https://radimrehurek.com/gensim/models/fasttext.html#gensim.models.fasttext.load_facebook_model``_
            return None

    def get_embedding_length(self) -> int:
        """Return the embedding length for selected model."""
        return self.model.vector_size

    def get_sims(self, word: str):
        """Get similar words."""
        return self.model.most_similar(word)

    def download_fasttext_models(self):
        """Perform complete download of fastText models and save
        them in appropriate ``cltk_data`` dir.

        TODO: Add tests
        TODO: Implement ``overwrite``
        TODO: error out better or continue to _load_model?
        """
        model_url = self._build_fasttext_url()
        if not self.interactive:
            if not self.silent:
                print(
                    f"CLTK message: Going to download file '{model_url}' to '{self.model_fp} ..."
                )  # pragma: no cover
            get_file_with_progress_bar(model_url=model_url, file_path=self.model_fp)
        else:
            print(  # pragma: no cover
                "CLTK message: This part of the CLTK depends upon word embedding models from the Fasttext project."
            )  # pragma: no cover
            dl_is_allowed = query_yes_no(
                f"Do you want to download file '{model_url}' to '{self.model_fp}'?"
            )  # type: bool
            if dl_is_allowed:
                get_file_with_progress_bar(model_url=model_url, file_path=self.model_fp)
            else:
                raise CLTKException(
                    f"Download of necessary Stanza model declined for '{self.iso_code}'. Unable to continue with Stanza's processing."
                )

    def _is_model_present(self):
        """Check if model in an otherwise valid filepath."""

        if os.path.isfile(self.model_fp):
            return True
        else:
            return False

    def _check_input_params(self):
        """Look at combination of parameters give to class
        and determine if any invalid combination or missing
        models.
        """

        # 1. check if lang valid
        get_lang(self.iso_code)  # check if iso_code valid

        # 2. check if any fasttext embeddings for this lang
        if not self._is_fasttext_lang_available():
            available_embeddings_str = "', '".join(MAP_LANGS_CLTK_FASTTEXT.keys())
            raise UnimplementedAlgorithmError(
                f"No embedding available for language '{self.iso_code}'. FastTextEmbeddings available for: '{available_embeddings_str}'."
            )

        # 3. check if requested model type is available for fasttext
        valid_model_types = ["bin", "vec"]
        if self.model_type not in valid_model_types:
            valid_model_types_str = "', '"
            raise CLTKException(
                f"Invalid model type '{self.model_type}'. Choose: '{valid_model_types_str}'."
            )

        # 4. check if requested training set is available for language for fasttext
        training_sets = ["common_crawl", "wiki"]
        if self.training_set not in training_sets:
            training_sets_str = "', '".join(training_sets)
            raise CLTKException(
                f"Invalid ``training_set`` '{self.training_set}'. Available: '{training_sets_str}'."
            )
        available_vectors = list()
        if self.training_set == "wiki":
            available_vectors = ["ang", "arb", "arc", "got", "lat", "pli", "san"]
        elif self.training_set == "common_crawl":
            available_vectors = ["arb", "lat", "san"]
        else:
            CLTKException("Unanticipated exception.")
        if self.iso_code in available_vectors:
            pass
        else:
            available_vectors_str = "', '".join(available_vectors)
            raise CLTKException(
                f"Training set '{self.training_set}' not available for language '{self.iso_code}'. Languages available for this training set: '{available_vectors_str}'."
            )

    def _load_model(self):
        """Load model into memory.

        TODO: When testing show that this is a Gensim type
        TODO: Suppress Gensim info printout from screen
        """
        return models.KeyedVectors.load_word2vec_format(self.model_fp)

    def _is_fasttext_lang_available(self) -> bool:
        """Returns whether any vectors are available, for
        fastText, for the input language. This is not comprehensive
        of all fastText embeddings, only those added into the CLTK.
        """
        get_lang(iso_code=self.iso_code)
        if self.iso_code not in MAP_LANGS_CLTK_FASTTEXT:
            return False
        else:
            return True

    def _build_fasttext_filepath(self):
        """Create filepath at which to save a downloaded
        fasttext model.

        .. todo::
           Do better than test for just name. Try trimming up to user home dir.

        >>> from cltk.embeddings.embeddings import FastTextEmbeddings  # doctest: +SKIP
        >>> embeddings_obj = FastTextEmbeddings(iso_code="lat", silent=True)  # doctest: +SKIP
        >>> vec_fp = embeddings_obj._build_fasttext_filepath()  # doctest: +SKIP
        >>> os.path.split(vec_fp)[1]  # doctest: +SKIP
        'wiki.la.vec'
        >>> embeddings_obj = FastTextEmbeddings(iso_code="lat", training_set="bin", silent=True)  # doctest: +SKIP
        >>> bin_fp = embeddings_obj._build_fasttext_filepath()  # doctest: +SKIP
        >>> os.path.split(bin_fp)[1]  # doctest: +SKIP
        'wiki.la.bin'
        >>> embeddings_obj = FastTextEmbeddings(iso_code="lat", training_set="common_crawl", model_type="vec", silent=True)  # doctest: +SKIP
        >>> os.path.split(vec_fp)[1]  # doctest: +SKIP
        'cc.la.300.vec'
        >>> embeddings_obj = FastTextEmbeddings(iso_code="lat", training_set="common_crawl", model_type="bin", silent=True)  # doctest: +SKIP
        >>> bin_fp = embeddings_obj._build_fasttext_filepath()  # doctest: +SKIP
        >>> vec_fp = embeddings_obj._build_fasttext_filepath()  # doctest: +SKIP
        >>> os.path.split(bin_fp)[1]  # doctest: +SKIP
        'cc.la.300.bin'
        """
        fasttext_code = MAP_LANGS_CLTK_FASTTEXT[self.iso_code]

        fp_model = None
        if self.training_set == "wiki":
            fp_model = os.path.join(
                CLTK_DATA_DIR,
                self.iso_code,
                "embeddings",
                "fasttext",
                f"wiki.{fasttext_code}.{self.model_type}",
            )
        elif self.training_set == "common_crawl":
            fp_model = os.path.join(
                CLTK_DATA_DIR,
                self.iso_code,
                "embeddings",
                "fasttext",
                f"cc.{fasttext_code}.300.{self.model_type}",
            )
        else:
            raise CLTKException(f"Unexpected ``training_set`` ``{self.training_set}``.")
        return fp_model

    def _build_fasttext_url(self):
        """Make the URL at which the requested model may be
        downloaded."""
        fasttext_code = MAP_LANGS_CLTK_FASTTEXT[self.iso_code]
        if self.training_set == "wiki":
            if self.model_type == "vec":
                ending = "vec"
            else:
                # for .bin
                ending = "zip"
            url = f"https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.{fasttext_code}.{ending}"
        elif self.training_set == "common_crawl":
            url = f"https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.{fasttext_code}.300.{self.model_type}.gz"
        else:
            raise CLTKException("Unexpected exception.")
        return url
