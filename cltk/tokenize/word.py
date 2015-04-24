"""Language-specific word tokenizers. Primary purpose is to handle enclitics."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'

from nltk.tokenize.punkt import PunktLanguageVars


class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and setup class variables."""
        self.language = language
        self.available_languages = ['latin']
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language, self.available_languages)  # pylint: disable=line-too-long

        if self.language == 'latin':
            self.enclitics = ['que', 've', 'ne']
            self.exceptions = ['atque', 'neque', 'quoque', 'itaque', 'usque', 'denique', 'quisque', 'namque', 'quinque', 'utique', 'quaeque', 'plerumque', 'utrumque', 'aeque', 'undique', 'utraque', 'cumque', 'cuique', 'plerique', 'cuiusque', 'utroque', 'utriusque', 'uterque', 'ubique', 'quaecumque', 'utrimque', 'quemque', 'quodque', 'quique', 'plerisque', 'utrique', 'quocumque', 'quicumque', 'pleraque', 'quodcumque', 'quaque', 'quacumque', 'utramque', 'quamque', 'quandoque', 'ubicumque', 'plerosque', 'utcumque', 'quidque', 'quibusque', 'unusquisque', 'quosque', 'quasque', 'quotienscumque', 'cuiuscumque', 'quemcumque', 'inique', 'cuicumque', 'quousque',
                               'tenue', 'siue', 'ioue', 'assidue', 'leue', 'adsidue', 'neue', 'niue', 'salue', 'quidue', 'breue', 'caue', 'graue', 'naue', 'pingue', 'praecipue'
                               ]

    def tokenize(self, string):
        """Tokenize incoming string."""
        punkt = PunktLanguageVars()
        generic_tokens = punkt.word_tokenize(string)
        specific_tokens = []
        for generic_token in generic_tokens:
            is_enclitic = False
            if generic_token not in self.exceptions:
                for enclitic in self.enclitics:
                    if generic_token.endswith(enclitic):
                        new_tokens = [generic_token[:-len(enclitic)]] + [enclitic]
                        specific_tokens += new_tokens
                        is_enclitic = True
                        break
            if not is_enclitic:
                specific_tokens.append(generic_token)

        return specific_tokens
