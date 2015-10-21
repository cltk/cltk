
import logging
import os
import time

from cltk.corpus.utils.formatter import phi5_plaintext_cleanup
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.stop.latin.stops import STOPS_LIST as latin_stops
from cltk.tokenize.word import nltk_tokenize_words
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer
from gensim.models import Word2Vec


def gen_docs(corpus, lemmatize, rm_stops):
    """Open and process files from a corpus. Return a list of sentences for an author. Each sentence
    is itself a list of tokenized words.
    """

    assert corpus in ['phi5', 'tlg']

    if corpus == 'phi5':
        language = 'latin'
        filepaths = assemble_phi5_author_filepaths()
        jv_replacer = JVReplacer()
        text_cleaner = phi5_plaintext_cleanup
        word_tokenizer = nltk_tokenize_words
        if rm_stops:
            stops = latin_stops
        else:
            stops = None
    elif corpus == 'tlg':
        language = 'greek'
        filepaths = assemble_tlg_author_filepaths()
        text_cleaner = tlg_plaintext_cleanup
        word_tokenizer = nltk_tokenize_words

        if rm_stops:
            stops = latin_stops
        else:
            stops = None

    if lemmatize:
        lemmatizer = LemmaReplacer(language)

    sent_tokenizer = TokenizeSentence(language)

    for filepath in filepaths:
        with open(filepath) as f:
            text = f.read()
        # light first-pass cleanup, before sentence tokenization (which relies on punctuation)
        text = text_cleaner(text, rm_punctuation=False, rm_periods=False)
        sent_tokens = sent_tokenizer.tokenize_sentences(text)
        #doc_sentences = []
        for sentence in sent_tokens:
            # a second cleanup at sentence-level, to rm all punctuation
            sentence = text_cleaner(sentence, rm_punctuation=True, rm_periods=True)
            sentence = word_tokenizer(sentence)
            sentence = [s.lower() for s in sentence]
            sentence = [w for w in sentence if w]
            if language == 'latin':
                sentence = [w[1:] if w.startswith('-') else w for w in sentence]

            if stops:
                sentence = [w for w in sentence if w not in stops]

            sentence = [w for w in sentence if len(w) > 1]  # rm short words

            if sentence:
                sentence = sentence

            if lemmatize:
                sentence = lemmatizer.lemmatize(sentence)
            if sentence and language == 'latin':
                sentence = [jv_replacer.replace(word) for word in sentence]
            if sentence != []:
                yield sentence
                #doc_sentences.append(sentence)
        #if doc_sentences != []:
        #    yield doc_sentences


def make_model(corpus, lemmatize=False, rm_stops=False, size=100, window=10, min_count=5, workers=4, sg=1, save_path=None):
    """Train W2V model."""

    # Simple training, with one large list
    t0 = time.time()

    sentences_stream = gen_docs(corpus, lemmatize=lemmatize, rm_stops=rm_stops)
    #sentences_list = []
    #for sent in sentences_stream:
    #    sentences_list.append(sent)

    model = Word2Vec(sentences=list(sentences_stream), size=size, window=window, min_count=min_count, workers=workers, sg=sg)

    '''
    # Step 0: Instantiate empty model ( https://groups.google.com/forum/#!topic/gensim/xXKz-v8brAI )
    model = Word2Vec(sentences=None, size=size, window=window, min_count=min_count, workers=workers, sg=sg)

    # Step 1: Add entire corpus's vocabulary to the model. Stream sentences.
    sentences_stream = gen_docs(corpus, lemmatize=lemmatize, rm_stops=rm_stops)
    vocab_counter = 0
    alert_per_processed = 10000
    for sentences in sentences_stream:
        vocab_counter += 1
        model.build_vocab(sentences)
        if vocab_counter % alert_per_processed == 0:
            print('Building vocab. Sentence #:', vocab_counter)

    # Step 2: Train model sentence-by-sentence. Again, stream sentences.
    sentences_stream = gen_docs(corpus, lemmatize=lemmatize, rm_stops=rm_stops)
    train_counter = 0
    for sentences in sentences_stream:
        train_counter += 1
        if train_counter % alert_per_processed == 0:
            print('Training model. Sentence #:', train_counter)
        try:
            model.train(sentences)
        except Exception as e:
            print(e)
    '''

    # "Trim" the model of unnecessary data. Model cannot be updated anymore.
    model.init_sims(replace=True)

    if save_path:
        save_path = os.path.expanduser(save_path)
        model.save(save_path)

    print('Total training time for {0}: {1} minutes'.format(save_path, (time.time() - t0) / 60))


if __name__ == '__main__':
    #filepath = os.path.expanduser('~/latin_word2vec_cltk/latin_s100_w30_min5_sg.model')
    #make_model('phi5', lemmatize=False, rm_stops=True, size=100, window=30, min_count=5, workers=4, sg=0, save_path=filepath)

    filepath = os.path.expanduser('~/latin_word2vec_cltk/latin_s100_w30_min5_sg_lemmed.model')
    make_model('phi5', lemmatize=True, rm_stops=True, size=100, window=30, min_count=5, workers=4, sg=0, save_path=filepath)

    filepath = os.path.expanduser('~/greek_word2vec_cltk/greek_s100_w30_min5_sg.model')
    make_model('tlg', lemmatize=False, rm_stops=True, size=100, window=30, min_count=5, workers=4, sg=0, save_path=filepath)

    filepath = os.path.expanduser('~/greek_word2vec_cltk/greek_s100_w30_min5_sg_lemmed.model')
    make_model('tlg', lemmatize=True, rm_stops=True, size=100, window=30, min_count=5, workers=4, sg=0, save_path=filepath)
