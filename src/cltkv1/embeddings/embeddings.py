"""Module for accessing pre-trained `fastText word embeddings
<https://fasttext.cc/>`_. Two sets of models are available
from fastText, one being trained only on corpora taken from
Wikipedia (249 languages, `here
<https://fasttext.cc/docs/en/pretrained-vectors.html>`_) and
the other being a combination of Wikipedia and Common Crawl
(157 languages, a subset of the former, `here
<https://fasttext.cc/docs/en/crawl-vectors.html>`_).

TODO: Consider whether to use Gensim for accessing fastText vectors instead.

TODO: Figure out how to test fastText mdoels that (maybe) fail on build server due to insufficient memory.
"""

import io
import os

import fasttext
import requests
from gensim.models import (
    KeyedVectors,
)  # for word2vec-style embeddings (.vec for fastText)
from gensim.models.wrappers import FastText  # for fastText's .bin format
from tqdm import tqdm

from cltkv1 import __cltk_data_dir__
from cltkv1.core.exceptions import CLTKException, UnimplementedLanguageError
from cltkv1.languages.utils import get_lang


class FastText:
    """Wrapper for embeddings (word2Vec, fastText).

    TODO: Find better names for this and the module.

    >>> from cltkv1.embeddings.embeddings import FastText
    >>> embeddings_obj = FastText(iso_code="lat")
    >>> embeddings_obj.get_sims(word="amicitia")[0][0]
    'amicitiam'
    >>> vector = embeddings_obj.get_word_vector("amicitia")
    >>> type(vector)
    <class 'numpy.ndarray'>
    """

    def __init__(
        self,
        iso_code: str,
        training_set: str = "wiki",
        model_type: str = "vec",
        interactive: bool = True,
        overwrite: bool = True,
    ):
        """Constructor for  ``FastText`` class.

        >>> embeddings_obj = FastText(iso_code="lat")
        >>> type(embeddings_obj)
        <class 'cltkv1.embeddings.embeddings.FastText'>

        # >>> embeddings_obj = FastText(iso_code="xxx")
        # Traceback (most recent call last):
        #   ..
        # cltkv1.core.exceptions.UnknownLanguageError
        """
        self.iso_code = iso_code
        self.training_set = training_set
        self.model_type = model_type
        self.interactive = interactive
        self.overwrite = overwrite

        self.MAP_LANGS_CLTK_FASTTEXT = {
            "arb": "ar",  # Arabic
            "arc": "arc",  # Aramaic
            "got": "got",  # Gothic
            "lat": "la",  # Latin
            "pli": "pi",  # Pali
            "san": "sa",  # Sanskrit
            "xno": "ang",  # Anglo-Saxon
        }

        self._check_input_params()

        # load model once all checks OK
        self.model_fp = self._build_fasttext_filepath()
        if not self._is_model_present():
            self.download_fasttext_models()
        elif self._is_model_present() and self.overwrite:
            self.download_fasttext_models()
        else:
            raise IOError(
                f"Model for '{self.iso_code}' / '{self.training_set}' / '{self.model_type}' already present at '{self.model_fp}' and ``overwrite=False``. Set to ``True`` to download model again and overwrite the current."
            )
        self.model = self._load_model()

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

        >>> from cltkv1.embeddings.embeddings import FastText
        >>> fasttext_model = FastText(iso_code="lat")
        >>> type(fasttext_model)
        <class 'cltkv1.embeddings.embeddings.FastText'>
        >>> fasttext_model = FastText(iso_code="ave") # doctest: +ELLIPSIS
        Traceback (most recent call last):
          ..
        cltkv1.core.exceptions.UnimplementedLanguageError: No embedding available for language 'ave'. FastText available for: ...
        >>> fasttext_model = FastText(iso_code="xxx")
        Traceback (most recent call last):
          ..
        cltkv1.core.exceptions.UnknownLanguageError
        >>> fasttext_model = FastText(iso_code="got", training_set="wiki", interactive=False) # doctest: +ELLIPSIS
        >>> type(fasttext_model)
        ...
        <class 'cltkv1.embeddings.embeddings.FastText'>
        >>> fasttext_model = FastText(iso_code="got", training_set="common_crawl", interactive=False) # doctest: +ELLIPSIS
        Traceback (most recent call last):
          ..
        cltkv1.core.exceptions.CLTKException: Training set 'common_crawl' not available for language 'got'. Languages available for this training set: ...

        TODO: Add tests for ``.bin`` files, too
        """

        # 1. check if lang valid
        get_lang(self.iso_code)  # check if iso_code valid

        # 2. check if any fasttext embeddings for this lang
        if not self._is_fasttext_lang_available():
            available_embeddings_str = "', '".join(self.MAP_LANGS_CLTK_FASTTEXT.keys())
            raise UnimplementedLanguageError(
                f"No embedding available for language '{self.iso_code}'. FastText available for: {available_embeddings_str}."
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
            available_vectors = ["arb", "arc", "got", "lat", "pli", "san", "xno"]
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
        return KeyedVectors.load_word2vec_format(self.model_fp)

    def get_word_vector(self, word: str):
        """Return embedding array."""
        return self.model.get_vector(word)

    def get_sims(self, word: str):
        """Get similar words."""
        return self.model.most_similar(word)

    def _is_fasttext_lang_available(self) -> bool:
        """Returns whether any vectors are available, for
        fastText, for the input language. This is not comprehensive
        of all fastText embeddings, only those added into the CLTK.

        # >>> from cltkv1.embeddings.embeddings import FastText
        # >>> embeddings_obj = FastText(iso_code="lat")
        # >>> embeddings_obj._is_fasttext_lang_available()
        # True
        # >>> embeddings_obj = FastText(iso_code="ave")
        # Traceback (most recent call last):
        #   ..
        # cltkv1.core.exceptions.UnimplementedLanguageError: No embedding available for language 'ave'. FastText available for: arb', 'arc', 'got', 'lat', 'pli', 'san', 'xno.
        # >>> embeddings_obj = FastText(iso_code="xxx")
        # Traceback (most recent call last):
        #   ..
        # cltkv1.core.exceptions.UnknownLanguageError
        """
        get_lang(iso_code=self.iso_code)
        if self.iso_code not in self.MAP_LANGS_CLTK_FASTTEXT:
            return False
        else:
            return True

    #
    # def _is_vector_for_lang(self) -> bool:
    #     """Check whether a embedding is available for a chosen
    #     vector type, ``wiki`` or ``common_crawl``.
    #
    #     >>> from cltkv1.embeddings.embeddings import FastText
    #     >>> embeddings_obj = FastText(iso_code="lat")
    #     >>> embeddings_obj._is_fasttext_lang_available()
    #     True
    #     >>> embeddings_obj = FastText(iso_code="lat", training_set="common_crawl")
    #     >>> embeddings_obj._is_vector_for_lang()
    #     True
    #     >>> embeddings_obj = FastText(iso_code="pli", training_set="wiki")
    #     >>> embeddings_obj._is_vector_for_lang()
    #     True
    #     >>> embeddings_obj = FastText(iso_code="pli", training_set="common_crawl")
    #     >>> embeddings_obj._is_vector_for_lang()
    #     False
    #     """
    #     training_sets = ["wiki", "common_crawl"]
    #     if self.training_set not in training_sets:
    #         training_sets_str = "', '".join(training_sets)
    #         raise CLTKException(
    #             f"Invalid ``training_set`` '{self.training_set}'. Available: '{training_sets_str}'."
    #         )
    #     available_vectors = list()
    #     if self.training_set == "wiki":
    #         available_vectors = ["arb", "arc", "got", "lat", "pli", "san", "xno"]
    #     elif self.training_set == "common_crawl":
    #         available_vectors = ["arb", "lat", "san"]
    #     if self.iso_code in available_vectors:
    #         return True
    #     else:
    #         return False
    #
    def _build_fasttext_filepath(self):
        """Create filepath at which to save a downloaded
        fasttext model.

        TODO: Do better than test for just name. Try trimming up to user home dir.

        # >>> from cltkv1.embeddings.embeddings import FastText
        # >>> embeddings_obj = FastText(iso_code="lat")
        # >>> vec_fp = embeddings_obj._build_fasttext_filepath()
        # >>> os.path.split(vec_fp)[1]
        # 'wiki.la.vec'
        # >>> embeddings_obj = FastText(iso_code="lat", training_set="bin")
        # >>> bin_fp = embeddings_obj._build_fasttext_filepath()
        # >>> os.path.split(bin_fp)[1]
        # 'wiki.la.bin'
        # >>> embeddings_obj = FastText(iso_code="lat", training_set="common_crawl", model_type="vec")
        # >>> os.path.split(vec_fp)[1]
        # 'cc.la.300.vec'
        # >>> embeddings_obj = FastText(iso_code="lat", training_set="common_crawl", model_type="bin")
        # >>> bin_fp = embeddings_obj._build_fasttext_filepath()
        # >>> vec_fp = embeddings_obj._build_fasttext_filepath()
        # >>> os.path.split(bin_fp)[1]
        # 'cc.la.300.bin'
        """
        fasttext_code = self.MAP_LANGS_CLTK_FASTTEXT[self.iso_code]

        fp_model = None
        if self.training_set == "wiki":
            fp_model = os.path.join(
                __cltk_data_dir__,
                self.iso_code,
                "embeddings",
                "fasttext",
                f"wiki.{fasttext_code}.{self.model_type}",
            )
        elif self.training_set == "common_crawl":
            fp_model = os.path.join(
                __cltk_data_dir__,
                self.iso_code,
                "embeddings",
                "fasttext",
                f"cc.{fasttext_code}.300.{self.model_type}",
            )
        else:
            print(self.training_set)
            print(self.model_type)
            print(fp_model)
        return fp_model

    # def _are_fasttext_models_downloaded(self, training_set: str):
    #     """Check ``.bin` and/or ``.vec`` is present on disk at:
    #     ``~/cltk_data/lat/embeddings/fasttext/wiki.la.bin`` and
    #     ``~/cltk_data/lat/embeddings/fasttext/wiki.la.vec``.
    #
    #     >>> embeddings_obj = FastText(iso_code="lat")
    #     >>> embeddings_obj.are_fasttext_models_downloaded(iso_code="lat", training_set="wiki")
    #     True
    #     >>> embeddings_obj.are_fasttext_models_downloaded(iso_code="lat", training_set="common_crawl")
    #     True
    #     """
    #     self._is_fasttext_lang_available()
    #     is_vector_for_lang(iso_code=iso_code, training_set=training_set)
    #     fp_model_bin = _build_fasttext_filepath(
    #         iso_code=iso_code, training_set=training_set, model_type="bin"
    #     )
    #     fp_model_vec = _build_fasttext_filepath(
    #         iso_code=iso_code, training_set=training_set, model_type="vec"
    #     )
    #     if os.path.isfile(fp_model_bin) and os.path.isfile(fp_model_vec):
    #         return True
    #     else:
    #         return False

    def _build_fasttext_url(self):
        """Make the URL at which the requested model may be
        downloaded."""
        fasttext_code = self.MAP_LANGS_CLTK_FASTTEXT[self.iso_code]
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

    # def _mk_dirs_for_file(filepath):
    #     """Make all dirs specified for final file.
    #
    #     >>> _mk_dirs_for_file("~/new-dir/some-file.txt")
    #     """
    #     dirs = os.path.split(filepath)[0]
    #     try:
    #         os.makedirs(dirs)
    #     except FileExistsError:
    #         # TODO: Log INFO level
    #         pass

    def _get_file_with_progress_bar(self, model_url: str):
        """Download file with a progress bar.

        Source: https://stackoverflow.com/a/37573701

        TODO: Look at "Download Large Files with Tqdm Progress Bar" here: https://medium.com/better-programming/python-progress-bars-with-tqdm-by-example-ce98dbbc9697
        TODO: Confirm everything saves right
        TODO: Add tests
        """
        self._mk_dirs_for_file()
        req_obj = requests.get(url=model_url, stream=True)
        total_size = int(req_obj.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
        with open(self.model_fp, "wb") as file_open:
            for data in req_obj.iter_content(block_size):
                progress_bar.update(len(data))
                file_open.write(data)
        progress_bar.close()
        if total_size != 0 and progress_bar.n != total_size:
            raise IOError(
                f"Expected downloaded file to be of size '{total_size}' however it is in fact '{progress_bar.n}'."
            )

    def download_fasttext_models(self, overwrite=False):
        """Perform complete download of fastText models and save
        them in appropriate ``cltk_data`` dir.

        TODO: Add tests
        TODO: Implement ``force``
        TODO: error out better or continue to _load_model?
        """
        model_url = self._build_fasttext_url()
        if not self.interactive:
            print(f"Going to download file '{self.model_url}' to '{self.model_fp} ...")
            self._get_file_with_progress_bar(model_url=model_url)
        else:
            res = input(
                f"Do you want to download file '{model_url}' to '{self.model_fp}'? [y/n]"
            )
            if res.lower() == "y":
                self._get_file_with_progress_bar(model_url=model_url)
            elif res.lower() == "n":
                # lot error here and below
                return None
            else:
                return None

    def _mk_dirs_for_file(self):
        """Make all dirs specified for final file.

        # >>> _mk_dirs_for_file("~/new-dir/some-file.txt")
        """
        dirs = os.path.split(self.model_fp)[0]
        try:
            os.makedirs(dirs)
        except FileExistsError:
            # TODO: Log INFO level; it's OK if dir already exists
            return None
