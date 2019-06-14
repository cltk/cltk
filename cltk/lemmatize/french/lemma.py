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
    def __init__(self):

        self.entries = self._load_entries()
        self.forms_and_lemmas = self._load_forms_and_lemmas()

    def _load_entries(self):
        """Check for availability of lemmatizer for French."""

        rel_path = os.path.join(get_cltk_data_dir(),
                                'french',
                                'text','french_data_cltk'
                                ,'entries.py')
        path = os.path.expanduser(rel_path)
        #logger.info('Loading entries. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader('entries', path)
        module = loader.load_module()
        entries = module.entries
        return entries

    def _load_forms_and_lemmas(self):

        rel_path = os.path.join(get_cltk_data_dir(),
                                'french',
                                'text', 'french_data_cltk',
                                'forms_and_lemmas.py')
        path = os.path.expanduser(rel_path)
        # logger.info('Loading forms and lemmas. This may take a minute.')
        loader = importlib.machinery.SourceFileLoader('forms_and_lemmas', path)
        module = loader.load_module()
        forms_and_lemmas = module.forms_and_lemmas
        return forms_and_lemmas

    def lemmatize(self, tokens):
        """define list of lemmas"""
        entries = self.entries
        forms_and_lemmas = self.forms_and_lemmas

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
