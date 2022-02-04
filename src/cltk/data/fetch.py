"""Import CLTK corpora.
TODO: ? Fix so ``import_corpora()`` can take relative path.
TODO: ? Add https://github.com/cltk/pos_latin

TODO: Consider renaming all "import" to "clone"
"""
import errno
import os
import shutil
import sys
from urllib.parse import urljoin

import yaml
from git import RemoteProgress, Repo

from cltk.core.cltk_logger import logger
from cltk.core.exceptions import CorpusImportError
from cltk.languages.utils import get_lang
from cltk.utils.utils import CLTK_DATA_DIR

__author__ = [
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Stephen Margheim <stephen.margheim@gmail.com>",
]


# TODO: Decide whether to drop repos w/o models
# langs_with_model_repo = ["grc", "lat", "ang", "gmh", "gml", "san", "non", "pli"]


LANGUAGE_CORPORA = {
    "akk": [
        {
            "name": "cdli_corpus",
            "origin": "https://github.com/cdli-gh/data.git",
            "type": "atf",
        }
    ],
    "arb": [
        {
            "name": "arabic_text_perseus",
            "origin": "https://github.com/cltk/arabic_text_perseus",
            "type": "text",
        },
        {
            "name": "quranic-corpus",
            "origin": "https://github.com/cltk/arabic_text_quranic_corpus",
            "type": "text",
        },
        {
            "name": "quranic-corpus-morphology",
            "origin": "https://github.com/cltk/arabic_morphology_quranic-corpus",
            "type": "text",
        },
    ],
    "lzh": [
        {
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_01.git",
            "name": "chinese_text_cbeta_01",
        },
        {
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_02.git",
            "name": "chinese_text_cbeta_02",
        },
        {
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_indices.git",
            "name": "chinese_text_cbeta_indices",
        },
        {
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_txt.git",
            "name": "chinese_text_cbeta_txt",
        },
        {
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_taf_xml.git",
            "name": "chinese_text_cbeta_taf_xml",
        },
        {
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_txt.git",
            "name": "chinese_text_cbeta_txt",
        },
    ],
    "cop": [
        {
            "type": "text",
            "origin": "https://github.com/cltk/coptic_text_scriptorium.git",
            "name": "coptic_text_scriptorium",
        }
    ],
    "grc": [
        {
            "name": "grc_software_tlgu",
            "origin": "https://github.com/cltk/grc_software_tlgu.git",
            "type": "software",
        },
        {
            "name": "grc_text_perseus",
            "origin": "https://github.com/cltk/grc_text_perseus.git",
            "type": "text",
        },
        {"origin": None, "name": "phi7", "location": "local", "type": "text"},
        {"name": "tlg", "origin": None, "location": "local", "type": "text"},
        {
            "name": "greek_proper_names_cltk",
            "origin": "https://github.com/cltk/greek_proper_names_cltk.git",
            "type": "lexicon",
        },
        {
            "name": "grc_models_cltk",
            "origin": "https://github.com/cltk/grc_models_cltk.git",
            "type": "model",
        },
        {
            "origin": "https://github.com/cltk/greek_treebank_perseus.git",
            "name": "greek_treebank_perseus",
            "type": "treebank",
        },
        {
            "origin": "https://github.com/vgorman1/Greek-Dependency-Trees.git",
            "name": "greek_treebank_gorman",
            "type": "treebank",
        },
        {
            "origin": "https://github.com/cltk/greek_lexica_perseus.git",
            "name": "greek_lexica_perseus",
            "type": "lexicon",
        },
        {
            "origin": "https://github.com/cltk/greek_training_set_sentence_cltk.git",
            "name": "greek_training_set_sentence_cltk",
            "type": "training_set",
        },
        {
            "name": "greek_word2vec_cltk",
            "origin": "https://github.com/cltk/greek_word2vec_cltk.git",
            "type": "model",
        },
        {
            "name": "greek_text_lacus_curtius",
            "origin": "https://github.com/cltk/greek_text_lacus_curtius.git",
            "type": "text",
        },
        {
            "name": "grc_text_first1kgreek",
            "origin": "https://github.com/cltk/First1KGreek",
            "type": "text",
        },
        {
            "name": "grc_text_tesserae",
            # modified plaintext with Tesserae-style citations
            "origin": "https://github.com/cltk/grc_text_tesserae.git",
            "type": "text",
        },
    ],
    "hbo": [
        {
            "name": "hebrew_text_sefaria",
            "origin": "https://github.com/cltk/hebrew_text_sefaria.git",
            "type": "text",
        }
    ],
    "lat": [
        {
            "type": "text",
            "name": "lat_text_perseus",
            "origin": "https://github.com/cltk/lat_text_perseus.git",
        },
        {
            "name": "lat_treebank_perseus",
            "origin": "https://github.com/cltk/lat_treebank_perseus.git",
            "type": "treebank",
        },
        {
            "name": "lat_text_latin_library",
            "origin": "https://github.com/cltk/lat_text_latin_library.git",
            "type": "text",
        },
        {"location": "local", "name": "phi5", "origin": None, "type": "text"},
        {"origin": None, "name": "phi7", "location": "local", "type": "text"},
        {
            "name": "latin_proper_names_cltk",
            "origin": "https://github.com/cltk/latin_proper_names_cltk.git",
            "type": "lexicon",
        },
        {
            "origin": "https://github.com/cltk/lat_models_cltk.git",
            "name": "lat_models_cltk",
            "type": "model",
        },
        {
            "name": "latin_pos_lemmata_cltk",
            "origin": "https://github.com/cltk/latin_pos_lemmata_cltk.git",
            "type": "lemma",
        },
        {
            "name": "latin_treebank_index_thomisticus",
            "origin": "https://github.com/cltk/latin_treebank_index_thomisticus.git",
            "type": "treebank",
        },
        {
            "name": "latin_lexica_perseus",
            "origin": "https://github.com/cltk/latin_lexica_perseus.git",
            "type": "lexicon",
        },
        {
            "name": "latin_training_set_sentence_cltk",
            "origin": "https://github.com/cltk/latin_training_set_sentence_cltk.git",
            "type": "training_set",
        },
        {
            "origin": "https://github.com/cltk/latin_word2vec_cltk.git",
            "name": "latin_word2vec_cltk",
            "type": "model",
        },
        {
            "type": "text",
            "name": "latin_text_antique_digiliblt",
            "origin": "https://github.com/cltk/latin_text_antique_digiliblt.git",
        },
        {
            "type": "text",
            "name": "latin_text_corpus_grammaticorum_latinorum",
            "origin": "https://github.com/cltk/latin_text_corpus_grammaticorum_latinorum.git",
        },
        {
            "type": "text",
            "name": "latin_text_poeti_ditalia",
            "origin": "https://github.com/cltk/latin_text_poeti_ditalia.git",
        },
        {
            "name": "lat_text_tesserae",
            # modified plaintext with Tesserae-style citations
            "origin": "https://github.com/cltk/lat_text_tesserae.git",
            "type": "text",
        },
        {
            "type": "lexicon",
            "name": "cltk_lat_lewis_elementary_lexicon",
            "origin": "https://github.com/cltk/cltk_lat_lewis_elementary_lexicon.git",
        },
    ],
    "multilingual": [
        {
            "type": "treebank",
            "origin": "https://github.com/cltk/multilingual_treebank_proiel.git",
            "name": "multilingual_treebank_proiel",
        },
        {
            "type": "treebank",
            "origin": "https://github.com/cltk/iswoc-treebank.git",
            "name": "multilingual_treebank_iswoc",
        },
        {
            "type": "treebank",
            "origin": "https://github.com/cltk/treebank-releases.git",
            "name": "multilingual_treebank_torot",
        },
    ],
    "pli": [
        {
            "type": "text",
            "origin": "https://github.com/cltk/pali_text_ptr_tipitaka.git",
            "name": "pali_text_ptr_tipitaka",
        },
        {
            "name": "pali_texts_gretil",
            "type": "text",
            "origin": "https://github.com/cltk/pali_texts_gretil",
        },
    ],
    "pan": [
        {
            "name": "punjabi_text_gurban",
            "origin": "https://github.com/cltk/punjabi_text_gurban.git",
            "type": "text",
        }
    ],
    "xct": [
        {
            "type": "pos",
            "origin": "https://github.com/cltk/tibetan_pos_tdc.git",
            "name": "tibetan_pos_tdc",
        },
        {
            "type": "lexicon",
            "origin": "https://github.com/cltk/tibetan_lexica_tdc.git",
            "name": "tibetan_lexica_tdc",
        },
    ],
    "san": [
        {
            "name": "sanskrit_text_jnu",
            "origin": "https://github.com/cltk/sanskrit_text_jnu.git",
            "type": "text",
        },
        {
            "name": "sanskrit_text_dcs",
            "origin": "https://github.com/cltk/sanskrit_text_dcs.git",
            "type": "text",
        },
        {
            "name": "sanskrit_parallel_sacred_texts",
            "origin": "https://github.com/cltk/sanskrit_parallel_sacred_texts.git",
            "type": "parallel",
        },
        {
            "name": "sanskrit_text_sacred_texts",
            "origin": "https://github.com/cltk/sanskrit_text_sacred_texts.git",
            "type": "text",
        },
        {
            "name": "sanskrit_parallel_gitasupersite",
            "origin": "https://github.com/cltk/sanskrit_parallel_gitasupersite.git",
            "type": "parallel",
        },
        {
            "name": "sanskrit_text_gitasupersite",
            "origin": "https://github.com/cltk/sanskrit_text_gitasupersite.git",
            "type": "text",
        },
        {
            "name": "sanskrit_text_wikipedia",
            "origin": "https://github.com/cltk/sanskrit_text_wikipedia.git",
            "type": "text",
        },
        {
            "name": "sanskrit_text_sanskrit_documents",
            "origin": "https://github.com/cltk/sanskrit_text_sanskrit_documents.git",
            "type": "text",
        },
        {
            "name": "san_models_cltk",
            "origin": "https://github.com/cltk/san_models_cltk.git",
            "type": "model",
        },
    ],
    "ang": [
        {
            "name": "old_english_text_sacred_texts",
            "origin": "https://github.com/cltk/old_english_text_sacred_texts.git",
            "type": "html",
        },
        {
            "origin": "https://github.com/cltk/ang_models_cltk.git",
            "name": "ang_models_cltk",
            "type": "model",
        },
    ],
    "ben": [
        {
            "name": "bengali_text_wikisource",
            "origin": "https://github.com/cltk/bengali_text_wikisource.git",
            "type": "text",
        }
    ],
    "chu": [
        {
            "name": "old_church_slavonic_ccmh",
            "origin": "https://github.com/cltk/old_church_slavonic_ccmh.git",
            "type": "text",
        }
    ],
    "pmh": [
        {
            "name": "prakrit_texts_gretil",
            "type": "text",
            "origin": "https://github.com/cltk/prakrit_texts_gretil.git",
        }
    ],
    "mal": [
        {
            "name": "malayalam_text_gretil",
            "origin": "https://github.com/cltk/malayalam_text_gretil.git",
            "type": "text",
        }
    ],
    "omr": [
        {
            "name": "marathi_text_wikisource",
            "origin": "https://github.com/cltk/marathi_text_wikisource.git",
            "type": "text",
        }
    ],
    "kaw": [
        {
            "name": "javanese_text_gretil",
            "origin": "https://github.com/cltk/javanese_text_gretil.git",
            "type": "text",
        }
    ],
    "non": [
        {
            "name": "old_norse_text_perseus",
            "origin": "https://github.com/cltk/old_norse_text_perseus.git",
            "type": "text",
        },
        {
            "name": "non_models_cltk",
            "origin": "https://github.com/cltk/non_models_cltk.git",
            "type": "model",
        },
        {
            "name": "old_norse_texts_heimskringla",
            "origin": "https://github.com/cltk/old_norse_texts_heimskringla.git",
            "type": "text",
        },
        {
            "name": "old_norse_runic_transcriptions",
            "origin": "https://github.com/cltk/old_norse_runes_corpus.git",
            "type": "text",
        },
        {
            "name": "cltk_non_zoega_dictionary",
            "origin": "https://github.com/cltk/cltk_non_zoega_dictionary.git",
            "type": "dictionary",
        },
    ],
    "tel": [
        {
            "name": "telugu_text_wikisource",
            "origin": "https://github.com/cltk/telugu_text_wikisource.git",
            "type": "text",
        }
    ],
    "hin": [
        {
            "type": "text",
            "origin": "https://github.com/cltk/hindi_text_ltrc.git",
            "name": "hindi_text_ltrc",
        }
    ],
    "fro": [
        {
            "name": "french_text_wikisource",
            "origin": "https://github.com/cltk/french_text_wikisource.git",
            "type": "text",
        },
        {
            "name": "french_lexicon_cltk",
            "origin": "https://github.com/cltk/french_lexicon_cltk.git",
            "type": "text",
        },
        {
            "name": "fro_models_cltk",
            "origin": "https://github.com/cltk/fro_models_cltk.git",
            "type": "model",
        },
    ],
    "guj": [
        {
            "name": "gujarati_text_wikisource",
            "origin": "https://github.com/cltk/gujarati_text_wikisource.git",
            "type": "text",
        }
    ],
    "gml": [
        {
            "name": "gml_models_cltk",
            "origin": "https://github.com/cltk/gml_models_cltk.git",
            "type": "model",
        }
    ],
    "gmh": [
        {
            "name": "gmh_models_cltk",
            "origin": "https://github.com/cltk/gmh_models_cltk.git",
            "type": "model",
        }
    ],
}


