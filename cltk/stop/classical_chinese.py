"""
Code for building and working with stoplists for Classical Chinese
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>'] # Update author list
__license__ = 'MIT License. See LICENSE.'

from cltk.stop.stop import BaseCorpusStoplist

class CorpusStoplist(BaseCorpusStoplist):

    def __init__(self, language='classical_chinese'):
        BaseCorpusStoplist.__init__(self, language)
        self.punctuation = '。，；？：！、《》'
        if not self.numpy_installed or not self.sklearn_installed:
            print('\n\nThe Corpus-based Stoplist method requires numpy and scikit-learn for calculations. Try installing with `pip install numpy sklearn scipy`.\n\n')
            raise ImportError
        else:
            from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
            self.vectorizer = CountVectorizer(analyzer='char', input='content') # Set df?
            self.tfidf_vectorizer = TfidfVectorizer(analyzer='char', input='content')

    def _remove_punctuation(self, texts, punctuation):
        # Change replacement pattern for 'char' analyzer parameter
        translator = str.maketrans({key: "" for key in punctuation}) 
        texts = [text.translate(translator) for text in texts] 
        return texts


if __name__ == "__main__":
    test_1 = """方廣錩〔題解〕《天竺國菩提達摩禪師論》，又名《達摩禪師論》，中國僧人假託禪宗初祖菩提達摩所撰典籍，著者不詳，一卷。在敦煌遺書中，"""

    test_2 = """至今已經發現兩種題名為《達摩禪師論》的文獻。其一為日本橋本凝胤所藏，首殘尾存，尾題作「達摩禪師論」，係唐高宗開耀元年"""

    test_corpus = [test_1, test_2]

    S = CorpusStoplist()
    print(S.build_stoplist(test_corpus, size=10,
                    basis='zou', inc_values=True))
