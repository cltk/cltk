"""Helper functions for any word-vector operations.

TODO: Figure out how to log ImportError when building on travis, if gensim not available
TODO: Run Latin W2V again with WordTokenizer().
TODO: Add CLTK logging to this.
"""

import logging
import os
import sys
import time

from cltk.utils.cltk_logger import logger

# TODO: Fix this
# KJ added this to fix failing build on Travis CI. Gensim seems to load boto, which in turn causes an error.
try:
    from gensim.models import Word2Vec
except AttributeError:
    logger.error('Command `from gensim.models import Word2Vec` failed with AttributeError.')


from cltk.corpus.utils.formatter import phi5_plaintext_cleanup
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer # Change lemmatizer
from cltk.stop.latin import STOPS_LIST as latin_stops
from cltk.tokenize.word import WordTokenizer
from cltk.tokenize.sentence import TokenizeSentence
from cltk.tokenize.word import WordTokenizer


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
        word_tokenizer = WordTokenizer('latin')
        if rm_stops:
            stops = latin_stops
        else:
            stops = None
    elif corpus == 'tlg':
        language = 'greek'
        filepaths = assemble_tlg_author_filepaths()
        text_cleaner = tlg_plaintext_cleanup
        word_tokenizer = WordTokenizer('greek')

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
        # doc_sentences = []
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
            if sentence:
                yield sentence
                # doc_sentences.append(sentence)
                # if doc_sentences != []:
                #    yield doc_sentences


def make_model(corpus, lemmatize=False, rm_stops=False, size=100, window=10, min_count=5, workers=4, sg=1,
               save_path=None):
    """Train W2V model."""

    # Simple training, with one large list
    t0 = time.time()

    sentences_stream = gen_docs(corpus, lemmatize=lemmatize, rm_stops=rm_stops)
    # sentences_list = []
    # for sent in sentences_stream:
    #    sentences_list.append(sent)

    model = Word2Vec(sentences=list(sentences_stream), size=size, window=window, min_count=min_count, workers=workers,
                     sg=sg)

    # "Trim" the model of unnecessary data. Model cannot be updated anymore.
    model.init_sims(replace=True)

    if save_path:
        save_path = os.path.expanduser(save_path)
        model.save(save_path)

    print('Total training time for {0}: {1} minutes'.format(save_path, (time.time() - t0) / 60))


def get_sims(word, language, lemmatized=False, threshold=0.70):
    """Get similar Word2Vec terms from vocabulary or trained model.

    TODO: Add option to install corpus if not available.
    """
    # Normalize incoming word string
    jv_replacer = JVReplacer()
    if language == 'latin':
        # Note that casefold() seemingly does not work with diacritic
        # Greek, likely because of it expects single code points, not
        # diacritics. Look into global string normalization to code points
        # for all languages, especially Greek.
        word = jv_replacer.replace(word).casefold()

    model_dirs = {'greek': get_cltk_data_dir() + '/greek/model/greek_word2vec_cltk',
                  'latin': get_cltk_data_dir() + '/latin/model/latin_word2vec_cltk'}
    assert language in model_dirs.keys(), 'Langauges available with Word2Vec model: {}'.format(model_dirs.keys())
    if lemmatized:
        lemma_str = '_lemmed'
    else:
        lemma_str = ''
    model_name = '{0}_s100_w30_min5_sg{1}.model'.format(language, lemma_str)
    model_dir_abs = os.path.expanduser(model_dirs[language])
    model_path = os.path.join(model_dir_abs, model_name)
    try:
        model = Word2Vec.load(model_path)
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print("CLTK's Word2Vec models cannot be found. Please import '{}_word2vec_cltk'.".format(language))
        raise
    try:
        similars = model.most_similar(word)
    except KeyError as key_err:
        print(key_err)
        possible_matches = []
        for term in model.vocab:
            if term.startswith(word[:3]):
                possible_matches.append(term)
        print("The following terms in the Word2Vec model you may be looking for: '{}'.".format(possible_matches))
        return None
    returned_sims = []
    for similar in similars:
        if similar[1] > threshold:
            returned_sims.append(similar[0])
    if not returned_sims:
        print("Matches found, but below the threshold of 'threshold={}'. Lower it to see these results.".format(threshold))
    return returned_sims