class ProgressPrinter(RemoteProgress):
    """Class that implements progress reporting."""

    def update(self, op_code, cur_count, max_count=None, message=""):
        if message:
            percentage = "%.0f" % (100 * cur_count / (max_count or 100.0))
            sys.stdout.write("Downloaded %s%% %s \r" % (percentage, message))


class FetchCorpus:
    """Import CLTK corpora."""

    def __init__(self, language: str, testing: bool = False):
        """Setup corpus importing.

        `testing` is a hack to check a tmp .yaml file to look at
        or local corpus. This keeps from overwriting local. A
        better idea is probably to refuse to overwrite the .yaml.
        """

        self.language = language.lower()
        if self.language != "multilingual":
            get_lang(iso_code=language)

        assert isinstance(testing, bool), "``testing`` parameter must be boolean type"
        self.testing = testing

        self.user_defined_corpora = self._get_user_defined_corpora()
        self.library_defined_corpora = self._get_library_defined_corpora()
        self.all_corpora_for_lang = (
            self.user_defined_corpora + self.library_defined_corpora
        )

    def __repr__(self):
        """Representation string for ipython
        :rtype : str
        """
        return "FetchCorpus for: {}".format(self.language)

    def _get_user_defined_corpora(self):
        """Check CLTK_DATA_DIR + '/distributed_corpora.yaml' for any custom,
        distributed corpora that the user wants to load locally.
        """
        if self.testing:
            distributed_corpora_fp = os.path.normpath(
                CLTK_DATA_DIR + "/test_distributed_corpora.yaml"
            )
        else:
            distributed_corpora_fp = os.path.normpath(
                CLTK_DATA_DIR + "/distributed_corpora.yaml"
            )
        try:
            with open(distributed_corpora_fp) as file_open:
                corpora_dict = yaml.safe_load(file_open)
        except FileNotFoundError:
            logger.debug("``~/cltk_data/distributed_corpora.yaml`` file not found.")
            return []
        except yaml.parser.ParserError as parse_err:
            logger.debug("Yaml parsing error: %s" % parse_err)
            return []
        user_defined_corpora = []
        for corpus_name in corpora_dict:
            about = corpora_dict[corpus_name]

            if about["language"].lower() == self.language:
                user_defined_corpus = dict()
                user_defined_corpus["origin"] = about["origin"]
                user_defined_corpus["type"] = about["type"]
                user_defined_corpus["name"] = corpus_name
                user_defined_corpus["user_defined"] = True
                user_defined_corpora.append(user_defined_corpus)

        return user_defined_corpora

    def _get_library_defined_corpora(self):
        """Pull from ``LANGUAGE_CORPORA`` and return
        corpora for given language.
        """
        try:
            return LANGUAGE_CORPORA[self.language]
        except KeyError:
            return list()

    @property
    def list_corpora(self):
        """Show corpora available for the CLTK to download."""
        return [corpus_info["name"] for corpus_info in self.all_corpora_for_lang]

    @staticmethod
    def _copy_dir_recursive(src_rel, dst_rel):
        """Copy contents of one directory to another. `dst_rel` dir cannot
        exist. Source: http://stackoverflow.com/a/1994840
        TODO: Move this to file_operations.py module.
        :type src_rel: str
        :param src_rel: Directory to be copied.
        :type dst_rel: str
        :param dst_rel: Directory to be created with contents of ``src_rel``.
        """
        src = os.path.expanduser(src_rel)
        dst = os.path.expanduser(dst_rel)
        try:
            shutil.copytree(src, dst)
            logger.info("Files copied from %s to %s", src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
                logger.info("Files copied from %s to %s", src, dst)
            else:
                raise

    def _get_corpus_properties(self, corpus_name: str):
        """Check whether a corpus is available for import.
        :type corpus_name: str
        :param corpus_name: Name of available corpus.
        :rtype : str
        """
        try:
            corpora = self.all_corpora
        except NameError as name_error:
            msg = "Corpus not available for language " '"%s": %s' % (
                self.language,
                name_error,
            )
            logger.error(msg)
            raise CorpusImportError(msg)
        for corpus_properties in corpora:
            if corpus_properties["name"] == corpus_name:
                return corpus_properties
        msg = 'Corpus "%s" not available for the ' '"%s" language.' % (
            corpus_name,
            self.language,
        )
        logger.error(msg)
        raise CorpusImportError(msg)

    def _git_user_defined_corpus(
        self, corpus_name, corpus_type, uri: str, branch="master"
    ):
        """Clone or update a git repo defined by user.
        TODO: This code is very redundant with what's in import_corpus(),
        could be refactored.
        """
        type_dir_rel = os.path.join(CLTK_DATA_DIR, self.language, corpus_type)
        type_dir = os.path.expanduser(type_dir_rel)
        repo_name = uri.split("/")[-1]  # eg, 'latin_corpus_newton_example.git'
        repo_name = repo_name.rstrip(".git")
        target_dir = os.path.join(type_dir, repo_name)
        target_file = os.path.join(type_dir, repo_name, "README.md")
        # check if corpus already present
        # if not, clone
        if not os.path.isfile(target_file):
            if not os.path.isdir(type_dir):
                os.makedirs(type_dir)
            try:
                msg = "Cloning '{}' from '{}'".format(corpus_name, uri)
                logger.info(msg)
                Repo.clone_from(
                    uri, target_dir, branch=branch, depth=1, progress=ProgressPrinter()
                )
            except CorpusImportError as corpus_imp_err:
                msg = "Git clone of '{}' failed: '{}'".format(uri, corpus_imp_err)
                logger.error(msg)
        # if corpus is present, pull latest
        else:
            try:
                repo = Repo(target_dir)
                assert not repo.bare  # or: assert repo.exists()
                git_origin = repo.remotes.origin
                msg = "Pulling latest '{}' from '{}'.".format(corpus_name, uri)
                logger.info(msg)
                git_origin.pull()
            except CorpusImportError as corpus_imp_err:
                msg = "Git pull of '{}' failed: '{}'".format(uri, corpus_imp_err)
                logger.error(msg)

    def import_corpus(
        self, corpus_name: str, local_path: str = None, branch: str = "master"
    ):
        """Download a remote or load local corpus into dir ``~/cltk_data``.

        TODO: maybe add ``from git import RemoteProgress``
        TODO: refactor this, it's getting kinda long

        :param corpus_name: The name of an available corpus.
        :param local_path: A filepath, required when importing local corpora.
        :param branch: What Git branch to clone.
        """

        matching_corpus_list = [
            _dict for _dict in self.all_corpora_for_lang if _dict["name"] == corpus_name
        ]
        if not matching_corpus_list:
            raise CorpusImportError(
                f"No corpus ``{corpus_name}`` for language ``{self.language}``."
            )
        if len(matching_corpus_list) > 1:
            raise CorpusImportError(
                f"Found more than one corpus with the name ``{corpus_name}``."
            )
        matching_corpus = matching_corpus_list[0]
        if matching_corpus.get("user_defined"):
            """{'origin': 'https://github.com/kylepjohnson/latin_corpus_newton_example.git',
            'type': 'text',
            'name': 'example_distributed_latin_corpus',
            'user_defined': True}
            """
            self._git_user_defined_corpus(
                matching_corpus["name"],
                matching_corpus["type"],
                matching_corpus["origin"],
            )
            return
        elif matching_corpus.get("location") == "local":
            # {'location': 'local', 'name': 'phi5', 'origin': None, 'type': 'text'}
            msg = "Importing from local path: '{}'".format(local_path)
            logger.info(msg)
            if corpus_name not in ["phi5", "phi7", "tlg"]:
                raise CorpusImportError(f"Unsupported local corpus ``{corpus_name}``.")
            if corpus_name == "phi5":
                # normalize path for checking dir
                if local_path.endswith("/"):
                    local_path = local_path[:-1]
                # check for right corpus dir
                if os.path.split(local_path)[1] != "PHI5":
                    logger.info("Directory must be named 'PHI5'.")
            if corpus_name == "phi7":
                # normalize local_path for checking dir
                if local_path.endswith("/"):
                    local_path = local_path[:-1]
                # check for right corpus dir
                if os.path.split(local_path)[1] != "PHI7":
                    logger.info("Directory must be named 'PHI7'.")
            if corpus_name == "tlg":
                # normalize path for checking dir
                if local_path.endswith("/"):
                    local_path = local_path[:-1]
                # check for right corpus dir
                if os.path.split(local_path)[1] != "TLG_E":
                    logger.info("Directory must be named 'TLG_E'.")
            # move the dir-checking commands into a function
            data_dir = os.path.expanduser(CLTK_DATA_DIR)
            originals_dir = os.path.join(data_dir, "originals")
            # check for `originals` dir; if not present mkdir
            if not os.path.isdir(originals_dir):
                os.makedirs(originals_dir)
                msg = "Wrote directory at '{}'.".format(originals_dir)
                logger.info(msg)
            tlg_originals_dir = os.path.join(data_dir, "originals", corpus_name)
            # check for `originals/<corpus_name>`; if pres, delete
            if os.path.isdir(tlg_originals_dir):
                shutil.rmtree(tlg_originals_dir)
                msg = "Removed directory at '{}'.".format(tlg_originals_dir)
                logger.info(msg)
            # copy_dir requires that target
            if not os.path.isdir(tlg_originals_dir):
                self._copy_dir_recursive(local_path, tlg_originals_dir)
        else:
            """{'type': 'text',
            'name': 'lat_text_perseus',
            'origin': 'https://github.com/cltk/lat_text_perseus.git'},
            """
            if (
                not matching_corpus.get("type")
                and not matching_corpus.get("name")
                and not matching_corpus.get("origin")
            ):
                raise FetchCorpus(f"Malformed record for ``{corpus_name}``.")
            git_uri = matching_corpus["origin"]
            type_dir_rel = os.path.join(
                CLTK_DATA_DIR, self.language, matching_corpus["type"]
            )
            type_dir = os.path.expanduser(type_dir_rel)
            target_dir = os.path.join(type_dir, corpus_name)
            target_file = os.path.join(type_dir, corpus_name, "README.md")
            # check if corpus already present
            # if not, clone
            if not os.path.isfile(target_file):
                if not os.path.isdir(type_dir):
                    os.makedirs(type_dir)
                try:
                    msg = "Cloning '{}' from '{}'".format(corpus_name, git_uri)
                    logger.info(msg)
                    Repo.clone_from(
                        git_uri,
                        target_dir,
                        branch=branch,
                        depth=1,
                        progress=ProgressPrinter(),
                    )
                except CorpusImportError as corpus_imp_err:
                    msg = "Git clone of '{}' failed: '{}'".format(
                        git_uri, corpus_imp_err
                    )
                    logger.error(msg)
            # if corpus is present, pull latest
            else:
                try:
                    repo = Repo(target_dir)
                    assert not repo.bare  # or: assert repo.exists()
                    git_origin = repo.remotes.origin
                    msg = "Pulling latest '{}' from '{}'.".format(corpus_name, git_uri)
                    logger.info(msg)
                    git_origin.pull()
                except CorpusImportError as corpus_imp_err:
                    msg = "Git pull of '{}' failed: '{}'".format(
                        git_uri, corpus_imp_err
                    )
                    logger.error(msg)
