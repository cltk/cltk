"""Import CLTK corpora.
TODO: Fix so ``import_corpora()`` can take relative path.
TODO: Add https://github.com/cltk/pos_latin
"""
from cltk.corpus.akkadian.corpora import AKKADIAN_CORPORA
from cltk.corpus.arabic.corpora import ARABIC_CORPORA
from cltk.corpus.chinese.corpora import CHINESE_CORPORA
from cltk.corpus.coptic.corpora import COPTIC_CORPORA
from cltk.corpus.greek.corpora import GREEK_CORPORA
from cltk.corpus.hebrew.corpora import HEBREW_CORPORA
from cltk.corpus.latin.corpora import LATIN_CORPORA
from cltk.corpus.sanskrit.corpora import SANSKRIT_CORPORA
from cltk.corpus.multilingual.corpora import MULTILINGUAL_CORPORA
from cltk.corpus.pali.corpora import PALI_CORPORA
from cltk.corpus.punjabi.corpora import PUNJABI_CORPORA
from cltk.corpus.tibetan.corpora import TIBETAN_CORPORA
from cltk.corpus.old_english.corpora import OLD_ENGLISH_CORPORA
from cltk.corpus.bengali.corpora import BENGALI_CORPORA
from cltk.corpus.old_church_slavonic.corpora import OCS_CORPORA
from cltk.corpus.prakrit.corpora import PRAKRIT_CORPORA
from cltk.corpus.hindi.corpora import HINDI_CORPORA
from cltk.corpus.javanese.corpora import JAVANESE_CORPORA
from cltk.corpus.malayalam.corpora import MALAYALAM_CORPORA
from cltk.corpus.old_norse.corpora import OLD_NORSE_CORPORA
from cltk.corpus.telugu.corpora import TELUGU_CORPORA
from cltk.corpus.classical_hindi.corpora import CLASSICAL_HINDI_CORPORA
from cltk.corpus.french.corpora import FRENCH_CORPORA
from cltk.corpus.marathi.corpora import MARATHI_CORPORA
from cltk.corpus.gujarati.corpora import GUJARATI_CORPORA
from cltk.corpus.middle_low_german.corpora import MIDDLE_LOW_GERMAN_CORPORA

from cltk.utils.cltk_logger import logger

import errno
from git import RemoteProgress
from git import Repo
import os
import sys
import shutil
from urllib.parse import urljoin
import yaml


__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>', 'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


AVAILABLE_LANGUAGES = ['akkadian', 'arabic', 'chinese', 'coptic', 'greek', 'hebrew', 'latin',
                       'multilingual', 'pali', 'punjabi', 'tibetan', 'sanskrit', 'old_english',
                       'bengali', 'prakrit', 'hindi', 'old_church_slavonic',
                       'malayalam', 'marathi', 'javanese','old_norse','telugu','classical_hindi',
                       'french', 'gujarati', 'middle_high_german', 'middle_low_german']


CLTK_DATA_DIR = '~/cltk_data'
LANGUAGE_CORPORA = {'akkadian': AKKADIAN_CORPORA,
                    'arabic': ARABIC_CORPORA,
                    'chinese': CHINESE_CORPORA,
                    'coptic': COPTIC_CORPORA,
                    'greek': GREEK_CORPORA,
                    'hebrew': HEBREW_CORPORA,
                    'latin': LATIN_CORPORA,
                    'multilingual': MULTILINGUAL_CORPORA,
                    'pali': PALI_CORPORA,
                    'punjabi': PUNJABI_CORPORA,
                    'tibetan': TIBETAN_CORPORA,
                    'sanskrit': SANSKRIT_CORPORA,
                    'old_english': OLD_ENGLISH_CORPORA,
                    'bengali': BENGALI_CORPORA,
                    'old_church_slavonic': OCS_CORPORA,
                    'prakrit': PRAKRIT_CORPORA,
                    'hindi': HINDI_CORPORA,
                    'malayalam': MALAYALAM_CORPORA,
                    'marathi': MARATHI_CORPORA,
                    'javanese': JAVANESE_CORPORA,
                    'old_norse':OLD_NORSE_CORPORA,
                    'telugu':TELUGU_CORPORA,
                    'classical_hindi':CLASSICAL_HINDI_CORPORA,
                    'french':FRENCH_CORPORA,
                    'gujarati': GUJARATI_CORPORA,
                    'middle_low_german': MIDDLE_LOW_GERMAN_CORPORA

                    }


class CorpusImportError(Exception):
    """CLTK exception to use when something goes wrong importing corpora"""
    pass


class ProgressPrinter(RemoteProgress):
    """Class that implements progress reporting."""
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            percentage = '%.0f' % (100 * cur_count / (max_count or 100.0))
            sys.stdout.write('Downloaded %s%% %s \r' % (percentage, message))


