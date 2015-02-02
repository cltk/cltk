"""Import CLTK corpora.
TODO: Fix so ``import_corpora()`` can take relative path.
TODO: Add https://github.com/cltk/pos_latin
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus.greek.corpora import GREEK_CORPORA
from cltk.corpus.latin.corpora import LATIN_CORPORA
from cltk.corpus.utils.cltk_logger import logger
import errno
import os
import requests
from requests_toolbelt import SSLAdapter
import shutil
import ssl
import sys
from urllib.parse import urlsplit


AVAILABLE_LANGUAGES = ['greek', 'latin']
CLTK_DATA_DIR = '~/cltk_data'


class CorpusImporter():
    """Import CLTK corpora."""

    def __init__(self, language):
        self.language = language.lower()
        self._setup_language_variables()

    def _setup_language_variables(self):
        """Check for availability of corpora for a language.
        TODO: Make the selection of available languages dynamic from dirs
        within ``corpora`` which contain a ``corpora.py`` file.
        """
        assert self.language in AVAILABLE_LANGUAGES, \
            'Corpora not available for %s language.' % self.language

    @property
    def list_corpora(self):
        """Show corpora available for the CLTK to download."""
        if self.language == 'greek':
            corpora = GREEK_CORPORA
        elif self.language == 'latin':
            corpora = LATIN_CORPORA
        else:
            sys.exit(1)
        corpus_list = []
        for corpus in corpora:
            corpus_list.append(corpus['name'])
        return corpus_list

    def _make_dirs(self, corpus_type, corpus_name):
        """Make directories for an incoming corpus."""
        home_rel = CLTK_DATA_DIR
        home = os.path.expanduser(home_rel)
        # make originals dir for saving downloaded file
        originals_dir = os.path.join(home, 'originals')
        if not os.path.isdir(originals_dir):
            os.makedirs(originals_dir)
            logger.info("Wrote directory at '%s'." % originals_dir)
        else:
            logger.info("Directory already exists at: '%s'." % originals_dir)
        # make directories for unpacking downloaded file
        unpack_dir = os.path.join(home, self.language, corpus_type, corpus_name)
        if not os.path.isdir(unpack_dir):
            os.makedirs(unpack_dir)
            logger.info("Wrote directories at '%s'." % unpack_dir)
        else:
            logger.info("Directories already exist at '%s'." % unpack_dir)
        return originals_dir, unpack_dir

    @staticmethod
    def _save_untar(url, dl_object, originals_dir, unpack_dir, corpus_name):
        """Write downloaded tar object and unpack."""
        # get filename from URL
        file_name = urlsplit(url).path.split('/')[-1]
        file_path_originals = os.path.join(originals_dir, file_name)
        # save into originals file
        try:
            with open(file_path_originals, 'wb') as new_file:
                new_file.write(dl_object.content)
                logger.info("Wrote file %s to '%s'." % (file_name, originals_dir))
        except Exception as except_write:  # pylint: disable=W0703
            logger.error("Failed to write file %s to '%s': %s" %
                         (file_name, originals_dir, except_write))
        # unpack into new dir
        try:
            shutil.unpack_archive(file_path_originals, unpack_dir)
            logger.info("Finished unpacking corpus %s to '%s'." %
                        (corpus_name, unpack_dir))
        except Exception as except_write:  # pylint: disable=W0703
            logger.error("Failed to uncompress corpus %s to '%s': %s" %
                         (corpus_name, unpack_dir, except_write))

    @staticmethod
    def _download_file(url, corpus_name):
        """Download file with SSL. Note: SSL GitHub connections require a
        extra TLSv1 extension to the ``requests`` library's connection.
        TODO: Maybe up max_retries
        http://docs.python-requests.org/en/latest/api/?highlight=max_retries#requests.adapters.HTTPAdapter
        http://stackoverflow.com/a/21371922
        """
        logger.info("Starting download of corpus %s from: '%s'." % (corpus_name, url))
        try:
            session = requests.Session()
            session.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
            downloaded_object = session.get(url, stream=True)
            logger.info("Downloaded file at '%s'." % url)
        except Exception as except_req:  # pylint: disable=W0703
            logger.error("Failed to download file at '%s': %s" % (url, except_req))
            sys.exit(1)
        return downloaded_object

    def _download_corpus(self, corpus_type, corpus_name, url):
        """Download and save incoming data.
        :type corpus_type: str
        :param corpus_type: Type of corpus to be downloaded.
        :type corpus_name: str
        :param corpus_name: Name of corpus to be downloaded.
        :type url: str
        :param url: URL from which to fetch ``tar.gz`` file.
        """
        downloaded_object = self._download_file(url, corpus_name)
        originals_dir, unpack_dir = self._make_dirs(corpus_type, corpus_name)
        self._save_untar(url, downloaded_object, originals_dir, unpack_dir,
                         corpus_name)

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
            logger.info(u'Files copied from {0:s} to {1:s}'.format(src, dst))
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
                logger.info(u'Files copied from {0:s} to {1:s}'.format(src, dst))
            else:
                raise

    def _check_corpus_availability(self, corpus_name):
        """Check whether a corpus is available for import.
        :type corpus_name: str
        :param corpus_name: Name of available corpus.
        :rtype : str
        """
        if self.language == 'greek':
            corpora = GREEK_CORPORA
        elif self.language == 'latin':
            corpora = LATIN_CORPORA
        else:
            logger.error('Corpora not available for %s language.' % self.language)
            sys.exit(1)
        corpus_properties = None
        for corpus in corpora:
            if corpus['name'] == corpus_name:
                corpus_properties = corpus
        if not corpus_properties:
            logger.info("Corpus '%s' not available for the '%s' language." %
                        (corpus_name, self.language))
            sys.exit(1)
        return corpus_properties

    def import_corpus(self, corpus_name, path=None):  # pylint: disable=R0912
        """Download a remote or load local corpus into dir ``~/cltk_data``.
        TODO: Move some if/else logic into own methods.
        :type corpus_name: str
        :param corpus_name: The name of an available corpus.
        :param path: str
        :param path: A filepath, required when importing local corpora.
        """
        corpus_properties = self._check_corpus_availability(corpus_name)
        location = corpus_properties['location']
        corpus_type = corpus_properties['type']
        if location == 'remote':
            path = corpus_properties['path']
            self._download_corpus(corpus_type, corpus_name, path)
        elif location == 'local':
            logger.info('Incoming path:', path)
            if not path:
                logger.info("'path' argument required for local corpora.")
                sys.exit(1)
            if corpus_name in ('phi5', 'phi7', 'tlg'):
                if corpus_name == 'phi5':
                    # normalize path for checking dir
                    if path.endswith('/'):
                        path = path[:-1]
                    # check for right corpus dir
                    if os.path.split(path)[1] != 'PHI5':
                        logger.info("Directory must be named 'PHI5'.")
                        sys.exit(1)
                if corpus_name == 'phi7':
                    # normalize path for checking dir
                    if path.endswith('/'):
                        path = path[:-1]
                    # check for right corpus dir
                    if os.path.split(path)[1] != 'PHI7':
                        logger.info("Directory must be named 'PHI7'.")
                        sys.exit(1)
                if corpus_name == 'tlg':
                    # normalize path for checking dir
                    if path.endswith('/'):
                        path = path[:-1]
                    # check for right corpus dir
                    if os.path.split(path)[1] != 'TLG_E':
                        logger.info("Directory must be named 'TLG_E'.")
                        sys.exit(1)
                # move the dir-checking commands into a function
                data_dir = os.path.expanduser(CLTK_DATA_DIR)
                originals_dir = os.path.join(data_dir, 'originals')
                # check for `originals` dir; if not present mkdir
                if not os.path.isdir(originals_dir):
                    os.makedirs(originals_dir)
                    logger.info("Wrote directory at '%s'." % originals_dir)
                tlg_originals_dir = os.path.join(data_dir,
                                                 'originals',
                                                 corpus_name)
                # check for `originals/<corpus_name>`; if pres, delete
                if os.path.isdir(tlg_originals_dir):
                    shutil.rmtree(tlg_originals_dir)
                    logger.info("Removed directory at '%s'." % tlg_originals_dir)
                # copy_dir requires that target
                if not os.path.isdir(tlg_originals_dir):
                    self._copy_dir_recursive(path, tlg_originals_dir)
