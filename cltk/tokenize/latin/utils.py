""" Tokenization utilities: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import pickle
from typing import List, Dict, Tuple, Set, Any, Generator

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize.punkt import PunktLanguageVars

from cltk.corpus.readers import get_corpus_reader
from cltk.tokenize.latin.params import ABBREVIATIONS

from cltk.tokenize.utils import BaseSentenceTokenizerTrainer

class SentenceTokenizerTrainer(BaseSentenceTokenizerTrainer):
    """ """
    def __init__(self: object, strict: bool = False):
        self.strict = strict
        self.punctuation = ['.', '?', '!']
        self.strict_punctuation = [';', ':', '—']
        self.abbreviations = ABBREVIATIONS

        BaseSentenceTokenizerTrainer.__init__(self, language='latin',
                                                punctuation=self.punctuation,
                                                strict=self.strict,
                                                strict_punctuation=self.strict_punctuation,
                                                abbreviations=self.abbreviations)

if __name__ == "__main__":
    latinlibrary = get_corpus_reader(corpus_name='latin_text_latin_library', language="latin")
    text = latinlibrary.raw()
    trainer = SentenceTokenizerTrainer()
    tokenizer = trainer.train_sentence_tokenizer(text)
    trainer.pickle_sentence_tokenizer('{}_punkt.pickle'.format(trainer.language), tokenizer)

#    tokenizer = pickle.load(open('{}.pickle'.format(trainer.language), 'rb'))
#    text = """I. Quae res in civitate duae plurimum possunt, eae contra nos ambae faciunt in hoc tempore, summa gratia et eloquentia; quarum alterum, C. Aquili, vereor, alteram metuo. Eloquentia Q. Hortensi ne me in dicendo impediat, non nihil commoveor, gratia Sex. Naevi ne P. Quinctio noceat, id vero non mediocriter pertimesco. Neque hoc tanto opere querendum videretur, haec summa in illis esse, si in nobis essent saltem mediocria; verum ita se res habet, ut ego, qui neque usu satis et ingenio parum possum, cum patrono disertissimo comparer, P. Quinctius, cui tenues opes, nullae facultates, exiguae amicorum copiae sunt, cum adversario gratiosissimo contendat. Illud quoque nobis accedit incommodum, quod M. Iunius, qui hanc causam aliquotiens apud te egit, homo et in aliis causis exercitatus et in hac multum ac saepe versatus, hoc tempore abest nova legatione impeditus, et ad me ventum est qui, ut summa haberem cetera, temporis quidem certe vix satis habui ut rem tantam, tot controversiis implicatam, possem cognoscere. Ita quod mihi consuevit in ceteris causis esse adiumento, id quoque in hac causa deficit. Nam, quod ingenio minus possum, subsidium mihi diligentia comparavi; quae quanta sit, nisi tempus et spatium datum sit, intellegi non potest. Quae quo plura sunt, C. Aquili, eo te et hos qui tibi in consilio sunt meliore mente nostra verba audire oportebit, ut multis incommodis veritas debilitata tandem aequitate talium virorum recreetur. Quod si tu iudex nullo praesidio fuisse videbere contra vim et gratiam solitudini atque inopiae, si apud hoc consilium ex opibus, non ex veritate causa pendetur, profecto nihil est iam sanctum atque sincerum in civitate, nihil est quod humilitatem cuiusquam gravitas et virtus iudicis consoletur. Certe aut apud te et hos qui tibi adsunt veritas valebit, aut ex hoc loco repulsa vi et gratia locum ubi consistat reperire non poterit."""
#
#    print(tokenizer.tokenize(text))
