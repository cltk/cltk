
from cltk.tokenize.word import WordTokenizer
from cltk.stop.arabic.stops import STOPS_LIST as ARABIC_STOPS
import cltk.corpus.arabic.utils.pyarabic.araby as araby

def stopwords_filter(string):

    text = string
    # strip tashkeel because the stop words list contains voweled words
    text = araby.strip_tashkeel(text)
    word_tokenizer = WordTokenizer("arabic")
    tokens = word_tokenizer.tokenize(text)

    # filter stop words
    no_stops = [w for w in tokens if w not in ARABIC_STOPS]

    return no_stops
