"""Module for lemmatizing Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import os
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set, Any, Generator
import reprlib

from cltk.lemmatize.ensemble import EnsembleDictLemmatizer, EnsembleRegexpLemmatizer, EnsembleUnigramLemmatizer
from cltk.lemmatize.latin.latin import latin_sub_patterns

from cltk.utils.file_operations import open_pickle

# Create CollatinusLemmatizer as subclass of NLTK's Sequential Backoff Tagger

from cltk.lemmatize.backoff import DictLemmatizer

try:
    from pycollatinus import Lemmatiseur
except ImportError as error:
    print(error.__class__.__name__ + ": " + error.message)

from pprint import pprint

class CollatinusLemmatizer(EnsembleDictLemmatizer):
    def __init__(self: object, backoff: object = None, source: str = None, verbose: bool = False):
        """Setup for CollatinusLemmatizer()."""
        self.tagger = Lemmatiseur()

        # Use Collatinus to create dictionary for DictLemmatizer
        super().__init__(lemmas={}, backoff=backoff, source='Collatinus output')

    def lemmatize(self: object, tokens: List[str], normalize=True):
        from cltk.stem.latin.j_v import JVReplacer
        replacer = JVReplacer()

        new_tokens = [token for token in tokens if token not in self.lemmas.keys()]
        text = " ".join([token.lower() for token in tokens]) # lower necessary?
        results = self.tagger.lemmatise_multiple(text)
        # print(results)
        hits = [list(set([r['lemma'] for r in result])) for result in results]

        # Handle punctuation ignored by Collatinus
        punctuation ="\"#$%&\'()*+,-/<=>@[\]^_`{|}~«»—!?;:."

        hits_ = []
        offset = 0
        for i, token in enumerate(tokens):
            if token in punctuation:
                hits_.append(token)
                offset += 1
            else:
                if normalize==True:
                    hits_.append([replacer.replace(hit) for hit in hits[i+offset]])
                else:
                    hits_.append(hits[i+offset])

        lemma_pairs = zip(tokens, hits_)
        self.lemmas.update(lemma_pairs)
        return self.tag(tokens)

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """DOC STRING
        :rtype: str
        :param tokens: List of tokens to be lemmatized
        :param index: Int with current token
        :param history: List with tokens that have already been lemmatized; NOT USED
        """

        keys = self.lemmas.keys()
        if tokens[index] in keys:
            hits = self.lemmas[tokens[index]]
            hits = list(set(hits))
            hits = [(hit, 1/len(hits)) for hit in hits]
            return hits if hits else None

    def __repr__(self: object):
        if self.source:
            return f'<{type(self).__name__}: {self.source}>'
        else:
            return f'<{type(self).__name__}: {self.repr.repr(self.lemmas)}>'

class EnsembleLatinLemmatizer(object):
    """Suggested ensemble chain; SUPER BETA
    """

    models_path = os.path.normpath(get_cltk_data_dir() + '/latin/model/latin_models_cltk/lemmata/backoff')

    def __init__(self: object, train: List[list] = None, seed: int = 3, verbose: bool = False):
        self.models_path = EnsembleLatinLemmatizer.models_path

        missing_models_message = "EnsembleLatinLemmatizer requires the ```latin_models_cltk``` to be in cltk_data. Please load this corpus."

        try:
            self.train =  open_pickle(os.path.join(self.models_path, 'latin_pos_lemmatized_sents.pickle'))
            self.LATIN_OLD_MODEL =  open_pickle(os.path.join(self.models_path, 'latin_lemmata_cltk.pickle'))
            self.LATIN_MODEL =  open_pickle(os.path.join(self.models_path, 'latin_model.pickle'))
        except FileNotFoundError as err:
            raise type(err)(missing_models_message)

        self.latin_sub_patterns = latin_sub_patterns # Move to latin_models_cltk

        self.seed = seed
        self.VERBOSE=verbose

        def _randomize_data(train: List[list], seed: int):
            import random
            random.seed(seed)
            random.shuffle(train)
            pos_train_sents = train[:4000]
            lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
            train_sents = lem_train_sents[:4000]
            test_sents = lem_train_sents[4000:5000]

            return pos_train_sents, train_sents, test_sents

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(self.train, self.seed)
        self._define_lemmatizer()

    def _define_lemmatizer(self: object):
        # Suggested backoff chain--should be tested for optimal order
        self.backoff0 = None
        self.backoff1 = EnsembleRegexpLemmatizer(self.latin_sub_patterns, source='CLTK Latin Regex Patterns', backoff=self.backoff0, verbose=self.VERBOSE)
        self.backoff2 = EnsembleUnigramLemmatizer(self.train_sents, source='CLTK Sentence Training Data', backoff=self.backoff1, verbose=self.VERBOSE)
        self.backoff3 = EnsembleDictLemmatizer(lemmas=self.LATIN_MODEL, source='Latin Model', backoff=self.backoff2, verbose=self.VERBOSE)
        self.backoff4 = CollatinusLemmatizer(backoff=self.backoff3, verbose=self.VERBOSE)
        self.lemmatizer = self.backoff4

    def _extract_lemma_scores(self, ensemble_lemmas):
        lemma_scores = []
        for token, lemma in ensemble_lemmas:
            lemma_scores_ = []
            for lemma_ in lemma:
                for value in lemma_.values():
                    for value_ in value:
                        lemma_scores_.append(value_)
            lemma_scores.append(lemma_scores_)
        return lemma_scores

    def _get_all_matches(self, lemma):
        # https://stackoverflow.com/a/35344958/1816347
        return sorted(set([lemma_[0] for lemma_ in lemma]))

    def _get_ranked_matches(self, lemma):
        # https://stackoverflow.com/a/35344958/1816347
        values_by_key = defaultdict(list)
        for k, v in lemma:
            values_by_key[k].append(v)
        means = sorted([(k, sum(v) / len(v)) for k, v in values_by_key.items()], key=lambda x:x[1], reverse=True)
        return means if means else [(None, 0)]

    def _get_max_ranked_matches(self, lemma):
        ranked_matches = self._get_ranked_matches(lemma)
        return max(ranked_matches, key=lambda x: x[1])[0]

    def _return_lemma_pairs(self, tokens, lemmas):
        return list(zip(tokens, lemmas))

    def lemmatize(self: object, tokens: List[str]):
        lemmas = self.lemmatizer.lemmatize(tokens)
        lemma_scores = self._extract_lemma_scores(lemmas)
        output_lemmas = [self._get_max_ranked_matches(lemma_score) for lemma_score in lemma_scores]
        return self._return_lemma_pairs(tokens, output_lemmas)

    # def evaluate(self: object):
    #     if self.VERBOSE:
    #         raise AssertionError("evaluate() method only works when verbose: bool = False")
    #     return self.lemmatizer.evaluate(self.test_sents)

    def __repr__(self: object):
        return f'<EnsembleLatinLemmatizer v0.1>'

if __name__ == '__main__':
    from cltk.tokenize.latin.word import WordTokenizer


    from cltk.stem.latin.j_v import JVReplacer

    def preprocess(text):
        import html
        replacer = JVReplacer()
        text = html.unescape(text) # Handle html entities
        text = re.sub(r'&nbsp;?', ' ',text) # &nbsp; stripped incorrectly in corpus?
        text = re.sub(r'\x00', ' ',text) # Another space problem?
        text = text.lower()
        text = replacer.replace(text) # Normalize u/v & i/j
        punctuation ="\"#$%&\'()*+,-/<=>@[\]^_`{|}~«»—!?;:."
        translator = str.maketrans({key: " " for key in punctuation})
        text = text.translate(translator)
        translator = str.maketrans({key: " " for key in '0123456789'})
        text = text.translate(translator)
        ends = '!?;:'
        translator = str.maketrans({key: "." for key in ends})
        text = text.translate(translator)
        text = re.sub('[ ]+', ' ', text) # Remove double spaces
        text = re.sub('\s+\n+\s+','\n', text) # Remove double lines and trim spaces around new lines
        return text.strip()

    text = """Hesterno die, patres conscripti, cum me et vestra dignitas et frequentia equitum Romanorum praesentium, quibus senatus dabatur, magno opere commosset, putavi mihi reprimendam esse P. Clodi impudicam impudentiam, cum is publicanorum causam stultissimis interrogationibus impediret, P. Tullioni Syro navaret operam atque ei se, cui totus venierat, etiam vobis inspectantibus venditaret. Itaque hominem furentem exsultantemque continui simul ac periculum iudici intendi: duobus inceptis verbis omnem impetum gladiatoris ferociamque compressi.  Ac tamen ignarus ille qui consules essent, exsanguis #atque aestuans se ex curia repente proripuit, cum quibusdam fractis iam atque inanibus minis et cum illius Pisoniani temporis Gabinianique terroribus: quem cum egredientem insequi coepissem, cepi equidem fructum maximum et ex consurrectione omnium vestrum et ex comitatu publicanorum. Sed vaecors repente sine suo vultu, sine colore, sine voce constitit; deinde respexit et, simul atque Cn. Lentulum consulem aspexit, concidit in curiae paene limine; recordatione, credo, Gabini sui desiderioque Pisonis. Cuius ego de ecfrenato et praecipiti furore quid dicam? <An> potest gravioribus a me verbis vulnerari quam est statim in facto ipso a gravissimo viro, P. Servilio, confectus ac trucidatus? cuius si iam vim et gravitatem illam singularem ac paene divinam adsequi possem, tamen non dubito quin ea tela quae coniecerit inimicus quam ea quae conlega patris emisit leviora atque hebetiora esse videantur.
    """

    text = preprocess(text)
    tokenizer = WordTokenizer()
    tokens = tokenizer.tokenize(text)
    ell = EnsembleLatinLemmatizer(seed=5, verbose=True)
    lemmas = ell.lemmatize(tokens)
    # coll = CollatinusLemmatizer()
    # lemmas = coll.lemmatize(tokens)
    pprint(lemmas)
    # lemmas = coll.lemmatize('arma virumque cano'.split())
    # pprint(lemmas)
    comb = ''
    for item in lemmas:
        if item[1]:
            comb += item[1] + ' '
        else:
            comb += 'UNK '
    print(comb)
