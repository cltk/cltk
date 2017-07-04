
from cltk.tokenize.word import WordTokenizer
from cltk.stop.arabic.stops import STOPS_LIST as ARABIC_STOPS
from cltk.utils.cltk_logger import logger

try:
    import pyarabic.araby as araby
except ImportError:
    logger.info('Arabic not supported. Install `pyarabic` library to strip diacritics.')
    pass

def stopwords_filter(string):

    text = string
    # strip tashkeel because the stop words list contains voweled words
    text = araby.strip_tashkeel(text)
    word_tokenizer = WordTokenizer("arabic")
    tokens = word_tokenizer.tokenize(text)

    # filter stop words
    no_stops = [w for w in tokens if w not in ARABIC_STOPS]

    return no_stops
