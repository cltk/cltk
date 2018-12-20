from cltk.tag.pos import POSTag

from cltk.corpus.old_english.alphabet import VOWELS
from cltk.corpus.old_english.alphabet import LONG_VOWELS
from cltk.corpus.old_english.alphabet import CONSONANTS

tagger = POSTag('old_english')

DIPHTHONGS = ['th', 'sc', 'ng', 'cg']


def syllabify(w):
    """
    Syllabify OE word based on Onset Maximisation:

    -Clusters of the form VCV are always partitioned as V-CV
    - In case of VCCV clusters, the following are partitioned as V-CCV
        - 'th' (considered the allophone of graphemes ⟨þ⟩ and ⟨ð⟩
        - 'sc'
        - 'ng'
        - 'cg'

    :param w: Word to be syllabified
    :return: Syllabified word
    """
    syllables = []

    for i, c in enumerate(w[1:-1]):
        if c in CONSONANTS and w[i] in VOWELS and w[i+2] in VOWELS:
            syllables.append(i)
        if c in CONSONANTS and w[i] in VOWELS and w[i+2] in CONSONANTS:
            if c + w[i+2] in DIPHTHONGS:
                syllables.append(i)
            else:
                syllables.append(i+1)

    for n, k in enumerate(syllables):
        w = w[:k + n + 1] + "." + w[k + n + 1:]

    w = w.split('.')

    if sum([x in VOWELS for x in w[-1]]) == 0:
        w[-2] = w[-2] + w[-1]
        w = w[:-1]

    return w

def syllable_quantity(syl):
    """
    Return the syllable quantity:

    Long syllables: CVC, CVV, CVVC
    Short syllables: CV
    :param syl:
    :return:
    """

    if syl[-1] in VOWELS and syl[-2] in VOWELS: return 'LONG'
    if syl[-1] in CONSONANTS and syl[-2] in VOWELS: return 'LONG'
    if syl[-2] in VOWELS and syl[-1] in VOWELS: return 'LONG'
    if syl[-1] in LONG_VOWELS: return 'LONG'

    return 'SHORT'


def stress_pos(text):
    """
    Rule-based stresser for Old English, taking into consideration the
    POS as tagged by CLTK's trained perceptron tagger.

    Note that the accuracy of the syllabifier is directly tied to that of
    the tagger.

    Primary stress rules in Old English are relatively simple:

    - Compound words receive stress on the first component

    - Verbal prefixes are never stressed

    - 'ge-', 'be-' and 'for-' are never stressed

    - Every other word receives primary stress on the first syllable
    """

    tagged_text = tagger.tag_crf(text)
    f_text = []

    for token, pos in tagged_text:

        #Ignore conjuctions
        if pos == 'C-':
            continue

        syl_token = syllabify(token.lower())
        # if word is a verb, then receive stress on the second syllable
        if pos is 'V-' and len(syl_token) > 1:
            syl_token[1] = '\'' + syl_token[1]

        # if suffix is either of 'ge-', 'be-', 'for-', receive stress on second syllable
        elif (token[:2] in ['ge', 'be', 'þe'] or token[:3] is 'for') and len(syl_token) > 1:
            syl_token[1] = '\'' + syl_token[1]

        # else receive stress on the first syllable
        else:
            syl_token[0] = '\'' + syl_token[0]

        # monosyllabic words aren't stressed
        if len(syl_token) == 1:
            f_text.append(token.lower())
        else:
            # finally formatting
            syl_token = '.'.join(syl_token)
            f_text.append(syl_token)

    return f_text
