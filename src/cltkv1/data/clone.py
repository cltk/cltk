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
from cltk.utils.cltk_logger import logger
from git import RemoteProgress, Repo

from cltkv1.core.exceptions import CorpusImportError
from cltkv1.languages.utils import get_lang
from cltkv1.utils.utils import CLTK_DATA_DIR

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
            "location": "remote",
            "type": "atf",
        }
    ],
    "arb": [
        {
            "name": "arabic_text_perseus",
            "origin": "https://github.com/cltk/arabic_text_perseus",
            "location": "remote",
            "type": "text",
            "RomanizationType": "Buckwalter",
        },
        {
            "name": "quranic-corpus",
            "origin": "https://github.com/cltk/arabic_text_quranic_corpus",
            "location": "remote",
            "type": "text",
            "RomanizationType": "none",
        },
        {
            "name": "quranic-corpus-morphology",
            "origin": "https://github.com/cltk/arabic_morphology_quranic-corpus",
            "location": "remote",
            "type": "text",
            "RomanizationType": "Buckwalter",
            "script": "Uthmani",
        },
    ],
    "lzh": [
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_01.git",
            "name": "chinese_text_cbeta_01",
        },
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_02.git",
            "name": "chinese_text_cbeta_02",
        },
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_indices.git",
            "name": "chinese_text_cbeta_indices",
        },
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_txt.git",
            "name": "chinese_text_cbeta_txt",
        },
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_taf_xml.git",
            "name": "chinese_text_cbeta_taf_xml",
        },
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/chinese_text_cbeta_txt.git",
            "name": "chinese_text_cbeta_txt",
        },
    ],
    "cop": [
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/coptic_text_scriptorium.git",
            "name": "coptic_text_scriptorium",
        }
    ],
    "grc": [
        {
            "name": "greek_software_tlgu",
            "origin": "https://github.com/cltk/greek_software_tlgu.git",
            "location": "remote",
            "type": "software",
        },
        {
            "origin": "https://github.com/cltk/greek_text_perseus.git",
            "name": "greek_text_perseus",
            "location": "remote",
            "type": "text",
        },
        {
            
            "origin": None,
            "name": "phi7",
            "location": "local",
            "type": "text",
        },
        {
            
            "name": "tlg",
            "origin": None,
            "location": "local",
            "type": "text",
        },
        {
            
            "name": "greek_proper_names_cltk",
            "origin": "https://github.com/cltk/greek_proper_names_cltk.git",
            "location": "remote",
            "type": "lexicon",
        },
        {
            "name": "greek_models_cltk",
            "origin": "https://github.com/cltk/greek_models_cltk.git",
            "location": "remote",
            "type": "model",
        },
        {
            "origin": "https://github.com/cltk/greek_treebank_perseus.git",
            "name": "greek_treebank_perseus",
            "location": "remote",
            "type": "treebank",
        },
        {
            "origin": "https://github.com/vgorman1/Greek-Dependency-Trees.git",
            "name": "greek_treebank_gorman",
            "location": "remote",
            "type": "treebank",
        },
        {
            
            "origin": "https://github.com/cltk/greek_lexica_perseus.git",
            "name": "greek_lexica_perseus",
            "location": "remote",
            "type": "lexicon",
        },
        {
            
            "origin": "https://github.com/cltk/greek_training_set_sentence_cltk.git",
            "name": "greek_training_set_sentence_cltk",
            "location": "remote",
            "type": "training_set",
        },
        {
            "name": "greek_word2vec_cltk",
            "origin": "https://github.com/cltk/greek_word2vec_cltk.git",
            "location": "remote",
            "type": "model",
        },
        {
            "name": "greek_text_lacus_curtius",
            "origin": "https://github.com/cltk/greek_text_lacus_curtius.git",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "greek_text_first1kgreek",
            "origin": "https://github.com/cltk/First1KGreek",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "greek_text_tesserae",
              # modified plaintext with Tesserae-style citations
            "origin": "https://github.com/cltk/greek_text_tesserae.git",
            "location": "remote",
            "type": "text",
        },
    ],
    "hbo": [
        {
            "name": "hebrew_text_sefaria",
            "origin": "https://github.com/cltk/hebrew_text_sefaria.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "lat": [
        {
            "location": "remote",
            "type": "text",
            "name": "latin_text_perseus",
            "origin": "https://github.com/cltk/latin_text_perseus.git",
        },
        {
            "name": "latin_treebank_perseus",
            "origin": "https://github.com/cltk/latin_treebank_perseus.git",
            "location": "remote",
            "type": "treebank",
        },
        {
            
            "name": "latin_text_latin_library",
            "origin": "https://github.com/cltk/latin_text_latin_library.git",
            "location": "remote",
            "type": "text",
        },
        {
            
            "location": "local",
            "name": "phi5",
            "origin": None,
            "type": "text",
        },
        {
            
            "origin": None,
            "name": "phi7",
            "location": "local",
            "type": "text",
        },
        {
            
            "name": "latin_proper_names_cltk",
            "origin": "https://github.com/cltk/latin_proper_names_cltk.git",
            "location": "remote",
            "type": "lexicon",
        },
        {
            "origin": "https://github.com/cltk/latin_models_cltk.git",
            "name": "latin_models_cltk",
            "location": "remote",
            "type": "model",
        },
        {
            
            "name": "latin_pos_lemmata_cltk",
            "origin": "https://github.com/cltk/latin_pos_lemmata_cltk.git",
            "location": "remote",
            "type": "lemma",
        },
        {
            "name": "latin_treebank_index_thomisticus",
            "origin": "https://github.com/cltk/latin_treebank_index_thomisticus.git",
            "location": "remote",
            "type": "treebank",
        },
        {
            
            "name": "latin_lexica_perseus",
            "origin": "https://github.com/cltk/latin_lexica_perseus.git",
            "location": "remote",
            "type": "lexicon",
        },
        {
            
            "name": "latin_training_set_sentence_cltk",
            "origin": "https://github.com/cltk/latin_training_set_sentence_cltk.git",
            "location": "remote",
            "type": "training_set",
        },
        {
            "origin": "https://github.com/cltk/latin_word2vec_cltk.git",
            "name": "latin_word2vec_cltk",
            "location": "remote",
            "type": "model",
        },
        {
            "location": "remote",
            "type": "text",
            "name": "latin_text_antique_digiliblt",
            "origin": "https://github.com/cltk/latin_text_antique_digiliblt.git",
        },
        {
            "location": "remote",
            "type": "text",
            "name": "latin_text_corpus_grammaticorum_latinorum",
            "origin": "https://github.com/cltk/latin_text_corpus_grammaticorum_latinorum.git",
        },
        {
            "location": "remote",
            "type": "text",
            "name": "latin_text_poeti_ditalia",
            "origin": "https://github.com/cltk/latin_text_poeti_ditalia.git",
        },
        {
            "name": "latin_text_tesserae",
              # modified plaintext with Tesserae-style citations
            "origin": "https://github.com/cltk/latin_text_tesserae.git",
            "location": "remote",
            "type": "text",
        },
    ],
    "multilingual": [
        {
            
            "location": "remote",
            "type": "treebank",
            "origin": "https://github.com/cltk/multilingual_treebank_proiel.git",
            "name": "multilingual_treebank_proiel",
        },
        {
            
            "location": "remote",
            "type": "treebank",
            "origin": "https://github.com/cltk/iswoc-treebank.git",
            "name": "multilingual_treebank_iswoc",
        },
        {
            
            "location": "remote",
            "type": "treebank",
            "origin": "https://github.com/cltk/treebank-releases.git",
            "name": "multilingual_treebank_torot",
        },
    ],
    "pli": [
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/pali_text_ptr_tipitaka.git",
            "name": "pali_text_ptr_tipitaka",
        },
        {
            "name": "pali_texts_gretil",
            "type": "text",
            "location": "remote",
            "origin": "https://github.com/cltk/pali_texts_gretil",
        },
    ],
    "pan": [
        {
            "name": "punjabi_text_gurban",
            "origin": "https://github.com/cltk/punjabi_text_gurban.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "xct": [
        {
            "location": "remote",
            "type": "pos",
            "origin": "https://github.com/cltk/tibetan_pos_tdc.git",
            "name": "tibetan_pos_tdc",
        },
        {
            "location": "remote",
            "type": "lexicon",
            "origin": "https://github.com/cltk/tibetan_lexica_tdc.git",
            "name": "tibetan_lexica_tdc",
        },
    ],
    "san": [
        {
            "name": "sanskrit_text_jnu",
            "location": "remote",
            "origin": "https://github.com/cltk/sanskrit_text_jnu.git",
            "type": "text",
        },
        {
            "name": "sanskrit_text_dcs",
            "origin": "https://github.com/cltk/sanskrit_text_dcs.git",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "sanskrit_parallel_sacred_texts",
            "origin": "https://github.com/cltk/sanskrit_parallel_sacred_texts.git",
            "location": "remote",
            "type": "parallel",
        },
        {
            "name": "sanskrit_text_sacred_texts",
            "location": "remote",
            "origin": "https://github.com/cltk/sanskrit_text_sacred_texts.git",
            "type": "text",
        },
        {
            "name": "sanskrit_parallel_gitasupersite",
            "origin": "https://github.com/cltk/sanskrit_parallel_gitasupersite.git",
            "location": "remote",
            "type": "parallel",
        },
        {
            "name": "sanskrit_text_gitasupersite",
            "origin": "https://github.com/cltk/sanskrit_text_gitasupersite.git",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "sanskrit_text_wikipedia",
            "origin": "https://github.com/cltk/sanskrit_text_wikipedia.git",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "sanskrit_text_sanskrit_documents",
            "origin": "https://github.com/cltk/sanskrit_text_sanskrit_documents.git",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "sanskrit_models_cltk",
            "origin": "https://github.com/cltk/sanskrit_models_cltk.git",
            "location": "remote",
            "type": "model",
        },
    ],
    "ang": [
        {
            "name": "old_english_text_sacred_texts",
            "origin": "https://github.com/cltk/old_english_text_sacred_texts.git",
            "location": "remote",
            "type": "html",
        },
        {
            "origin": "https://github.com/cltk/old_english_models_cltk.git",
            "name": "old_english_models_cltk",
            "location": "remote",
            "type": "model",
        },
    ],
    "ben": [
        {
            "name": "bengali_text_wikisource",
            "origin": "https://github.com/cltk/bengali_text_wikisource.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "chu": [
        {
            "name": "old_church_slavonic_ccmh",
            "origin": "https://github.com/cltk/old_church_slavonic_ccmh.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "pmh": [
        {
            "name": "prakrit_texts_gretil",
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/prakrit_texts_gretil.git",
        }
    ],
    "mal": [
        {
            "name": "malayalam_text_gretil",
            "origin": "https://github.com/cltk/malayalam_text_gretil.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "omr": [
        {
            "name": "marathi_text_wikisource",
            "origin": "https://github.com/cltk/marathi_text_wikisource.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "kaw": [
        {
            "name": "javanese_text_gretil",
            "origin": "https://github.com/cltk/javanese_text_gretil.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "non": [
        {
            "name": "old_norse_text_perseus",
            "location": "remote",
            "origin": "https://github.com/cltk/old_norse_text_perseus.git",
            "type": "text",
        },
        {
            "name": "old_norse_models_cltk",
            "origin": "https://github.com/cltk/old_norse_models_cltk.git",
            "location": "remote",
            "type": "model",
        },
        {
            "name": "old_norse_texts_heimskringla",
            "location": "remote",
            "origin": "https://github.com/cltk/old_norse_texts_heimskringla.git",
            "type": "text",
        },
        {
            "name": "old_norse_runic_transcriptions",
            "location": "remote",
            "origin": "https://github.com/cltk/old_norse_runes_corpus.git",
            "type": "text",
        },
        {
            "name": "old_norse_dictionary_zoega",
            "location": "remote",
            "origin": "https://github.com/cltk/old_norse_dictionary_zoega.git",
            "type": "dictionary",
        },
    ],
    "tel": [
        {
            "name": "telugu_text_wikisource",
            "origin": "https://github.com/cltk/telugu_text_wikisource.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "hin": [
        {
            "location": "remote",
            "type": "text",
            "origin": "https://github.com/cltk/hindi_text_ltrc.git",
            "name": "hindi_text_ltrc",
        }
    ],
    "fro": [
        {
            "name": "french_text_wikisource",
            "origin": "https://github.com/cltk/french_text_wikisource.git",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "french_lexicon_cltk",
            "origin": "https://github.com/cltk/french_lexicon_cltk.git",
            "location": "remote",
            "type": "text",
        },
        {
            "name": "french_data_cltk",
            "origin": "https://github.com/cltk/french_data_cltk.git",
            "location": "remote",
            "type": "text",
        },
    ],
    "guj": [
        {
            "name": "gujarati_text_wikisource",
            "origin": "https://github.com/cltk/gujarati_text_wikisource.git",
            "location": "remote",
            "type": "text",
        }
    ],
    "gml": [
        {
            "name": "middle_low_german_models_cltk",
            "origin": "https://github.com/cltk/middle_low_german_models_cltk.git",
            "location": "remote",
            "type": "model",
        }
    ],
    "gmh": [
        {
            "name": "middle_high_german_models_cltk",
            "origin": "https://github.com/cltk/middle_high_german_models_cltk.git",
            "location": "remote",
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


class CorpusImporter:
    """Import CLTK corpora."""

    def __init__(self, language, testing=False):
        """Setup corpus importing.

        `testing` is a hack to check a tmp .yaml file to look at or local corpus. This keeps from overwriting
        local. A better idea is probably to refuse to overwrite the .yaml.
        """

        self.language = language.lower()
        if self.language != "multilingual":
            get_lang(iso_code=language)

        assert isinstance(testing, bool), "``testing`` parameter must be boolean type"
        self.testing = testing

        self.user_defined_corpora = self._setup_language_variables()

        # if user_defined_corpora, then we need to add these to the corpus.py objects
        if self.user_defined_corpora:
            logger.info(
                'User-defined corpus found for "{}" language'.format(self.language)
            )
            try:
                logger.debug(
                    'Core corpora also found for "{}" language'.format(self.language)
                )
                logger.debug("Combining the user-defined and the core corpora")
                self.official_corpora = LANGUAGE_CORPORA[self.language]
                self.all_corpora = self.official_corpora
                for corpus in self.user_defined_corpora:
                    self.all_corpora.append(corpus)
            except KeyError:
                logger.debug(
                    "Nothing in the official repos "
                    'for "{}" language. Make the all_corpora solely '
                    "from the .yaml".format(self.language)
                )
                self.all_corpora = []
                for corpus in self.user_defined_corpora:
                    self.all_corpora.append(corpus)
        else:
            logger.info(
                'No user-defined corpora found for "{}" language'.format(self.language)
            )
            # self.official_corpora = LANGUAGE_CORPORA[self.language]
            self.all_corpora = LANGUAGE_CORPORA[self.language]

    def __repr__(self):
        """Representation string for ipython
        :rtype : str
        """
        return "CorpusImporter for: {}".format(self.language)

    def _check_distributed_corpora_file(self):
        """Check get_cltk_data_dir() + '/distributed_corpora.yaml' for any custom,
        distributed corpora that the user wants to load locally.

        TODO: write check or try if `cltk_data` dir is not present
        """
        if self.testing:
            distributed_corpora_fp = os.path.normpath(
                get_cltk_data_dir() + "/test_distributed_corpora.yaml"
            )
        else:
            distributed_corpora_fp = os.path.normpath(
                get_cltk_data_dir() + "/distributed_corpora.yaml"
            )

        try:
            with open(distributed_corpora_fp) as file_open:
                corpora_dict = yaml.safe_load(file_open)
        except FileNotFoundError:
            logger.info("``~/cltk_data/distributed_corpora.yaml`` file not found.")
            return []
        except yaml.parser.ParserError as parse_err:
            logger.debug("Yaml parsing error: %s" % parse_err)
            return []
        user_defined_corpora = []
        for corpus_name in corpora_dict:
            about = corpora_dict[corpus_name]

            if about["language"].lower() == self.language:
                user_defined_corpus = dict()
                # user_defined_corpus['git_remote'] = about['git_remote']
                user_defined_corpus["origin"] = about["origin"]
                user_defined_corpus["type"] = about["type"]
                user_defined_corpus["name"] = corpus_name
                user_defined_corpora.append(user_defined_corpus)

        return user_defined_corpora

    def _setup_language_variables(self):
        """Check for availability of corpora for a language.
        within ``corpora`` which contain a ``corpora.py`` file.

        TODO: Make the selection of available languages dynamic from dirs
        """
        if self.language not in LANGUAGE_CORPORA:
            # If no official repos, check if user has custom
            user_defined_corpora = self._check_distributed_corpora_file()
            if user_defined_corpora:
                return user_defined_corpora
            else:
                msg = 'Corpora not available (either core or user-defined) for the "{}" language.'.format(
                    self.language
                )
                logger.info(msg)
                raise CorpusImportError(msg)
        else:
            user_defined_corpora = self._check_distributed_corpora_file()
            return user_defined_corpora

    @property
    def list_corpora(self):
        """Show corpora available for the CLTK to download."""
        try:
            # corpora = LANGUAGE_CORPORA[self.language]
            corpora = self.all_corpora
            corpus_names = [corpus["name"] for corpus in corpora]
            return corpus_names
        except (NameError, KeyError) as error:
            msg = 'Corpus not available for language "{}": {}'.format(
                self.language, error
            )
            logger.error(msg)
            raise CorpusImportError(msg)

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

    def _get_corpus_properties(self, corpus_name):
        """Check whether a corpus is available for import.
        :type corpus_name: str
        :param corpus_name: Name of available corpus.
        :rtype : str
        """
        try:
            # corpora = LANGUAGE_CORPORA[self.language]
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
        # git_uri = urljoin('https://github.com/cltk/', corpus_name + '.git')
        # self._download_corpus(corpus_type, corpus_name, path)
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
        self, corpus_name, local_path=None, branch="master"
    ):  # pylint: disable=R0912
        """Download a remote or load local corpus into dir ``~/cltk_data``.
        TODO: maybe add ``from git import RemoteProgress``
        TODO: refactor this, it's getting kinda long
        :type corpus_name: str
        :param corpus_name: The name of an available corpus.
        :param local_path: str
        :param local_path: A filepath, required when importing local corpora.
        :param branch: What Git branch to clone.
        """
        corpus_properties = self._get_corpus_properties(corpus_name)
        try:
            location = corpus_properties["location"]
        except KeyError:
            # git_uri = corpus_properties['git_remote']
            git_name = corpus_properties[""]
            git_uri = corpus_properties["origin"]
            git_type = corpus_properties["type"]
            # pass this off to a special downloader just for custom urls
            self._git_user_defined_corpus(git_name, git_type, git_uri)
            return
        corpus_type = corpus_properties["type"]
        if location == "remote":
            # git_uri = urljoin('https://github.com/cltk/', corpus_name + '.git')
            git_uri = corpus_properties["origin"]
            type_dir_rel = os.path.join(CLTK_DATA_DIR, self.language, corpus_type)
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
        elif location == "local":
            msg = "Importing from local path: '{}'".format(local_path)
            logger.info(msg)
            if corpus_name in ("phi5", "phi7", "tlg"):
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


if __name__ == "__main__":
    for lang in LANGUAGE_CORPORA:
        c = CorpusImporter(language=lang)
        print(c.list_corpora)
        # c.import_corpus("latin_training_set_sentence_cltk")
