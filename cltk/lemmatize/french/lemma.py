from cltk.tokenize.word import WordTokenizer
from cltk.lemmatize.french.french import regex
import os
import importlib.machinery

__author__ = ['Natasha Voake <natashavoake@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


class LemmaReplacer(object):  # pylint: disable=too-few-public-methods
    """Lemmatize French words by replacing input words with corresponding
    values from a replacement list.
    """

    def _load_necessary_data(self):
        """Check for availability of lemmatizer for French."""

        rel_path = os.path.join('~','cltk_data',
                                'french',
                                'text','cltk_data_french',
                                'lemmas','entries.py')
        path = os.path.expanduser(rel_path)
        #logger.info('Loading entries. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader('entries', path)
        module1 = loader.load_module()
        entries = module1.entries

        rel_path = os.path.join('~', 'cltk_data',
                                'french',
                                'text', 'cltk_data_french',
                                'lemmas', 'forms_and_lemmas.py')
        path = os.path.expanduser(rel_path)
        # logger.info('Loading forms and lemmas. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader('forms_and_lemmas', path)
        module2 = loader.load_module()
        forms_and_lemmas = module2.forms_and_lemmas
        return entries, forms_and_lemmas

    def lemmatize(self, tokens):
        """define list of lemmas"""
        lemma_list = [x[0] for x in entries]
        """Provide a lemma for each token"""
        lemmatized = []
        for token in tokens:
            """check for a match between token and list of lemmas"""
            if token in lemma_list:
                lemmed = (token, token)
                lemmatized.append(lemmed)
            else:
                """if no match check for a match between token and list of lemma forms"""
                lemma = [k for k, v in forms_and_lemmas.items() if token in v]
                if lemma != []:
                    lemmed = (token, lemma)
                    lemmatized.append(lemmed)
                elif lemma == []:
                    """if no match apply regular expressions and check for a match against the list of lemmas again"""
                    regexed = regex(token)
                    if regexed in lemma_list:
                        lemmed = (token, regexed)
                        lemmatized.append(lemmed)
                    else:
                        lemmed = (token, "None")
                        lemmatized.append(lemmed)
        return lemmatized


