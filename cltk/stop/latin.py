"""
Code for building and working with stoplists for Latin
"""

# KPJ included as author for Perseus list under GPL license; keep? Or
# should it be MPL as in accompanying documentation; see below.
# Also, multiple licenses from consolidating code—how to handle?
# Here they are in parallel lists:
# - PJB: CorpusStoplist code
# - KPJ: Perseus list

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = ['MIT License. See LICENSE.', 'GPL License.']

from string import punctuation
from cltk.stop.stop import BaseCorpusStoplist

class CorpusStoplist(BaseCorpusStoplist):

    def __init__(self, language='latin'):
        BaseCorpusStoplist.__init__(self, language)
        self.punctuation = punctuation
        if not self.numpy_installed or not self.sklearn_installed:
            print('\n\nThe Corpus-based Stoplist method requires numpy and scikit-learn for calculations. Try installing with `pip install numpy sklearn scipy`.\n\n')
            raise ImportError
        else:
            from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
            self.vectorizer = CountVectorizer(input='content') # Set df?
            self.tfidf_vectorizer = TfidfVectorizer(input='content')

# Reference lists

"""This stopword list is taken from the Perseus Hopper source at
``/sgml/reading/build/stoplists``. Source at ``http://sourceforge.net/projects/perseus-hopper/``.

Perseus data licensed under  the Mozilla Public License 1.1 (MPL 1.1)
[``http://www.mozilla.org/MPL/1.1/``].
"""
PERSEUS_STOPS = 'ab ac ad adhic aliqui aliquis an ante apud at atque aut ' \
                'autem cum cur de deinde dum ego enim ergo es est et etiam ' \
                'etsi ex fio haud hic iam idem igitur ille in infra inter ' \
                'interim ipse is ita magis modo mox nam ne nec necque neque ' \
                'nisi non nos o ob per possum post pro quae quam quare qui ' \
                'quia quicumque quidem quilibet quis quisnam quisquam ' \
                'quisque quisquis quo quoniam sed si sic sive sub sui sum ' \
                'super suus tam tamen trans tu tum ubi uel uero unus ut'.split()

# For consistency between releases; should be deprecated
STOPS_LIST = PERSEUS_STOPS


if __name__ == "__main__":
    test_1 = """cogitanti mihi saepe numero et memoria vetera repetenti perbeati fuisse, quinte frater, illi videri solent, qui in optima re publica, cum et honoribus et rerum gestarum gloria florerent, eum vitae cursum tenere potuerunt, ut vel in negotio sine periculo vel in otio cum dignitate esse possent; ac fuit cum mihi quoque initium requiescendi atque animum ad utriusque nostrum praeclara studia referendi fore iustum et prope ab omnibus concessum arbitrarer, si infinitus forensium rerum labor et ambitionis occupatio decursu honorum, etiam aetatis flexu constitisset. quam spem cogitationum et consiliorum meorum cum graves communium temporum tum varii nostri casus fefellerunt; nam qui locus quietis et tranquillitatis plenissimus fore videbatur, in eo maximae moles molestiarum et turbulentissimae tempestates exstiterunt; neque vero nobis cupientibus atque exoptantibus fructus oti datus est ad eas artis, quibus a pueris dediti fuimus, celebrandas inter nosque recolendas. nam prima aetate incidimus in ipsam perturbationem disciplinae veteris, et consulatu devenimus in medium rerum omnium certamen atque discrimen, et hoc tempus omne post consulatum obiecimus eis fluctibus, qui per nos a communi peste depulsi in nosmet ipsos redundarent. sed tamen in his vel asperitatibus rerum vel angustiis temporis obsequar studiis nostris et quantum mihi vel fraus inimicorum vel causae amicorum vel res publica tribuet oti, ad scribendum potissimum conferam; tibi vero, frater, neque hortanti deero neque roganti, nam neque auctoritate quisquam apud me plus valere te potest neque voluntate."""

    test_2 = """ac mihi repetenda est veteris cuiusdam memoriae non sane satis explicata recordatio, sed, ut arbitror, apta ad id, quod requiris, ut cognoscas quae viri omnium eloquentissimi clarissimique senserint de omni ratione dicendi. vis enim, ut mihi saepe dixisti, quoniam, quae pueris aut adulescentulis nobis ex commentariolis nostris incohata ac rudia exciderunt, vix sunt hac aetate digna et hoc usu, quem ex causis, quas diximus, tot tantisque consecuti sumus, aliquid eisdem de rebus politius a nobis perfectiusque proferri; solesque non numquam hac de re a me in disputationibus nostris dissentire, quod ego eruditissimorum hominum artibus eloquentiam contineri statuam, tu autem illam ab elegantia doctrinae segregandam putes et in quodam ingeni atque exercitationis genere ponendam. ac mihi quidem saepe numero in summos homines ac summis ingeniis praeditos intuenti quaerendum esse visum est quid esset cur plures in omnibus rebus quam in dicendo admirabiles exstitissent; nam quocumque te animo et cogitatione converteris, permultos excellentis in quoque genere videbis non mediocrium artium, sed prope maximarum. quis enim est qui, si clarorum hominum scientiam rerum gestarum vel utilitate vel magnitudine metiri velit, non anteponat oratori imperatorem? quis autem dubitet quin belli duces ex hac una civitate praestantissimos paene innumerabilis, in dicendo autem excellentis vix paucos proferre possimus? iam vero consilio ac sapientia qui regere ac gubernare rem publicam possint, multi nostra, plures patrum memoria atque etiam maiorum exstiterunt, cum boni perdiu nulli, vix autem singulis aetatibus singuli tolerabiles oratores invenirentur. ac ne qui forte cum aliis studiis, quae reconditis in artibus atque in quadam varietate litterarum versentur, magis hanc dicendi rationem, quam cum imperatoris laude aut cum boni senatoris prudentia comparandam putet, convertat animum ad ea ipsa artium genera circumspiciatque, qui in eis floruerint quamque multi sint; sic facillime, quanta oratorum sit et semper fuerit paucitas, iudicabit."""

    test_corpus = [test_1, test_2]

    S = CorpusStoplist()
    print(S.build_stoplist(test_corpus, size=10,
                    basis='zou', inc_values=True))
