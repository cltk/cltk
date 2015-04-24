"""Language-specific word tokenizers. Primary purpose is to handle enclitics."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from nltk.tokenize.punkt import PunktLanguageVars


class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and setup class variables."""
        self.language = language
        self.available_languages = ['greek', 'latin']
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language, self.available_languages)  # pylint: disable=line-too-long

        if self.language == 'greek':
            self.enclitics = []
        elif self.language == 'latin':
            self.enclitics = ['que', 've', 'ne']

    def tokenize(self, string):
        """Tokenize incoming string."""
        punkt = PunktLanguageVars()
        generic_tokens = punkt.word_tokenize(string)
        specific_tokens = []
        for generic_token in generic_tokens:
            is_enclitic = False
            for enclitic in self.enclitics:
                if generic_token.endswith(enclitic):
                    new_tokens = [generic_token[:-len(enclitic)]] + [enclitic]
                    specific_tokens += new_tokens
                    is_enclitic = True
                    break
            if not is_enclitic:
                print('generic unsplit token:', generic_token)
                specific_tokens.append(generic_token)

        return specific_tokens
