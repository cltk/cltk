""" Params: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

from nltk.tokenize.punkt import PunktLanguageVars

PRAENOMINA = ['a', 'agr', 'ap', 'c', 'cn', 'd', 'f', 'k', 'l', "m'", 'm', 'mam', 'n', 'oct', 'opet', 'p', 'post', 'pro', 'q', 's', 'ser', 'sert', 'sex', 'st', 't', 'ti', 'v', 'vol', 'vop', 'a', 'ap', 'c', 'cn', 'd', 'f', 'k', 'l', 'm', "m'", 'mam', 'n', 'oct', 'opet', 'p', 'paul', 'post', 'pro', 'q', 'ser', 'sert', 'sex', 'sp', 'st', 'sta', 't', 'ti', 'v', 'vol', 'vop']

CALENDAR = ['ian', 'febr', 'mart', 'apr', 'mai', 'iun', 'iul', 'aug', 'sept', 'oct', 'nov', 'dec'] \
            + ['kal', 'non', 'id', 'a.d']

MISC = ['coll', 'cos', 'ord', 'pl.', 's.c', 'suff', 'trib']

ABBREVIATIONS = set(
                   PRAENOMINA +
                   CALENDAR +
                   MISC
                   )

### Exceptions for the word tokenizer
from typing import List

que_exceptions = []  # type: List[str]
n_exceptions = []  # type: List[str]
ne_exceptions = []  # type: List[str]
ue_exceptions = []  # type: List[str]
ve_exceptions = []  # type: List[str]
st_exceptions = []  # type: List[str]

# quisque / quique
que_exceptions += ['quisque', 'quidque', 'quicque', 'quodque', 'cuiusque', 'cuique', 'quemque', "quamque", 'quoque',
                   'quaque', 'quique', 'quaeque', 'quorumque', 'quarumque', 'quibusque', 'quosque', 'quasque']

# uterque
que_exceptions += ['uterque', 'utraque', 'utrumque', 'utriusque', 'utrique', 'utrumque', 'utramque', 'utroque',
                   'utraque', 'utrique', 'utraeque', 'utrorumque', 'utrarumque', 'utrisque', 'utrosque', 'utrasque']

# quiscumque
que_exceptions += ['quicumque', 'quidcumque', 'quodcumque', 'cuiuscumque', 'cuicumque', 'quemcumque', 'quamcumque',
                   'quocumque', 'quacumque', 'quicumque', 'quaecumque', 'quorumcumque', 'quarumcumque', 'quibuscumque',
                   'quoscumque', 'quascumque']

# unuscumque
que_exceptions += ['unusquisque', 'unaquaeque', 'unumquodque', 'unumquidque', 'uniuscuiusque', 'unicuique',
                   'unumquemque', 'unamquamque', 'unoquoque', 'unaquaque']

# plerusque
que_exceptions += ['plerusque', 'pleraque', 'plerumque', 'plerique', 'pleraeque', 'pleroque', 'pleramque',
                   'plerorumque', 'plerarumque', 'plerisque', 'plerosque', 'plerasque']

# misc
que_exceptions += ['absque', 'abusque', 'adaeque', 'adusque', 'aeque', 'antique', 'atque', 'circumundique', 'conseque',
                   'cumque', 'cunque', 'denique', 'deque', 'donique', 'hucusque', 'inique', 'inseque', 'itaque',
                   'longinque', 'namque', 'neque', 'oblique', 'peraeque', 'praecoque', 'propinque', 'qualiscumque',
                   'quandocumque', 'quandoque', 'quantuluscumque', 'quantumcumque', 'quantuscumque', 'quinque',
                   'quocumque', 'quomodocumque', 'quomque', 'quotacumque', 'quotcumque', 'quotienscumque',
                   'quotiensque', 'quotusquisque', 'quousque', 'relinque', 'simulatque', 'torque', 'ubicumque',
                   'ubique', 'undecumque', 'undique', 'usque', 'usquequaque', 'utcumque', 'utercumque', 'utique',
                   'utrimque', 'utrique', 'utriusque', 'utrobique', 'utrubique']

ne_exceptions += ['absone', 'acharne', 'acrisione', 'acumine', 'adhucine', 'adsuetudine', 'aeetine', 'aeschynomene',
                  'aesone', 'agamemnone', 'agmine', 'albane', 'alcyone', 'almone', 'alsine', 'amasene', 'ambitione',
                  'amne', 'amoene', 'amymone', 'anadyomene', 'andrachne', 'anemone', 'aniene', 'anne', 'antigone',
                  'aparine', 'apolline', 'aquilone', 'arachne', 'arne', 'arundine', 'ascanione', 'asiane', 'asine',
                  'aspargine', 'babylone', 'barine', 'bellone', 'belone', 'bene', 'benigne', 'bipenne', 'bizone',
                  'bone', 'bubone', 'bulbine', 'cacumine', 'caligine', 'calymne', 'cane', 'carcine', 'cardine',
                  'carmine', 'catacecaumene', 'catone', 'cerne', 'certamine', 'chalbane', 'chamaedaphne',
                  'chamaemyrsine', 'chaone', 'chione', 'christiane', 'clymene', 'cognomine', 'commagene', 'commune',
                  'compone', 'concinne', 'condicione', 'condigne', 'cone', 'confine', 'consone', 'corone', 'crastine',
                  'crepidine', 'crimine', 'crine', 'culmine', 'cupidine', 'cyane', 'cydne', 'cyllene', 'cyrene',
                  'daphne', 'depone', 'desine', 'dicione', 'digne', 'dine', 'dione', 'discrimine', 'diutine', 'dracone',
                  'dulcedine', 'elatine', 'elephantine', 'elleborine', 'epidamne', 'erigone', 'euadne', 'euphrone',
                  'euphrosyne', 'examine', 'faune', 'femine', 'feminine', 'ferrugine', 'fine', 'flamine', 'flumine',
                  'formidine', 'fragmine', 'fraterne', 'fulmine', 'fune', 'germane', 'germine', 'geryone', 'gorgone',
                  'gramine', 'grandine', 'haecine', 'halcyone', 'hammone', 'harundine', 'hedone', 'helene', 'helxine',
                  'hermione', 'heroine', 'hesione', 'hicine', 'hicne', 'hierabotane', 'hippocrene', 'hispane',
                  'hodierne', 'homine', 'hominesne', 'hortamine', 'hucine', 'humane', 'hunccine', 'huncine', 'iasione',
                  'iasone', 'igne', 'imagine', 'immane', 'immune', 'impoene', 'impone', 'importune', 'impune', 'inane',
                  'inconcinne', 'indagine', 'indigne', 'inferne', 'inguine', 'inhumane', 'inpone', 'inpune', 'insane',
                  'insigne', 'inurbane', 'ismene', 'istucine', 'itone', 'iuuene', 'karthagine', 'labiene',
                  'lacedaemone', 'lanugine', 'latine', 'legione', 'lene', 'lenone', 'libidine', 'limine', 'limone',
                  'lumine', 'magne', 'maligne', 'mane', 'margine', 'marone', 'masculine', 'matutine', 'medicamine',
                  'melpomene', 'memnone', 'mesene', 'messene', 'misene', 'mitylene', 'mnemosyne', 'moderamine', 'moene',
                  'mone', 'mortaline', 'mucrone', 'munimine', 'myrmidone', 'mytilene', 'ne', 'necne', 'neptune', 'nequene',
                  'nerine', 'nocturne', 'nomine', 'nonne', 'nullane', 'numine', 'nuncine', 'nyctimene', 'obscene',
                  'obsidione', 'oenone', 'omine', 'omne', 'oppone', 'opportune', 'ordine', 'origine', 'orphne',
                  'oxymyrsine', 'paene', 'pallene', 'pane', 'paraetacene', 'patalene', 'pectine', 'pelagine', 'pellene',
                  'pene', 'perbene', 'perbenigne', 'peremne', 'perenne', 'perindigne', 'peropportune', 'persephone',
                  'phryne', 'pirene', 'pitane', 'plane', 'pleione', 'plene', 'pone', 'praefiscine', 'prasiane',
                  'priene', 'priuigne', 'procne', 'proditione', 'progne', 'prone', 'propone', 'pulmone', 'pylene',
                  'pyrene', 'pythone', 'ratione', 'regione', 'religione', 'remane', 'retine', 'rhene', 'rhododaphne',
                  'robigine', 'romane', 'roxane', 'rubigine', 'sabine', 'sane', 'sanguine', 'saturne', 'seditione',
                  'segne', 'selene', 'semine', 'semiplene', 'sene', 'sepone', 'serene', 'sermone', 'serrane', 'siccine',
                  'sicine', 'sine', 'sithone', 'solane', 'sollemne', 'somne', 'sophene', 'sperne', 'spiramine',
                  'stamine', 'statione', 'stephane', 'sterne', 'stramine', 'subpone', 'subtegmine', 'subtemine',
                  'sulmone', 'superne', 'supine', 'suppone', 'susiane', 'syene', 'tantane', 'tantine', 'taprobane',
                  'tegmine', 'telamone', 'temne', 'temone', 'tene', 'testudine', 'theophane', 'therone', 'thyone',
                  'tiberine', 'tibicine', 'tiburne', 'tirone', 'tisiphone', 'torone', 'transitione', 'troiane',
                  'turbine', 'turne', 'tyrrhene', 'uane', 'uelamine', 'uertigine', 'uesane', 'uimine', 'uirgine',
                  'umbone', 'unguine', 'uolumine', 'uoragine', 'urbane', 'uulcane', 'zone']

n_exceptions += ['aenean', 'agmen', 'alioquin', 'an', 'attamen', 'cacumen', 'carmen', 'certamen', 'clymenen', 'cognomen',
                 'crimen', 'culmen', 'dein', 'deucalion', 'discrimen', 'en', 'epitheton', 'erinyn', 'exin', 'flumen',
                 'forsan', 'forsitan', 'fulmen', 'gramen', 'hymen', 'iason', 'in', 'limen', 'liquamen', 'lumen', 'nomen',
                 'non', 'numen', 'omen', 'orion', 'paean', 'pan', 'pelion', 'phaethon', 'python', 'quin', 'semen', 'sin',
                 'specimen', 'tamen', 'themin', 'titan']

# English words; this list added to better handle English header, navigation, etc. in plaintext files of the Latin Library corpus.
n_exceptions += ['alcuin', 'caen', 'christian', 'chronicon', 'châtillon', 'claudian', 'john', 'justin', 'latin',
                 'lucan', 'martin', 'novatian', 'quintilian', 'roman', 'tertullian']

ue_exceptions += ['agaue', 'ambigue', 'assidue', 'aue', 'boue', 'breue', 'calue', 'caue', 'ciue', 'congrue', 'contigue',
                  'continue', 'curue', 'exigue', 'exue', 'fatue', 'faue', 'fue', 'furtiue', 'gradiue', 'graue',
                  'ignaue', 'incongrue', 'ingenue', 'innocue', 'ioue', 'lasciue', 'leue', 'moue', 'mutue', 'naue',
                  'neue', 'niue', 'perexigue', 'perspicue', 'pingue', 'praecipue', 'praegraue', 'prospicue', 'proterue',
                  'remoue', 'resolue', 'saeue', 'salue', 'siue', 'solue', 'strenue', 'sue', 'summoue', 'superflue',
                  'supplicue', 'tenue', 'uiue', 'ungue', 'uoue']

ve_exceptions += ['agave', 'ave', 'bove', 'breve', 'calve', 'cave', 'cive', 'curve', 'fave', 'furtive', 'gradive',
                  'grave', 'ignave', 'iove', 'lascive', 'leve', 'move', 'nave', 'neve', 'nive', 'praegrave',
                  'promiscue', 'prospicve', 'proterve', 'remove', 'resolve', 'saeve', 'salve', 'sive', 'solve',
                  'summove', 'vive', 'vove']

st_exceptions += ['abest', 'adest', 'ast', 'deest', 'est', 'inest', 'interest', 'post', 'potest', 'prodest', 'subest',
                  'superest']

latin_exceptions = list(set(que_exceptions
                            + ne_exceptions
                            + n_exceptions
                            + ue_exceptions
                            + ve_exceptions
                            + st_exceptions
                            ))

latin_replacements = [
    (r'\bmecum\b', 'cum me'),
    (r'\btecum\b', 'cum te'),
    (r'\bsecum\b', 'cum se'),
    (r'\bnobiscum\b', 'cum nobis'),
    (r'\bvobiscum\b', 'cum vobis'),
    (r'\bquocum\b', 'cum quo'),
    (r'\bquacum\b', 'cum qua'),
    (r'\bquicum\b', 'cum qui'),
    (r'\bquibuscum\b', 'cum quibus'),
    (r'\bsodes\b', 'si audes'),
    (r'\bsatin\b', 'satis ne'),
    (r'\bscin\b', 'scis ne'),
    (r'\bsultis\b', 'si vultis'),
    (r'\bsimilist\b', 'similis est'),
    (r'\bqualist\b', 'qualis est')
]

class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')

PUNCTUATION = ('.', '?', '!')
STRICT_PUNCTUATION = PUNCTUATION+('-', ':', ';')
