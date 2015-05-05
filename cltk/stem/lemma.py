"""Lemmatize Latin words."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.utils.cltk_logger import logger
import importlib.machinery
from nltk.tokenize.punkt import PunktLanguageVars
import os
import re

AVAILABLE_LANGUAGES = ['greek', 'latin']


class LemmaReplacer(object):  # pylint: disable=R0903
    """Lemmatize Latin words by replacing input words with corresponding
    values from a replacement list.
    """

    def __init__(self, language):
        """Import replacement patterns into a list."""
        self.language = language.lower()
        assert self.language in AVAILABLE_LANGUAGES, \
            "Lemmatizer not available for language '{0}'.".format(self.language)
        self.lemmata = self._load_replacement_patterns()
        #self._patterns = self._compile_patterns(self._raw_patterns)

    def _load_replacement_patterns(self):
        """Check for availability of lemmatizer for a language."""
        if self.language == 'latin':
            rel_path = os.path.join('~/cltk_data',
                                    self.language,
                                    'model/latin_models_cltk/lemmata/latin_lemmata_cltk.py')  # pylint: disable=C0301
            path = os.path.expanduser(rel_path)
            logger.info('Loading lemmata. This may take a minute.')
            loader = importlib.machinery.SourceFileLoader('latin_lemmata_cltk', path)
            module = loader.load_module()
            lemmata = module.LEMMATA
            return lemmata
            #for inflection, headword in lemmata.items():
            #    yield inflection, headword


    def _compile_patterns(self, raw_patterns):
        """Take incoming generator and compile regex replacements."""

        #return [(re.compile(regex), repl) for (regex, repl) in patterns]
        #yield [(re.compile(regex), repl) for (regex, repl) in raw_patterns]
        for (regex, repl) in raw_patterns:
            yield re.compile(regex), repl

    def lemmatize(self, text):
        """Replacer of text via the dict.
        :type text: str
        :param text: Input text to be lemmatized.
        :rtype : str
        """
        for (pattern, repl) in self._patterns:
            text, count = re.subn(pattern, repl, text)
            '''
            if count == 1:
                yield new_token
            '''
        return text



    def lemmatize_tokens(self, in_tokens, testing=False):
        """Simple. Try equal match of tokens. Watch out for periods which ``PunktLanguageVars()`` sticks on."""
        lemmatized_tokens = []
        for token in in_tokens:
            final_period = False
            if token[-1] == '.':
                final_period = True
                token = token[:-1]
            for k, v in self.lemmata.items():
                if token == k:
                    if final_period == True:
                        token = token + '.'
                        v = v + '.'
                    if not testing:
                        lemmatized_tokens.append(v)
                    else:
                        print(token, '-->', v)
                    break
            else:
                if not testing:
                    lemmatized_tokens.append(token)
                else:
                    print(token, '-->', token)
        return lemmatized_tokens


if __name__ == '__main__':
    print('***')
    r = LemmaReplacer('latin')
    p = PunktLanguageVars()
    s = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum. Maiores nostri sic habuerunt et ita in legibus posiuerunt: furem dupli condemnari, foeneratorem quadrupli. Quanto peiorem ciuem existimarint foeneratorem quam furem, hinc licet existimare. Et uirum bonum quom laudabant, ita laudabant: bonum agricolam bonumque colonum; amplissime laudari existimabatur qui ita laudabatur. Mercatorem autem strenuum studiosumque rei quaerendae existimo, uerum, ut supra dixi, periculosum et calamitosum. At ex agricolis et uiri fortissimi et milites strenuissimi gignuntur, maximeque pius quaestus stabilissimusque consequitur minimeque inuidiosus, minimeque male cogitantes sunt qui in eo studio occupati sunt. Nunc, ut ad rem redeam, quod promisi institutum principium hoc erit.'
    tokens = p.word_tokenize(s.lower())
    lemmatized = r.lemmatize_tokens(tokens)
    print(lemmatized)
