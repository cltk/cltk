"""CLTK corpus and software importer. Remote `.tar.gz` files are saved in
`~/cltk_data/originals`, then unpacked into its fitting directory. Indices of
available corpora are available in, e.g.: `cltk/corpora/greek/corpora.py`.
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>',
]
__license__ = 'MIT License. See LICENSE.'

from cltk.corpus import CLTK_DATA_DIR
from cltk.corpus.greek.corpora import GREEK_CORPORA
from cltk.corpus.latin.corpora import LATIN_CORPORA
# from cltk.corpus.cltk_logging import logger
import errno
import os
import requests
from requests_toolbelt import SSLAdapter
import shutil
import ssl
import sys
from urllib.parse import urlsplit


def list_corpora(language):
    """Print to screen corpora available to the CLTK. Invoke with, e.g.:
    `list_corpora('latin')`.

    :param language: str
    """
    if language == 'greek':
        corpora = GREEK_CORPORA
    elif language == 'latin':
        corpora = LATIN_CORPORA
    else:
        pass
        #logger.info('No corpora available for this language.')
    #logger.info('Available CLTK corpora for %s:' % language)
    # [logger.info(corpus['name']) for corpus in corpora]
    corpora_list = []
    for corpus in corpora:
        corpora_list.append(corpus['name'])
    return corpora_list


def make_dirs(language, corpus_type, corpus_name):
    """Make directories for an incoming corpus.
    # TODO: Check if tuple is right return type.

    :param language: str
    :param corpus_type: str
    :param corpus_name: str
    :rtype : tuple
    """
    home_rel = CLTK_DATA_DIR
    home = os.path.expanduser(home_rel)
    # make originals dir for saving downloaded file
    originals_dir = os.path.join(home, 'originals')
    if not os.path.isdir(originals_dir):
        os.makedirs(originals_dir)
        #logger.info('Wrote directory at: %s' % originals_dir)
    else:
        pass
        #logger.info('Directory already exists at: %s' % originals_dir)
    # make directories for unpacking downloaded file
    unpack_dir = os.path.join(home, language, corpus_type, corpus_name)
    if not os.path.isdir(unpack_dir):
        os.makedirs(unpack_dir)
        #logger.info('Wrote directories at: %s' % unpack_dir)
    else:
        pass
        #logger.info('Directories already exist at: %s' % unpack_dir)
    return originals_dir, unpack_dir


def save_untar(url, downloaded_object, originals_dir, unpack_dir, corpus_name):
    """Write downloaded tar object and unpack.

    :param url: str
    :param downloaded_object: str
    :param originals_dir: str
    :param unpack_dir: str
    :param corpus_name: str
    """
    # get filename from URL
    file_name = urlsplit(url).path.split('/')[-1]
    file_path_originals = os.path.join(originals_dir, file_name)
    # save into originals file
    try:
        with open(file_path_originals, 'wb') as new_file:
            new_file.write(downloaded_object.content)
            #logger.info('Wrote file %s to %s.' % (file_name, originals_dir))
    except Exception as e:
        pass
        #logger.info('Failed to write file %s to %s: %s' % (file_name, originals_dir, e))
    # unpack into new dir
    try:
        shutil.unpack_archive(file_path_originals, unpack_dir)
        #logger.info('Finished unpacking corpus %s to %s.' % (corpus_name, unpack_dir))
    except Exception as e:
        pass
        #logger.info('Finished unpacking corpus %s to %s: %s' % (corpus_name, unpack_dir, e))


def download_file(url, corpus_name):
    """Download file with SSL.

    :param url: str
    :param corpus_name: str
    :rtype : object
    """
    #logger.info('Starting download of corpus %s from: %s .' % (corpus_name, url))
    try:
        session = requests.Session()
        session.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        downloaded_object = session.get(url, stream=True)
        #logger.info('Downloaded file at %s .' % url)
    except Exception as e:
        pass
        #logger.info('Failed to download file at %s : %s' % (url, e))
    return downloaded_object


def download_corpus(language, corpus_type, corpus_name, url):
    """Download and save incoming data.

    :param language: str
    :param corpus_type: str
    :param corpus_name: str
    :param url: str
    """
    downloaded_object = download_file(url, corpus_name)
    originals_dir, unpack_dir = make_dirs(language, corpus_type, corpus_name)
    save_untar(url, downloaded_object, originals_dir, unpack_dir, corpus_name)


def copy_dir_recursive(src_rel, dst_rel):
    """Copy contents of one directory to another. `dst` dir cannot exist.
    Source: http://stackoverflow.com/a/1994840
    """
    src = os.path.expanduser(src_rel)
    dst = os.path.expanduser(dst_rel)
    print(src)
    print(dst)
    try:
        shutil.copytree(src, dst)
        #logger.info(u'Files copied from {0:s} to {1:s}'.format(src, dst))
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
            #logger.info(u'Files copied from {0:s} to {1:s}'.format(src, dst))
        else:
            raise


#TODO mk singuler
def import_corpus(language, corpus_name, path=None):
    """Download a remote or load local corpus into 'cltk_data'. Invoke with
    e.g. `import_corpora('latin', 'latin_text_latin_library')` or for local
    corpora e.g. `import_corpora('latin', 'latin_text_latin_library', '~/Downloads/corpora/TLG_E/')`.

    :param language: str
    :param corpus_name: str
    :param path: str
    """
    if language == 'greek':
        corpora = GREEK_CORPORA
    elif language == 'latin':
        corpora = LATIN_CORPORA

    corpus_properties = None
    for corpus in corpora:
        if corpus['name'] == corpus_name:
            corpus_properties = corpus
    if not corpus_properties:
        print('Corpus %s not available for the %s language.' % (corpus_name, language))
        sys.exit()
    location = corpus_properties['location']
    corpus_type = corpus_properties['type']
    if location == 'remote':
        path = corpus_properties['path']
        download_corpus(language, corpus_type, corpus_name, path)
    elif location == 'local':
        print('Incoming path:', path)
        if not path:
            print("'path' argument required for local corpora.")
            sys.exit()
        if corpus_name in ('phi5', 'phi7', 'tlg'):
            if corpus_name == 'phi5':
                if path.endswith('/'):  # normalize path for checking dir
                    path = path[:-1]
                if os.path.split(path)[1] != 'PHI5':  # check for right corpus dir
                    print("Directory must be named 'PHI5'.")
                    sys.exit()
            if corpus_name == 'phi7':
                if path.endswith('/'):  # normalize path for checking dir
                    path = path[:-1]
                if os.path.split(path)[1] != 'PHI7':  # check for right corpus dir
                    print("Directory must be named 'PHI7'.")
                    sys.exit()
            if corpus_name == 'tlg':
                if path.endswith('/'):  # normalize path for checking dir
                    path = path[:-1]
                if os.path.split(path)[1] != 'TLG_E':  # check for right corpus dir
                    print("Directory must be named 'TLG_E'.")
                    sys.exit()
            # move the dir-checking commands into a function
            data_dir = os.path.expanduser(CLTK_DATA_DIR)
            originals_dir = os.path.join(data_dir, 'originals')
            # check for `originals` dir; if not present mkdir
            if not os.path.isdir(originals_dir):
                os.makedirs(originals_dir)
                print('Wrote directory at: %s' % originals_dir)
            tlg_originals_dir = os.path.join(data_dir, 'originals', corpus_name)
            # check for `originals/<corpus_name>`; if pres, delete
            if os.path.isdir(tlg_originals_dir):
                shutil.rmtree(tlg_originals_dir)
                print('Removed directory at: %s.' % tlg_originals_dir)
            # copy_dir requires that target
            if not os.path.isdir(tlg_originals_dir):
                copy_dir_recursive(path, tlg_originals_dir)
