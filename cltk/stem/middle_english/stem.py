

__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

"""
Stemming present a significant challenge in ME, as it is exceptionally difficult to account for the orthographical
 variations sometimes even occurring within a single text. The affix algorithm attempts to account for variations in
 spelling, but still Mostly relies on a relatively narrow hard-coded list (Middle English Dictionary(MED)
 https://quod.lib.umich.edu/m/med/).
  TODO: Improve on the affix stemmer by implementing an accurate spell checker (Levenshtein Automata?)
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
            'te', 'th', 'ti', 'ur', 'e', 'i', 'k', 'n', 't']

PREFIXES = ['yester', 'yister', 'yistyr', 'yistyr', 'yuster', 'forth', 'yond', 'eth', 'toe', 'too', 'tou', 'tow', 'tuo',
            'two', 'at', 'ef', 'et', 'ex', 'ta', 'te', 'th', 'to', 'tu', 'i', 'y']

#User-defined exception dictionary
exceptions = dict()

def affix_stemmer(words, exception_list = exceptions):
    """
    :param words: string list
    :return: string list
    """

    for i, w in enumerate(words):

        try:
            words[i] = exception_list[w]

        except:
            if len(w) <=4:
                continue

            word = w

            for prefix in PREFIXES:
                if word.startswith(prefix):
                    word = word[len(prefix):]
                    break

            for en in ['', 's', 'e', 'en', 'es']:

                if len(word) <= 4:
                    break

                # Strip suffixes
                for suffix in SUFFIXES:

                    if len(suffix) <= len(en):
                        break

                    if (word + en).endswith(suffix):
                        word = word[:-len(suffix)+len(en)]
                        break

                if len(word) <= 4:
                    break

            words[i] = word

    return words
    