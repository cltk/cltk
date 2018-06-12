"""
Starter lists have been included to handle the Latin enclitics
(-que, -ne, -ue/-ve, -cum). These lists are based on high-frequency vocabulary
 and have been supplemented on a as-needed basis; i.e. they are not
 comprehensive. Additions to the exceptions list are welcome. PJB
"""

from typing import List

que_exceptions = []  # type: List[str]
n_exceptions = []  # type: List[str]
ne_exceptions = []  # type: List[str]
ue_exceptions = []  # type: List[str]
ve_exceptions = []  # type: List[str]
st_exceptions = []  # type: List[str]

# quisque
que_exceptions += ['quisque', 'quidque', 'quicque', 'quodque', 'cuiusque', 'cuique', 'quemque', 'quoque', 'quique', 'quaeque', 'quorumque', 'quarumque', 'quibusque', 'quosque', 'quasque']

# uterque
que_exceptions += ['uterque', 'utraque', 'utrumque', 'utriusque', 'utrique', 'utrumque', 'utramque', 'utroque', 'utraque', 'utrique', 'utraeque', 'utrorumque', 'utrarumque', 'utrisque', 'utrosque', 'utrasque']

# quiscumque
que_exceptions += ['quicumque', 'quidcumque', 'quodcumque', 'cuiuscumque', 'cuicumque', 'quemcumque', 'quamcumque', 'quocumque', 'quacumque', 'quicumque', 'quaecumque', 'quorumcumque', 'quarumcumque', 'quibuscumque', 'quoscumque', 'quascumque']

# unuscumque
que_exceptions += ['unusquisque', 'unaquaeque', 'unumquodque', 'unumquidque', 'uniuscuiusque', 'unicuique', 'unumquemque', 'unamquamque', 'unoquoque', 'unaquaque']

# plerusque
que_exceptions += ['plerusque', 'pleraque', 'plerumque', 'plerique', 'pleraeque', 'pleroque', 'pleramque', 'plerorumque', 'plerarumque', 'plerisque', 'plerosque', 'plerasque']

# misc
que_exceptions += ['absque', 'abusque', 'adaeque', 'adusque', 'aeque', 'antique', 'atque', 'circumundique', 'conseque', 'cumque', 'cunque', 'denique', 'deque', 'donique', 'hucusque', 'inique', 'inseque', 'itaque', 'longinque', 'namque', 'neque', 'oblique', 'peraeque', 'praecoque', 'propinque', 'qualiscumque', 'quandocumque', 'quandoque', 'quantuluscumque', 'quantumcumque', 'quantuscumque', 'quinque', 'quocumque', 'quomodocumque', 'quomque', 'quotacumque', 'quotcumque', 'quotienscumque', 'quotiensque', 'quotusquisque', 'quousque', 'relinque', 'simulatque', 'torque', 'ubicumque', 'ubique', 'undecumque', 'undique', 'usque', 'usquequaque', 'utcumque', 'utercumque', 'utique', 'utrimque', 'utrique', 'utriusque', 'utrobique', 'utrubique']

