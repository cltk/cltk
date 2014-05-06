import nltk
language_punkt_vars = nltk.tokenize.punkt.PunktLanguageVars
language_punkt_vars.sent_end_chars=('.', '?', ';', ':')


train_data = """

"""

trainer = nltk.tokenize.punkt.PunktTrainer(train_data, language_punkt_vars)
params = trainer.get_params()
sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(params)

for sentence in sbd.sentences_from_text(to_be_tokenized, realign_boundaries=True):
    print(sentence)
    print('---')


or:

# import punkt
import nltk.tokenize.punkt

# Make a new Tokenizer
tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

# Read in trainings corpus (one example: Slovene)
import codecs
text = codecs.open("slovene.plain","Ur","iso-8859-2").read()

# Train tokenizer
tokenizer.train(text)

# Dump pickled tokenizer
import pickle
out = open("slovene.pickle","wb")
pickle.dump(tokenizer, out)
out.close()

###########


# http://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.punkt

In [1]: import nltk.data

In [2]: s = """Multum tibi esse animi scio; nam etiam antequam instrueres te praeceptis salutaribus et dura vincentibus, satis adversus fortunam placebas tibi, et multo magis postquam cum illa manum conseruisti viresque expertus es tuas, quae numquam certam dare fiduciam sui possunt nisi cum multae difficultates hinc et illinc apparuerunt, aliquando vero et propius accesserunt. Sic verus ille animus et in alienum non venturus arbitrium probatur; haec eius obrussa est. Non potest athleta magnos spiritus ad certamen afferre qui numquam suggillatus est: ille qui sanguinem suum vidit, cuius dentes crepuere sub pugno, ille qui subplantatus ad versarium toto tulit corpore nec proiecit animum proiectus, qui quotiens cecidit contumacior resurrexit, cum magna spe descendit ad pugnam. Ergo, ut similitudinem istam prosequar, saepe iam fortuna supra te fuit, nec tamen tradidisti te, sed subsiluisti et acrior constitisti; multum enim adicit sibi virtus lacessita."""

In [4]: sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    # this looks at:  'tokenizers/punkt/english.pickle'


In [8]: print('\n-----\n'.join(sent_detector.tokenize(s.strip())))
Multum tibi esse animi scio; nam etiam antequam instrueres te praeceptis salutaribus et dura vincentibus, satis adversus fortunam placebas tibi, et multo magis postquam cum illa manum conseruisti viresque expertus es tuas, quae numquam certam dare fiduciam sui possunt nisi cum multae difficultates hinc et illinc apparuerunt, aliquando vero et propius accesserunt.
-----
Sic verus ille animus et in alienum non venturus arbitrium probatur; haec eius obrussa est.
-----
Non potest athleta magnos spiritus ad certamen afferre qui numquam suggillatus est: ille qui sanguinem suum vidit, cuius dentes crepuere sub pugno, ille qui subplantatus ad versarium toto tulit corpore nec proiecit animum proiectus, qui quotiens cecidit contumacior resurrexit, cum magna spe descendit ad pugnam.
-----
Ergo, ut similitudinem istam prosequar, saepe iam fortuna supra te fuit, nec tamen tradidisti te, sed subsiluisti et acrior constitisti; multum enim adicit sibi virtus lacessita.


####

import pickle

In [13]: with open('/Users/kyle/nltk_data/tokenizers/punkt/english.pickle', 'rb') as f:
    r = f.read()
   ....:

In [14]: up = pickle.loads(r)

In [15]: up
Out[15]: <nltk.tokenize.punkt.PunktSentenceTokenizer at 0x105b1a630>

In [19]: help(up)

Help on PunktSentenceTokenizer in module nltk.tokenize.punkt object:

class PunktSentenceTokenizer(PunktBaseClass, nltk.tokenize.api.TokenizerI)
 |  A sentence tokenizer which uses an unsupervised algorithm to build
 |  a model for abbreviation words, collocations, and words that start
 |  sentences; and then uses that model to find sentence boundaries.
 |  This approach has been shown to work well for many European
 |  languages.
 |
 |  Method resolution order:
 |      PunktSentenceTokenizer
 |      PunktBaseClass
 |      nltk.tokenize.api.TokenizerI
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  __init__(self, train_text=None, verbose=False, lang_vars=<nltk.tokenize.punkt.PunktLanguageVars object at 0x105658438>, token_cls=<class 'nltk.tokenize.punkt.PunktToken'>)
 |      train_text can either be the sole training text for this sentence
 |      boundary detector, or can be a PunktParameters object.
 |
 |  debug_decisions(self, text)
 |      Classifies candidate periods as sentence breaks, yielding a dict for
 |      each that may be used to understand why the decision was made.
 |
 |      See format_debug_decision() to help make this output readable.
 |
 |  dump(self, tokens)
 |      # [XX] TESTING
 |
 |  sentences_from_text(self, text, realign_boundaries=True)
 |      Given a text, generates the sentences in that text by only
 |      testing candidate sentence breaks. If realign_boundaries is
 |      True, includes in the sentence closing punctuation that
 |      follows the period.
 |
 |  sentences_from_text_legacy(self, text)
 |      Given a text, generates the sentences in that text. Annotates all
 |      tokens, rather than just those with possible sentence breaks. Should
 |      produce the same results as ``sentences_from_text``.
 |
 |  sentences_from_tokens(self, tokens)
 |      Given a sequence of tokens, generates lists of tokens, each list
