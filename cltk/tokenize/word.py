"""Language-specific word tokenizers. Primary purpose is to handle enclitics.

Re: latin
Starter lists have been included to handle the Latin enclitics
(-que, -ne, -ue/-ve, -cum). These lists are based on high-frequency vocabulary
 and have been supplemented on a as-needed basis; i.e. they are not
 comprehensive. Additions to the exceptions list are welcome. PJB
"""

from nltk.tokenize.punkt import PunktLanguageVars

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'


class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        self.available_languages = ['latin']
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language,  # pylint: disable=line-too-long
                                                                                            self.available_languages)  # pylint: disable=line-too-long

        if self.language == 'latin':
            self.enclitics = ['que', 'n', 'ne', 'ue', 've', 'cum','st']

            self.inclusions = []
            
            cum_inclusions = ['mecum', 'tecum', 'secum', 'nobiscum', 'vobiscum', 'quocum', 'quicum' 'quibuscum']
            
            self.exceptions = self.enclitics

            que_exceptions = []
            n_exceptions = []
            ne_exceptions = []
            ue_exceptions = []
            ve_exceptions = []
            cum_exceptions = []
            st_exceptions = []

            # quisque
            que_exceptions += ['quisque', 'quidque', 'quicque', 'quodque', 'cuiusque', 'cuique',
                               'quemque', 'quoque', 'quique', 'quaeque', 'quorumque', 'quarumque',
                               'quibusque', 'quosque', 'quasque']

            # uterque
            que_exceptions += ['uterque', 'utraque', 'utrumque', 'utriusque', 'utrique', 'utrumque',
                               'utramque', 'utroque', 'utraque', 'utrique', 'utraeque', 'utrorumque',
                               'utrarumque', 'utrisque', 'utrosque', 'utrasque']

            # quiscumque
            que_exceptions += ['quicumque', 'quidcumque', 'quodcumque', 'cuiuscumque', 'cuicumque',
                               'quemcumque', 'quamcumque', 'quocumque', 'quacumque', 'quicumque',
                               'quaecumque', 'quorumcumque', 'quarumcumque', 'quibuscumque',
                               'quoscumque', 'quascumque']

            # unuscumque
            que_exceptions += ['unusquisque', 'unaquaeque', 'unumquodque', 'unumquidque',
                               'uniuscuiusque', 'unicuique', 'unumquemque', 'unamquamque', 'unoquoque',
                               'unaquaque']

            # plerusque
            que_exceptions += ['plerusque', 'pleraque', 'plerumque', 'plerique', 'pleraeque',
                               'pleroque', 'pleramque', 'plerorumque', 'plerarumque', 'plerisque',
                               'plerosque', 'plerasque']

            # misc
            que_exceptions += ['absque', 'abusque', 'adaeque', 'adusque', 'aeque', 'antique', 'atque',
                               'circumundique', 'conseque', 'cumque', 'cunque', 'denique', 'deque',
                               'donique', 'hucusque', 'inique', 'inseque', 'itaque', 'longinque',
                               'namque', 'oblique', 'peraeque', 'praecoque', 'propinque',
                               'qualiscumque', 'quandocumque', 'quandoque', 'quantuluscumque',
                               'quantumcumque', 'quantuscumque', 'quinque', 'quocumque',
                               'quomodocumque', 'quomque', 'quotacumque', 'quotcumque',
                               'quotienscumque', 'quotiensque', 'quotusquisque', 'quousque', 'relinque',
                               'simulatque', 'torque', 'ubicumque', 'ubique', 'undecumque', 'undique',
                               'usque', 'usquequaque', 'utcumque', 'utercumque', 'utique', 'utrimque',
                               'utrique', 'utriusque', 'utrobique', 'utrubique']

            ne_exceptions += ['absone', 'acharne', 'acrisione', 'acumine', 'adhucine', 'adsuetudine',
                              'aeetine', 'aeschynomene', 'aesone', 'agamemnone', 'agmine', 'albane',
                              'alcyone', 'almone', 'alsine', 'amasene', 'ambitione', 'amne', 'amoene',
                              'amymone', 'anadyomene', 'andrachne', 'anemone', 'aniene', 'anne',
                              'antigone', 'aparine', 'apolline', 'aquilone', 'arachne', 'arne',
                              'arundine', 'ascanione', 'asiane', 'asine', 'aspargine', 'babylone',
                              'barine', 'bellone', 'belone', 'bene', 'benigne', 'bipenne', 'bizone',
                              'bone', 'bubone', 'bulbine', 'cacumine', 'caligine', 'calymne', 'cane',
                              'carcine', 'cardine', 'carmine', 'catacecaumene', 'catone', 'cerne',
                              'certamine', 'chalbane', 'chamaedaphne', 'chamaemyrsine', 'chaone',
                              'chione', 'christiane', 'clymene', 'cognomine', 'commagene', 'commune',
                              'compone', 'concinne', 'condicione', 'condigne', 'cone', 'confine',
                              'consone', 'corone', 'crastine', 'crepidine', 'crimine', 'crine',
                              'culmine', 'cupidine', 'cyane', 'cydne', 'cyllene', 'cyrene', 'daphne',
                              'depone', 'desine', 'dicione', 'digne', 'dine', 'dione', 'discrimine',
                              'diutine', 'dracone', 'dulcedine', 'elatine', 'elephantine', 'elleborine',
                              'epidamne', 'erigone', 'euadne', 'euphrone', 'euphrosyne', 'examine',
                              'faune', 'femine', 'feminine', 'ferrugine', 'fine', 'flamine', 'flumine',
                              'formidine', 'fragmine', 'fraterne', 'fulmine', 'fune', 'germane',
                              'germine', 'geryone', 'gorgone', 'gramine', 'grandine', 'haecine',
                              'halcyone', 'hammone', 'harundine', 'hedone', 'helene', 'helxine',
                              'hermione', 'heroine', 'hesione', 'hicine', 'hicne', 'hierabotane',
                              'hippocrene', 'hispane', 'hodierne', 'homine', 'hominesne', 'hortamine',
                              'hucine', 'humane', 'hunccine', 'huncine', 'iasione', 'iasone', 'igne',
                              'imagine', 'immane', 'immune', 'impoene', 'impone', 'importune', 'impune',
                              'inane', 'inconcinne', 'indagine', 'indigne', 'inferne', 'inguine',
                              'inhumane', 'inpone', 'inpune', 'insane', 'insigne', 'inurbane', 'ismene',
                              'istucine', 'itone', 'iuuene', 'karthagine', 'labiene', 'lacedaemone',
                              'lanugine', 'latine', 'legione', 'lene', 'lenone', 'libidine', 'limine',
                              'limone', 'lumine', 'magne', 'maligne', 'mane', 'margine', 'marone',
                              'masculine', 'matutine', 'medicamine', 'melpomene', 'memnone', 'mesene',
                              'messene', 'misene', 'mitylene', 'mnemosyne', 'moderamine', 'moene',
                              'mone', 'mortaline', 'mucrone', 'munimine', 'myrmidone', 'mytilene',
                              'necne', 'neptune', 'nequene', 'nerine', 'nocturne', 'nomine', 'nonne',
                              'nullane', 'numine', 'nuncine', 'nyctimene', 'obscene', 'obsidione',
                              'oenone', 'omine', 'omne', 'oppone', 'opportune', 'ordine', 'origine',
                              'orphne', 'oxymyrsine', 'paene', 'pallene', 'pane', 'paraetacene',
                              'patalene', 'pectine', 'pelagine', 'pellene', 'pene', 'perbene',
                              'perbenigne', 'peremne', 'perenne', 'perindigne', 'peropportune',
                              'persephone', 'phryne', 'pirene', 'pitane', 'plane', 'pleione', 'plene',
                              'pone', 'praefiscine', 'prasiane', 'priene', 'priuigne', 'procne',
                              'proditione', 'progne', 'prone', 'propone', 'pulmone', 'pylene', 'pyrene',
                              'pythone', 'ratione', 'regione', 'religione', 'remane', 'retine', 'rhene',
                              'rhododaphne', 'robigine', 'romane', 'roxane', 'rubigine', 'sabine',
                              'sane', 'sanguine', 'saturne', 'seditione', 'segne', 'selene', 'semine',
                              'semiplene', 'sene', 'sepone', 'serene', 'sermone', 'serrane', 'siccine',
                              'sicine', 'sine', 'sithone', 'solane', 'sollemne', 'somne', 'sophene',
                              'sperne', 'spiramine', 'stamine', 'statione', 'stephane', 'sterne',
                              'stramine', 'subpone', 'subtegmine', 'subtemine', 'sulmone', 'superne',
                              'supine', 'suppone', 'susiane', 'syene', 'tantane', 'tantine', 'taprobane',
                              'tegmine', 'telamone', 'temne', 'temone', 'tene', 'testudine', 'theophane',
                              'therone', 'thyone', 'tiberine', 'tibicine', 'tiburne', 'tirone',
                              'tisiphone', 'torone', 'transitione', 'troiane', 'turbine', 'turne',
                              'tyrrhene', 'uane', 'uelamine', 'uertigine', 'uesane', 'uimine', 'uirgine',
                              'umbone', 'unguine', 'uolumine', 'uoragine', 'urbane', 'uulcane', 'zone']
                              
            n_exceptions += ['aenean', 'agmen', 'alioquin', 'an', 'attamen', 'carmen', 'certamen', 'cognomen', 'crimen', 'dein', 'discrimen', 'en', 'epitheton', 'exin', 'flumen', 'forsan', 'forsitan', 'fulmen', 'iason', 'in', 'limen', 'liquamen', 'lumen', 'nomen', 'non', 'numen', 'omen', 'orion', 'quin', 'semen', 'specimen', 'tamen', 'titan']

            ue_exceptions += ['agaue', 'ambigue', 'assidue', 'aue', 'boue', 'breue', 'calue', 'caue',
                              'ciue', 'congrue', 'contigue', 'continue', 'curue', 'exigue', 'exue',
                              'fatue', 'faue', 'fue', 'furtiue', 'gradiue', 'graue', 'ignaue',
                              'incongrue', 'ingenue', 'innocue', 'ioue', 'lasciue', 'leue', 'moue',
                              'mutue', 'naue', 'neue', 'niue', 'perexigue', 'perspicue', 'pingue',
                              'praecipue', 'praegraue', 'prospicue', 'proterue', 'remoue', 'resolue',
                              'saeue', 'salue', 'siue', 'solue', 'strenue', 'sue', 'summoue',
                              'superflue', 'supplicue', 'tenue', 'uiue', 'ungue', 'uoue']

            ve_exceptions += ['agave', 'ave', 'bove', 'breve', 'calve', 'cave', 'cive', 'curve', 'fave',
                              'furtive', 'gradive', 'grave', 'ignave', 'iove', 'lascive', 'leve', 'move',
                              'nave', 'neve', 'nive', 'praegrave', 'prospicve', 'proterve', 'remove',
                              'resolve', 'saeve', 'salve', 'sive', 'solve', 'summove', 'vive', 'vove']

            st_exceptions += ['abest', 'adest', 'ast', 'deest', 'est', 'inest', 'interest', 'post', 'potest', 'prodest', 'subest', 'superest']

            self.exceptions = list(set(self.exceptions
                                       + que_exceptions
                                       + ne_exceptions
                                       + n_exceptions
                                       + ue_exceptions
                                       + ve_exceptions
                                       + st_exceptions
                                       ))

            self.inclusions = list(set(self.inclusions
                                       + cum_inclusions))

    def tokenize(self, string):
        """Tokenize incoming string."""
        punkt = PunktLanguageVars()
        generic_tokens = punkt.word_tokenize(string)
        # Rewrite as an if-else block for exceptions rather than separate list comprehensions
        generic_tokens = [x for item in generic_tokens for x in ([item] if item.lower() != 'nec' else ['c', item[:-1]])] # Handle 'nec' as a special case.
        generic_tokens = [x for item in generic_tokens for x in ([item] if item.lower() != 'sodes' else [item[0]+'i', 'audes'])] # Handle 'sodes' as a special case.
        generic_tokens = [x for item in generic_tokens for x in ([item] if item.lower() != 'sultis' else [item[0]+'i', 'vultis'])] # Handle 'sultis' as a special case.
        generic_tokens = [x for item in generic_tokens for x in ([item] if item.lower() != 'satin' else [item[:-1] + 's', 'ne'])] # Handle 'satin' as a special case.
        generic_tokens = [x for item in generic_tokens for x in ([item] if item.lower() != 'scin' else [item[:-1] + 's', 'ne'])] # Handle 'scin' as a special case.      
        specific_tokens = []
        for generic_token in generic_tokens:
            is_enclitic = False
            if generic_token not in self.exceptions:
                for enclitic in self.enclitics:
                    if generic_token.endswith(enclitic):
                        if enclitic == 'cum':
                            if generic_token.lower() in self.inclusions:
                                specific_tokens += [enclitic] + [generic_token[:-len(enclitic)]]
                            else:
                                specific_tokens += [generic_token]
                        elif enclitic == 'n':
                                specific_tokens += [generic_token[:-len(enclitic)]] + ['ne']                                                                                                    
                        elif enclitic == 'st':
                            if generic_token.endswith('ust'):
                                specific_tokens += [generic_token[:-len(enclitic)+1]] + ['est']
                            else:
                                # Does not handle 'similist', 'qualist', etc. correctly
                                specific_tokens += [generic_token[:-len(enclitic)]] + ['est']
                        else:
                            specific_tokens += [enclitic] + [generic_token[:-len(enclitic)]]
                        is_enclitic = True
                        break
            if not is_enclitic:
                specific_tokens.append(generic_token)
        return specific_tokens

def nltk_tokenize_words(string, attached_period=False):
    """Wrap NLTK's tokenizer PunktLanguageVars(), but make final period
    its own token.
    >>> nltk_punkt("Sentence 1. Sentence 2.")
    >>> ['Sentence', 'one', '.', 'Sentence', 'two', '.']

    Optionally keep the NLTK's output:
    >>> nltk_punkt("Sentence 1. Sentence 2.", attached_period=True)
    >>> ['Sentence', 'one.', 'Sentence', 'two.']

    TODO: Run some tests to determine whether there is a large penalty for
    re-calling PunktLanguageVars() for each use of this function. If so, this
    will need to become a class, perhaps inheriting from the PunktLanguageVars
    object. Maybe integrate with WordTokenizer.
    """
    assert isinstance(string, str), "Incoming string must be type str."
    punkt = PunktLanguageVars()
    tokens = punkt.word_tokenize(string)
    if attached_period:
        return tokens
    new_tokens = []
    for word in tokens:
        if word.endswith('.'):
            new_tokens.append(word[:-1])
            new_tokens.append('.')
        else:
            new_tokens.append(word)
    return new_tokens