ne_exceptions += ['absone', 'acharne', 'acrisione', 'acumine', 'adhucine', 'adsuetudine', 'aeetine', 'aeschynomene', 'aesone', 'agamemnone', 'agmine', 'albane', 'alcyone', 'almone', 'alsine', 'amasene', 'ambitione', 'amne', 'amoene', 'amymone', 'anadyomene', 'andrachne', 'anemone', 'aniene', 'anne', 'antigone', 'aparine', 'apolline', 'aquilone', 'arachne', 'arne', 'arundine', 'ascanione', 'asiane', 'asine', 'aspargine', 'babylone', 'barine', 'bellone', 'belone', 'bene', 'benigne', 'bipenne', 'bizone', 'bone', 'bubone', 'bulbine', 'cacumine', 'caligine', 'calymne', 'cane', 'carcine', 'cardine', 'carmine', 'catacecaumene', 'catone', 'cerne', 'certamine', 'chalbane', 'chamaedaphne', 'chamaemyrsine', 'chaone', 'chione', 'christiane', 'clymene', 'cognomine', 'commagene', 'commune', 'compone', 'concinne', 'condicione', 'condigne', 'cone', 'confine', 'consone', 'corone', 'crastine', 'crepidine', 'crimine', 'crine', 'culmine', 'cupidine', 'cyane', 'cydne', 'cyllene', 'cyrene', 'daphne', 'depone', 'desine', 'dicione', 'digne', 'dine', 'dione', 'discrimine', 'diutine', 'dracone', 'dulcedine', 'elatine', 'elephantine', 'elleborine', 'epidamne', 'erigone', 'euadne', 'euphrone', 'euphrosyne', 'examine', 'faune', 'femine', 'feminine', 'ferrugine', 'fine', 'flamine', 'flumine', 'formidine', 'fragmine', 'fraterne', 'fulmine', 'fune', 'germane', 'germine', 'geryone', 'gorgone', 'gramine', 'grandine', 'haecine', 'halcyone', 'hammone', 'harundine', 'hedone', 'helene', 'helxine', 'hermione', 'heroine', 'hesione', 'hicine', 'hicne', 'hierabotane', 'hippocrene', 'hispane', 'hodierne', 'homine', 'hominesne', 'hortamine', 'hucine', 'humane', 'hunccine', 'huncine', 'iasione', 'iasone', 'igne', 'imagine', 'immane', 'immune', 'impoene', 'impone', 'importune', 'impune', 'inane', 'inconcinne', 'indagine', 'indigne', 'inferne', 'inguine', 'inhumane', 'inpone', 'inpune', 'insane', 'insigne', 'inurbane', 'ismene', 'istucine', 'itone', 'iuuene', 'karthagine', 'labiene', 'lacedaemone', 'lanugine', 'latine', 'legione', 'lene', 'lenone', 'libidine', 'limine', 'limone', 'lumine', 'magne', 'maligne', 'mane', 'margine', 'marone', 'masculine', 'matutine', 'medicamine', 'melpomene', 'memnone', 'mesene', 'messene', 'misene', 'mitylene', 'mnemosyne', 'moderamine', 'moene', 'mone', 'mortaline', 'mucrone', 'munimine', 'myrmidone', 'mytilene', 'necne', 'neptune', 'nequene', 'nerine', 'nocturne', 'nomine', 'nonne', 'nullane', 'numine', 'nuncine', 'nyctimene', 'obscene', 'obsidione', 'oenone', 'omine', 'omne', 'oppone', 'opportune', 'ordine', 'origine', 'orphne', 'oxymyrsine', 'paene', 'pallene', 'pane', 'paraetacene', 'patalene', 'pectine', 'pelagine', 'pellene', 'pene', 'perbene', 'perbenigne', 'peremne', 'perenne', 'perindigne', 'peropportune', 'persephone', 'phryne', 'pirene', 'pitane', 'plane', 'pleione', 'plene', 'pone', 'praefiscine', 'prasiane', 'priene', 'priuigne', 'procne', 'proditione', 'progne', 'prone', 'propone', 'pulmone', 'pylene', 'pyrene', 'pythone', 'ratione', 'regione', 'religione', 'remane', 'retine', 'rhene', 'rhododaphne', 'robigine', 'romane', 'roxane', 'rubigine', 'sabine', 'sane', 'sanguine', 'saturne', 'seditione', 'segne', 'selene', 'semine', 'semiplene', 'sene', 'sepone', 'serene', 'sermone', 'serrane', 'siccine', 'sicine', 'sine', 'sithone', 'solane', 'sollemne', 'somne', 'sophene', 'sperne', 'spiramine', 'stamine', 'statione', 'stephane', 'sterne', 'stramine', 'subpone', 'subtegmine', 'subtemine', 'sulmone', 'superne', 'supine', 'suppone', 'susiane', 'syene', 'tantane', 'tantine', 'taprobane', 'tegmine', 'telamone', 'temne', 'temone', 'tene', 'testudine', 'theophane', 'therone', 'thyone', 'tiberine', 'tibicine', 'tiburne', 'tirone', 'tisiphone', 'torone', 'transitione', 'troiane', 'turbine', 'turne', 'tyrrhene', 'uane', 'uelamine', 'uertigine', 'uesane', 'uimine', 'uirgine', 'umbone', 'unguine', 'uolumine', 'uoragine', 'urbane', 'uulcane', 'zone']

n_exceptions += ['aenean', 'agmen', 'alioquin', 'an', 'attamen', 'carmen', 'certamen', 'cognomen', 'crimen', 'dein', 'discrimen', 'en', 'epitheton', 'exin', 'flumen', 'forsan', 'forsitan', 'fulmen', 'hymen', 'iason', 'in', 'limen', 'liquamen', 'lumen', 'nomen', 'non', 'numen', 'omen', 'orion', 'quin', 'semen', 'specimen', 'tamen', 'titan']
 
# English words; this list added to better handle English header, navigation, etc. in plaintext files of the Latin Library corpus.
n_exceptions += ['alcuin', 'caen', 'christian', 'chronicon', 'châtillon', 'claudian', 'john', 'justin', 'latin', 'lucan', 'martin', 'novatian', 'quintilian', 'roman', 'tertullian']

ue_exceptions += ['agaue', 'ambigue', 'assidue', 'aue', 'boue', 'breue', 'calue', 'caue', 'ciue', 'congrue', 'contigue', 'continue', 'curue', 'exigue', 'exue', 'fatue', 'faue', 'fue', 'furtiue', 'gradiue', 'graue', 'ignaue', 'incongrue', 'ingenue', 'innocue', 'ioue', 'lasciue', 'leue', 'moue', 'mutue', 'naue', 'neue', 'niue', 'perexigue', 'perspicue', 'pingue', 'praecipue', 'praegraue', 'prospicue', 'proterue', 'remoue', 'resolue', 'saeue', 'salue', 'siue', 'solue', 'strenue', 'sue', 'summoue', 'superflue', 'supplicue', 'tenue', 'uiue', 'ungue', 'uoue']

ve_exceptions += ['agave', 'ave', 'bove', 'breve', 'calve', 'cave', 'cive', 'curve', 'fave', 'furtive', 'gradive', 'grave', 'ignave', 'iove', 'lascive', 'leve', 'move', 'nave', 'neve', 'nive', 'praegrave', 'prospicve', 'proterve', 'remove', 'resolve', 'saeve', 'salve', 'sive', 'solve', 'summove', 'vive', 'vove']

st_exceptions += ['abest', 'adest', 'ast', 'deest', 'est', 'inest', 'interest', 'post', 'potest', 'prodest', 'subest', 'superest']

latin_exceptions = list(set(que_exceptions
    + ne_exceptions
    + n_exceptions
    + ue_exceptions
    + ve_exceptions
    + st_exceptions
    ))