class CorpusImporter:
    """Import CLTK corpora."""

    def __init__(self, language, testing=False):
        """Setup corpus importing.

        `testing` is a hack to check a tmp .yaml file to look at or local corpus. This keeps from overwriting
        local. A better idea is probably to refuse to overwrite the .yaml.
        """
        self.language = language.lower()

        assert isinstance(testing, bool), '`testing` parameter must be boolean type'
        self.testing = testing

        self.user_defined_corpora = self._setup_language_variables()

        # if user_defined_corpora, then we need to add these to the corpus.py objects
        if self.user_defined_corpora:
            logger.info('User-defined corpus found for "{}" language'.format(self.language))
            try:
                logger.debug('Core corpora also found for "{}" language'.format(self.language))
                logger.debug('Combining the user-defined and the core corpora')
                self.official_corpora = LANGUAGE_CORPORA[self.language]
                self.all_corpora = self.official_corpora
                for corpus in self.user_defined_corpora:
                    self.all_corpora.append(corpus)
            except KeyError:
                logger.debug('Nothing in the official repos '
                             'for "{}" language. Make the all_corpora solely '
                             'from the .yaml'.format(self.language))
                self.all_corpora = []
                for corpus in self.user_defined_corpora:
                    self.all_corpora.append(corpus)
        else:
            logger.info('No user-defined corpora found for "{}" language'.format(self.language))
            # self.official_corpora = LANGUAGE_CORPORA[self.language]
            self.all_corpora = LANGUAGE_CORPORA[self.language]

    def __repr__(self):
        """Representation string for ipython
        :rtype : str
        """
        return 'CorpusImporter for: {}'.format(self.language)

    def _check_distributed_corpora_file(self):
        """Check '~/cltk_data/distributed_corpora.yaml' for any custom,
        distributed corpora that the user wants to load locally.

        TODO: write check or try if `cltk_data` dir is not present
        """
        if self.testing:
            distributed_corpora_fp = os.path.expanduser('~/cltk_data/test_distributed_corpora.yaml')
        else:
            distributed_corpora_fp = os.path.expanduser('~/cltk_data/distributed_corpora.yaml')

        try:
            with open(distributed_corpora_fp) as file_open:
                corpora_dict = yaml.safe_load(file_open)
        except FileNotFoundError:
            logger.info('`~/cltk_data/distributed_corpora.yaml` file not found.')
            return []
        except yaml.parser.ParserError as parse_err:
            logger.debug('Yaml parsing error: %s' % parse_err)
            return []

        user_defined_corpora = []
        for corpus_name in corpora_dict:
            about = corpora_dict[corpus_name]

            if about['language'].lower() == self.language:
                user_defined_corpus = dict()
                # user_defined_corpus['git_remote'] = about['git_remote']
                user_defined_corpus['origin'] = about['origin']
                user_defined_corpus['type'] = about['type']
                user_defined_corpus['name'] = corpus_name
                user_defined_corpora.append(user_defined_corpus)

        return user_defined_corpora

    def _setup_language_variables(self):
        """Check for availability of corpora for a language.
        TODO: Make the selection of available languages dynamic from dirs
        within ``corpora`` which contain a ``corpora.py`` file.
        """
        if self.language not in AVAILABLE_LANGUAGES:
            # If no official repos, check if user has custom
            user_defined_corpora = self._check_distributed_corpora_file()
            if user_defined_corpora:
                return user_defined_corpora
            else:
                msg = 'Corpora not available (either core or user-defined) for the "{}" language.'.format(self.language)
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
            corpus_names = [corpus['name'] for corpus in corpora]
            return corpus_names
        except (NameError, KeyError) as error:
            msg = 'Corpus not available for language "{}": {}'.format(self.language, error)
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
            logger.info('Files copied from %s to %s', src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
                logger.info('Files copied from %s to %s', src, dst)
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
            msg = 'Corpus not available for language ' \
                  '"%s": %s' % (self.language, name_error)
            logger.error(msg)
            raise CorpusImportError(msg)
        for corpus_properties in corpora:
            if corpus_properties['name'] == corpus_name:
                return corpus_properties
        msg = 'Corpus "%s" not available for the ' \
              '"%s" language.' % (corpus_name, self.language)
        logger.error(msg)
        raise CorpusImportError(msg)

    def _git_user_defined_corpus(self, corpus_name, corpus_type, uri: str, branch='master'):
        """Clone or update a git repo defined by user.
        TODO: This code is very redundant with what's in import_corpus(),
        could be refactored.
        """
        # git_uri = urljoin('https://github.com/cltk/', corpus_name + '.git')
        # self._download_corpus(corpus_type, corpus_name, path)
        type_dir_rel = os.path.join(CLTK_DATA_DIR, self.language, corpus_type)
        type_dir = os.path.expanduser(type_dir_rel)
        repo_name = uri.split('/')[-1]  # eg, 'latin_corpus_newton_example.git'
        repo_name = repo_name.rstrip('.git')
        target_dir = os.path.join(type_dir, repo_name)
        target_file = os.path.join(type_dir, repo_name, 'README.md')
        # check if corpus already present
        # if not, clone
        if not os.path.isfile(target_file):
            if not os.path.isdir(type_dir):
                os.makedirs(type_dir)
            try:
                msg = "Cloning '{}' from '{}'".format(corpus_name, uri)
                logger.info(msg)
                Repo.clone_from(uri, target_dir, branch=branch, depth=1,
                                progress=ProgressPrinter())
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

    def import_corpus(self, corpus_name, local_path=None, branch='master'):  # pylint: disable=R0912
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
            location = corpus_properties['location']
        except KeyError:
            # git_uri = corpus_properties['git_remote']
            git_name = corpus_properties['']
            git_uri = corpus_properties['origin']
            git_type = corpus_properties['type']
            # pass this off to a special downloader just for custom urls
            self._git_user_defined_corpus(git_name, git_type, git_uri)
            return
        corpus_type = corpus_properties['type']
        if location == 'remote':
            # git_uri = urljoin('https://github.com/cltk/', corpus_name + '.git')
            git_uri = corpus_properties['origin']
            type_dir_rel = os.path.join(CLTK_DATA_DIR, self.language, corpus_type)
            type_dir = os.path.expanduser(type_dir_rel)
            target_dir = os.path.join(type_dir, corpus_name)
            target_file = os.path.join(type_dir, corpus_name, 'README.md')
            # check if corpus already present
            # if not, clone
            if not os.path.isfile(target_file):
                if not os.path.isdir(type_dir):
                    os.makedirs(type_dir)
                try:
                    msg = "Cloning '{}' from '{}'".format(corpus_name, git_uri)
                    logger.info(msg)
                    Repo.clone_from(git_uri, target_dir, branch=branch, depth=1,
                                    progress=ProgressPrinter())
                except CorpusImportError as corpus_imp_err:
                    msg = "Git clone of '{}' failed: '{}'".format(git_uri, corpus_imp_err)
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
                    msg = "Git pull of '{}' failed: '{}'".format(git_uri, corpus_imp_err)
                    logger.error(msg)
        elif location == 'local':
            msg = "Importing from local path: '{}'".format(local_path)
            logger.info(msg)
            if corpus_name in ('phi5', 'phi7', 'tlg'):
                if corpus_name == 'phi5':
                    # normalize path for checking dir
                    if local_path.endswith('/'):
                        local_path = local_path[:-1]
                    # check for right corpus dir
                    if os.path.split(local_path)[1] != 'PHI5':
                        logger.info("Directory must be named 'PHI5'.")
                if corpus_name == 'phi7':
                    # normalize local_path for checking dir
                    if local_path.endswith('/'):
                        local_path = local_path[:-1]
                    # check for right corpus dir
                    if os.path.split(local_path)[1] != 'PHI7':
                        logger.info("Directory must be named 'PHI7'.")
                if corpus_name == 'tlg':
                    # normalize path for checking dir
                    if local_path.endswith('/'):
                        local_path = local_path[:-1]
                    # check for right corpus dir
                    if os.path.split(local_path)[1] != 'TLG_E':
                        logger.info("Directory must be named 'TLG_E'.")
                # move the dir-checking commands into a function
                data_dir = os.path.expanduser(CLTK_DATA_DIR)
                originals_dir = os.path.join(data_dir, 'originals')
                # check for `originals` dir; if not present mkdir
                if not os.path.isdir(originals_dir):
                    os.makedirs(originals_dir)
                    msg = "Wrote directory at '{}'.".format(originals_dir)
                    logger.info(msg)
                tlg_originals_dir = os.path.join(data_dir,
                                                 'originals',
                                                 corpus_name)
                # check for `originals/<corpus_name>`; if pres, delete
                if os.path.isdir(tlg_originals_dir):
                    shutil.rmtree(tlg_originals_dir)
                    msg = "Removed directory at '{}'.".format(tlg_originals_dir)
                    logger.info(msg)
                # copy_dir requires that target
                if not os.path.isdir(tlg_originals_dir):
                    self._copy_dir_recursive(local_path, tlg_originals_dir)


if __name__ == '__main__':
    c = CorpusImporter('latin')
    # print(c.list_corpora)
    c.import_corpus('latin_training_set_sentence_cltk')
