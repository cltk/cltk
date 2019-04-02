

__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

"""
Stemming present a significant challenge in ME, as it is exceptionally
difficult to account for the orthographical variations sometimes even
occurring within a single text. The affix algorithm attempts to account
for variations in spelling, but still Mostly relies on a relatively narrow
hard-coded list (Middle English Dictionary(MED) https://quod.lib.umich.edu/m/med/)

  TODO: Improve on the affix stemmer by implementing an accurate spell checker
  TODO: Implement a stochastic algorithm/Implement overarching stemmer class
"""

SUFFIXES = ['rightes', 'eresse', 'kinnes', 'lechen', 'licher', 'linges', 'lokest', 'longes', 'wardes', 'atour', 'aunce',
            'enger', 'estre', 'evous', 'iende', 'iinde', 'istre', 'ivous', 'lesse', 'liche', 'liece', 'liest', 'lyese',
            'nesce', 'neshe', 'nissa', 'nisse', 'omlie', 'right', 'somes', 'trice', 'eren', 'erie', 'acle', 'ager',
            'aten', 'atif', 'aunt', 'cund', 'elet', 'ende', 'erel', 'esse', 'fold', 'ible', 'ical', 'ieth', 'inde',
            'ioun', 'ious', 'iple', 'laes', 'laus', 'leas', 'lech', 'lese', 'lice', 'ling', 'long', 'lous', 'lyas',
            'ment', 'most', 'nece', 'rede', 'ship', 'soum', 'uous', 'ward', 'ade', 'age', 'ail', 'ain', 'air', 'and',
            'ard', 'ari', 'dom', 'ede', 'els', 'eon', 'ere', 'est', 'eth', 'eur', 'ful', 'gat', 'hed', 'ial', 'ien',
            'ier', 'ild', 'ing', 'ise', 'ish', 'ist', 'ith', 'kin', 'lac', 'les', 'leu', 'lez', 'læs', 'mel', 'mor',
            'nes', 'nez', 'oir', 'orn', 'oun', 'our', 'ous', 'som', 'ure', 'wil', 'al', 'an', 'ar', 'at', 'ed', 'el',
            'en', 'er', 'es', 'et', 'fi', 'if', 'ik', 'il', 'in', 'ir', 'it', 'li', 'ok', 'om', 'on', 'ot', 're', 'se',
            'te', 'th', 'ti', 'ur']

PREFIXES = ['yester', 'yister', 'yistyr', 'yistyr', 'yuster', 'forth', 'yond', 'eth', 'toe', 'too', 'tou', 'tow', 'tuo',
            'two', 'at', 'ef', 'et', 'ex', 'ta', 'te', 'th', 'to', 'tu']

# Used for attaching endings to suffixes, catches more orthographical variations (e.g 'ir', 'ire')
ENDS = ['', 's', 'e', 'en', 'es']

# User-defined exception dictionary
exceptions = dict()


def affix_stemmer(words, exception_list=exceptions, strip_pref = True, strip_suf = True):
    """
    :param words: string list

    The affix stemmer works by rule-based stripping. It can work on prefixes,

    >>> affix_stemmer(['yesterday', 'yesterdom', 'yisterweek'])
    'day dom week'

    suffixes,

    >>> affix_stemmer(['likingnes', 'armlich', 'heighli'])
    'liking arm heigh'

    or both

    >>> affix_stemmer(['yisterdayes'])
    'day'

    You can also define whether the stemmer will strip suffixes

    >>> affix_stemmer(['yisterdayes'], strip_suf = False)
    'dayes'

    or prefixes

    >>> affix_stemmer(['yisterdayes'], strip_pref = False)
    'yisterday'

    The stemmer also accepts a user-defined dictionary, that essentially serves
    the function of a dictionary look-up stemmer

    >>> affix_stemmer(['arisnesse'], exception_list = {'arisnesse':'rise'})
    'rise'

    :exception_list:
    :return: string
    """

    for i, w in enumerate(words):

        try:
            words[i] = exception_list[w]

        except:
            if len(w) <= 4:
                continue

            word = w

            if strip_pref:

                for prefix in PREFIXES:
                    if word.startswith(prefix):
                        word = word[len(prefix):]
                        break

            if strip_suf:

                for en in ENDS:

                    if len(word) <= 4:
                        break

                    # Strip suffixes
                    for suffix in SUFFIXES:

                        if len(suffix) <= len(en):
                            break

                        if (word + en).endswith(suffix):
                            word = word[:-len(suffix) + len(en)]
                            break

                    if len(word) <= 4:
                        break

            words[i] = word

    return " ".join(words)
