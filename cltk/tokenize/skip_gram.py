import itertools
from nltk import ngrams

def skipgrams(sequence, n, k):
    for ngram in ngrams(sequence, n + k, pad_right=True):
        head = ngram[:1]
        tail = ngram[1:]
        for skip_tail in itertools.combinations(tail, n - 1):
            if skip_tail[-1] is None:
                continue
            yield head + skip_tail
