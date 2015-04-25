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
            #self.enclitics = ['que', 've', 'ne']
            self.enclitics = ['que']
            # Patrick's excpetions
            self.exceptions = ['atque', 'neque', 'quoque', 'itaque', 'usque', 'denique', 'quisque', 'namque', 'quinque', 'utique', 'quaeque', 'plerumque', 'utrumque', 'aeque', 'undique', 'utraque', 'cumque', 'cuique', 'plerique', 'cuiusque', 'utroque', 'utriusque', 'uterque', 'ubique', 'quaecumque', 'utrimque', 'quemque', 'quodque', 'quique', 'plerisque', 'utrique', 'quocumque', 'quicumque', 'pleraque', 'quodcumque', 'quaque', 'quacumque', 'utramque', 'quamque', 'quandoque', 'ubicumque', 'plerosque', 'utcumque', 'quidque', 'quibusque', 'unusquisque', 'quosque', 'quasque', 'quotienscumque', 'cuiuscumque', 'quemcumque', 'inique', 'cuicumque', 'quousque',
                               'tenue', 'siue', 'ioue', 'assidue', 'leue', 'adsidue', 'neue', 'niue', 'salue', 'quidue', 'breue', 'caue', 'graue', 'naue', 'pingue', 'praecipue'
                               ]
            # Kyle's exceptions
            self.exceptions = ['atque', 'neque', 'quoque', 'itaque', 'usque', 'denique', 'quisque', 'namque', 'quinque', 'utique', 'plerumque', 'aeque', 'undique', 'cumque', 'plerique', 'utroque', 'uterque', 'ubique', 'utrimque', 'quocumque', 'quicumque', 'quaque', 'quacumque', 'que', 'quandoque', 'ubicumque', 'deque', 'utcumque', 'unusquisque', 'quotienscumque', 'inique', 'quousque', 'usquequaque', 'qualiscumque', 'utrasque', 'quantumcumque', 'oblique', 'absque', 'quandocumque', 'utrubique', 'quotiensque', 'antique', 'simulatque', 'quicque', 'undecumque', 'peraeque', 'utrobique', 'adusque', 'hucusque', 'adaeque', 'quomodocumque', 'quotcumque', 'quantuscumque', 'abusque', 'donique', 'inseque', 'circumundique', 'propinque', 'praecoque', 'quantuluscumque', 'longinque', 'conseque', 'utercumque', 'quotusquisque', 'quescumque', 'ne', 'sine', 'bene', 'sane', 'paene', 'plane', 'nonne', 'mane', 'commune', 'pone', 'impune', 'insigne', 'benigne', 'necne', 'pane', 'magne', 'anne', 'superne', 'opportune', 'digne', 'lene', 'immane', 'indigne', 'bone', 'maligne', 'plene', 'tisiphone', 'dione', 'urbane', 'sicine', 'procne', 'pene', 'erigone', 'alcyone', 'cyrene', 'germane', 'humane', 'hicine', 'segne', 'insane', 'syene', 'clymene', 'perenne', 'chione', 'condigne', 'cyllene', 'peropportune', 'messene', 'christiane', 'antigone', 'progne', 'amymone', 'persephone', 'pallene', 'oenone', 'fraterne', 'melpomene', 'inhumane', 'euadne', 'taprobane', 'helxine', 'hermione', 'pyrene', 'phryne', 'dine', 'serene', 'hicne', 'hucine', 'daphne', 'sabine', 'asine', 'cyane', 'commagene', 'concinne', 'obscene', 'chamaedaphne', 'theophane', 'nerine', 'diutine', 'perbene', 'inurbane', 'thyone', 'ismene', 'elephantine', 'amoene', 'anemone', 'stephane', 'torone', 'priene', 'arne', 'inferne', 'hippocrene', 'sophene', 'roxane', 'rhene', 'feminine', 'pirene', 'carcine', 'mnemosyne', 'nyctimene', 'susiane', 'pleione', 'pitane', 'mitylene', 'elatine', 'alsine', 'mytilene', 'matutine', 'oxymyrsine', 'peremne', 'hesione', 'absone', 'sithone', 'limone', 'acharne', 'hierabotane', 'euphrone', 'moene', 'zone', 'arachne', 'pellene', 'calymne', 'bizone', 'elleborine', 'impoene', 'corone', 'halcyone', 'paraetacene', 'istucine', 'chalbane', 'semiplene', 'masculine', 'acrisione', 'mesene', 'belone', 'praefiscine', 'consone', 'barine', 'inconcinne', 'aeschynomene', 'anadyomene', 'orphne', 'andrachne', 'pylene', 'prone', 'adhucine', 'hispane', 'aparine', 'importune', 'asiane', 'catacecaumene', 'chamaemyrsine', 'hedone', 'supine', 'myrmidone', 'nuncine', 'perindigne', 'prasiane', 'rhododaphne', 'euphrosyne', 'perbenigne', 'itone', 'patalene', 'bulbine', 'iasione', 'selene', 'praecipue', 'assidue', 'strenue', 'ambigue', 'sue', 'perspicue', 'congrue', 'incongrue', 'ingenue', 'exigue', 'fatue', 'continue', 'superflue', 'prospicue', 'mutue', 'fue', 'innocue', 'perexigue', 'supplicue', 'contigue']
            # quisque, added manually by Kyle
            self.exceptions = self.exceptions + ['quisque', 'quidque', 'quique', 'quaeque', 'quaeque', 'cuiusque', 'cuiusque', '', 'quorumque', 'quarumque', 'quorumque', 'cuique', 'cuique', 'quibusque', 'quibusque', 'quibusque', 'quemque', 'quidque', 'quosque', 'quasque', 'quaeque', 'quoque', 'quoque', 'quibusque', 'quibusque', 'quibusque']
            self.exceptions = set(self.exceptions)


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
