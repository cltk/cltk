"""`download_test_corpora.py` - helper class to download test corpora."""
import logging

from cltk.corpus.utils.importer import CorpusImporter

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

logging.basicConfig(level=logging.INFO)


try:
    corpus_importer = CorpusImporter('latin')
    corpus_importer.import_corpus('latin_text_latin_library')
except:
    LOG.exception('Failure to download test corpus')

# TODO add other corpora as necessary
