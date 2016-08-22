from collections import ChainMap

# Wordlists for conjunctions, prepositions, and interjections based on Allen & Greenough; ambiguous forms removed

CONJUNCTIONS = ['-que', '-ue', '-ve', 'at', 'atque', 'atqui', 'attamen', 'aut', 'autem', 'ceu', 'dum', 'dummodo', 'enim', 'enimuero', 'ergo', 'et', 'etenim', 'etiam', 'etiamsi', 'etsi', 'idcirco', 'ideo', 'igitur', 'inde', 'itaque', 'itidem', 'nam', 'namque', 'neque', 'ni', 'nihilominus', 'nisi', 'praeut', 'proinde', 'prout', 'quamlibet', 'quamobrem', 'quamuis', 'quantumlibet', 'quantumuis', 'quapropter', 'quare', 'quasi', 'que', 'quocirca', 'quoque', 'sed', 'seu', 'si', 'sicut', 'sin', 'siue', 'tamen', 'tametsi', 'tamquam', 'unde', 'ut', 'ue', 'uel', 'uelut', 'ueluti']

CONJUNCTIONS_2 = {'ac': 'atque', 'nec': 'neque'}

PREPOSITIONS = ['ab', 'abs', 'absque', 'ad', 'ante', 'apud', 'cis', 'contra', 'de', 'e', 'erga', 'ex', 'in', 'infra', 'inter', 'iuxta', 'ob', 'per', 'post', 'prae', 'praeter', 'prope', 'propter', 'sub', 'subter', 'super', 'supra', 'trans']

INTERJECTIONS = ['ecce', 'ehem', 'eheu', 'eho', 'ehodum', 'eia', 'en', 'euge', 'euhoe', 'euae', 'euoe', 'heu', 'heus', 'ho', 'io', 'o', 'papae', 'uae', 'uah']

PUNCTUATION = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

IRREGULAR_AMBIGUOUS = ['esse', 'es', 'est', 'estis', 'eram', 'eras', 'ero', 'eris', 'sitis', 'esses', 'esset', 'essemus', 'essetis', 'essent', 'potes', 'poteris', 'potui', 'ire', 'eo', 'is', 'imus', 'eam', 'eas', 'irem', 'ii', 'volo', 'vis', 'voles', 'volet', 'volemus', 'voletis', 'volent', 'velis', 'velles', 'vellet', 'vellemus', 'velletis', 'vellent', 'malo', 'malam', 'malis', 'malitis', 'fero', 'ferimus', 'feram', 'feras', 'fer', 'ferimur', 'ferimini', 'dedi', 'dedit', 'dedimus', 'dederis', 'inquies', 'inque']

SUM = ['esse', 'fuisse', 'sum', 'es', 'est', 'sumus', 'estis', 'sunt', 'eram', 'eras', 'erat', 'eramus', 'eratis', 'erant', 'ero', 'eris', 'erit', 'erimus', 'eritis', 'erunt', 'fui', 'fuisti', 'fuit', 'fuimus', 'fuistis', 'fuerunt', 'fueram', 'fueras', 'fuerat', 'fueramus', 'fueratis', 'fuerant', 'fuero', 'fueris', 'fuerit', 'fuerimus', 'fueritis', 'fuerint', 'sim', 'sis', 'sit', 'simus', 'sitis', 'sint', 'essem', 'esses', 'esset', 'essemus', 'essetis', 'essent', 'fuerim', 'fueris', 'fuerit', 'fuerimus', 'fueritis', 'fuerint', 'fuissem', 'fuisses', 'fuisset', 'fuissemus', 'fuissetis', 'fuissent', 'es', 'este', 'esto', 'esto', 'estote', 'sunto']

POSSUM = ['posse', 'potuisse', 'possum', 'potes', 'potest', 'possumus', 'potestis', 'possunt', 'poteram', 'poteras', 'poterat', 'poteramus', 'poteratis', 'poterant', 'potero', 'poteris', 'poterit', 'poterimus', 'poteritis', 'poterunt', 'potui', 'potuisti', 'potuit', 'potuimus', 'potuistis', 'potuerunt', 'potueram', 'potueras', 'potuerat', 'potueramus', 'potueratis', 'potuerant', 'potuero', 'potueris', 'potuerit', 'potuerimus', 'potueritis', 'potuerint', 'possim', 'possis', 'possit', 'possimus', 'possitis', 'possint', 'possem', 'posses', 'posset', 'possemus', 'possetis', 'possent', 'potuerim', 'potueris', 'potuerit', 'potuerimus', 'potueritis', 'potuerint', 'potuissem', 'potuisses', 'potuisset', 'potuissemus', 'potuissetis', 'potuissent', 'potes', 'poteste', 'potesto', 'potesto', 'potestote', 'possunto']

EO = ['ire', 'isse', 'ivisse', 'eo', 'is', 'it', 'imus', 'itis', 'eunt', 'ibam', 'ibas', 'ibat', 'ibamus', 'ibatis', 'ibant', 'ibo', 'ibis', 'ibit', 'ibimus', 'ibitis', 'ibunt', 'ivi', 'ivisti', 'ivit', 'ivimus', 'ivistis', 'iverunt', 'iveram', 'iveras', 'iverat', 'iveramus', 'iveratis', 'iverant', 'ivero', 'iveris', 'iverit', 'iverimus', 'iveritis', 'iverint', 'eam', 'eas', 'eat', 'eamus', 'eatis', 'eant', 'irem', 'ires', 'iret', 'iremus', 'iretis', 'irent', 'iverim', 'iveris', 'iverit', 'iverimus', 'iveritis', 'iverint', 'ivissem', 'ivisses', 'ivisset', 'ivissemus', 'ivissetis', 'ivissent', 'i', 'ite', 'ito', 'ito', 'itote', 'eunto', 'ii', 'iisti', 'iit', 'iimus', 'iistis', 'ierunt']

VOLO = ['velle', 'voluisse', 'volo', 'vis', 'vult', 'volumus', 'vultis', 'volunt', 'volebam', 'volebas', 'volebat', 'volebamus', 'volebatis', 'volebant', 'volam', 'voles', 'volet', 'volemus', 'voletis', 'volent', 'volui', 'voluisti', 'voluit', 'voluimus', 'voluistis', 'voluerunt', 'volueram', 'volueras', 'voluerat', 'volueramus', 'volueratis', 'voluerant', 'voluero', 'volueris', 'voluerit', 'voluerimus', 'volueritis', 'voluerint', 'velim', 'velis', 'velit', 'velimus', 'velitis', 'velint', 'vellem', 'velles', 'vellet', 'vellemus', 'velletis', 'vellent', 'voluerim', 'volueris', 'voluerit', 'voluerimus', 'volueritis', 'voluerint', 'voluissem', 'voluisses', 'voluisset', 'voluissemus', 'voluissetis', 'voluissent']

NOLO = ['nolle', 'noluisse', 'nolo', 'nolumus', 'nolunt', 'nolebam', 'nolebas', 'nolebat', 'nolebamus', 'nolebatis', 'nolebant', 'nolam', 'noles', 'nolet', 'nolemus', 'noletis', 'nolent', 'nolui', 'noluisti', 'noluit', 'noluimus', 'noluistis', 'noluerunt', 'nolueram', 'nolueras', 'noluerat', 'nolueramus', 'nolueratis', 'noluerant', 'noluero', 'nolueris', 'noluerit', 'noluerimus', 'nolueritis', 'noluerint', 'nolim', 'nolis', 'nolit', 'nolimus', 'nolitis', 'nolint', 'nollem', 'nolles', 'nollet', 'nollemus', 'nolletis', 'nollent', 'noluerim', 'nolueris', 'noluerit', 'noluerimus', 'nolueritis', 'noluerint', 'noluissem', 'noluisses', 'noluisset', 'noluissemus', 'noluissetis', 'noluissent', 'noli', 'nolite', 'nolito', 'nolito', 'nolitote', 'nolunto']

MALO = ['malle', 'maluisse', 'malo', 'mavis', 'mavult', 'malumus', 'mavultis', 'malunt', 'malebam', 'malebas', 'malebat', 'malebamus', 'malebatis', 'malebant', 'malam', 'males', 'malet', 'malemus', 'maletis', 'malent', 'malui', 'maluisti', 'maluit', 'maluimus', 'maluistis', 'maluerunt', 'malueram', 'malueras', 'maluerat', 'malueramus', 'malueratis', 'maluerant', 'maluero', 'malueris', 'maluerit', 'maluerimus', 'malueritis', 'maluerint', 'malim', 'malis', 'malit', 'malimus', 'malitis', 'malint', 'mallem', 'malles', 'mallet', 'mallemus', 'malletis', 'mallent', 'maluerim', 'malueris', 'maluerit', 'maluerimus', 'malueritis', 'maluerint', 'maluissem', 'maluisses', 'maluisset', 'maluissemus', 'maluissetis', 'maluissent']

FERO = ['ferre', 'tulisse', 'fero', 'fers', 'fert', 'ferimus', 'fertis', 'ferunt', 'ferebam', 'ferebas', 'ferebat', 'ferebamus', 'ferebatis', 'ferebant', 'feram', 'feres', 'feret', 'feremus', 'feretis', 'ferent', 'tuli', 'tulisti', 'tulit', 'tulimus', 'tulistis', 'tulerunt', 'tuleram', 'tuleras', 'tulerat', 'tuleramus', 'tuleratis', 'tulerant', 'tulero', 'tuleris', 'tulerit', 'tulerimus', 'tuleritis', 'tulerint', 'feram', 'feras', 'ferat', 'feramus', 'feratis', 'ferant', 'ferrem', 'ferres', 'ferret', 'ferremus', 'ferretis', 'ferrent', 'tulerim', 'tuleris', 'tulerit', 'tulerimus', 'tuleritis', 'tulerint', 'tulissem', 'tulisses', 'tulisset', 'tulissemus', 'tulissetis', 'tulissent', 'fer', 'ferte', 'ferto', 'ferto', 'fertote', 'ferunto', 'feror', 'ferris', 'fertur', 'ferimur', 'ferimini', 'feruntur', 'ferebar', 'ferebaris', 'ferebatur', 'ferebamur', 'ferebamini', 'ferebantur', 'ferar', 'fereris', 'feretur', 'feremur', 'feremini', 'ferentur', 'ferar', 'feraris', 'feratur', 'feramur', 'feramini', 'ferantur', 'ferrer', 'ferreris', 'ferretur', 'ferremur', 'ferremini', 'ferrentur', 'ferre', 'ferimini', 'fertor', 'fertor', 'feruntor']

FIO = ['fieri', 'fio', 'fis', 'fit', 'fimus', 'fitis', 'fiunt', 'fiebam', 'fiebas', 'fiebat', 'fiebamus', 'fiebatis', 'fiebant', 'fiam', 'fies', 'fiet', 'fiemus', 'fietis', 'fient', 'fiam', 'fias', 'fiat', 'fiamus', 'fiatis', 'fiant', 'fierem', 'fieres', 'fieret', 'fieremus', 'fieretis', 'fierent', 'fi', 'fite']

DO = ['dare', 'dedisse', 'do', 'das', 'dat', 'damus', 'datis', 'dant', 'dabam', 'dabas', 'dabat', 'dabamus', 'dabatis', 'dabant', 'dabo', 'dabis', 'dabit', 'dabimus', 'dabitis', 'dabunt', 'dedi', 'dedisti', 'dedit', 'dedimus', 'dedistis', 'dederunt', 'dederam', 'dederas', 'dederat', 'dederamus', 'dederatis', 'dederant', 'dedero', 'dederis', 'dederit', 'dederimus', 'dederitis', 'dederint', 'dem', 'duim', 'des', 'duis', 'det', 'duit', 'demus', 'duimus', 'detis', 'duitis', 'dent', 'duint', 'darem', 'dares', 'daret', 'daremus', 'daretis', 'darent', 'dederim', 'dederis', 'dederit', 'dederimus', 'dederitis', 'dederint', 'dedissem', 'dedisses', 'dedisset', 'dedissemus', 'dedissetis', 'dedissent', 'da', 'date', 'dato', 'dato', 'datote', 'danto', 'dor', 'daris', 'datur', 'damur', 'damini', 'dantur', 'dabar', 'dabaris', 'dabatur', 'dabamur', 'dabamini', 'dabantur', 'dabor', 'daberis', 'dabitur', 'dabimur', 'dabimini', 'dabuntur', 'der', 'deris', 'detur', 'demur', 'demini', 'dentur', 'darer', 'dareris', 'daretur', 'daremur', 'daremini', 'darentur', 'dare', 'damini', 'dator', 'dator', 'dantor']

INQUAM = ['inquam', 'inquis', 'inquit', 'inquimus', 'inquitis', 'inquiunt', 'inquiebat', 'inquies', 'inquiet', 'inquii', 'inquisti', 'inquit', 'inquiat', 'inque', 'inquito', 'inquito']

# Add participles?

SUM = [item for item in SUM if item not in IRREGULAR_AMBIGUOUS]
POSSUM = [item for item in POSSUM if item not in IRREGULAR_AMBIGUOUS]
EO = [item for item in EO if item not in IRREGULAR_AMBIGUOUS]
VOLO = [item for item in VOLO if item not in IRREGULAR_AMBIGUOUS]
MALO = [item for item in MALO if item not in IRREGULAR_AMBIGUOUS]
NOLO = [item for item in NOLO if item not in IRREGULAR_AMBIGUOUS]
FERO = [item for item in FERO if item not in IRREGULAR_AMBIGUOUS]
FIO = [item for item in FIO if item not in IRREGULAR_AMBIGUOUS]
DO = [item for item in DO if item not in IRREGULAR_AMBIGUOUS]
INQUAM = [item for item in INQUAM if item not in IRREGULAR_AMBIGUOUS]

SUM = {item: 'sum' for item in SUM}
POSSUM = {item: 'possum' for item in POSSUM}
EO = {item: 'eo' for item in EO}
VOLO = {item: 'volo' for item in VOLO}
MALO = {item: 'malo' for item in MALO}
NOLO = {item: 'nolo' for item in NOLO}
FERO = {item: 'fero' for item in FERO}
FIO = {item: 'fio' for item in FIO}
DO = {item: 'do' for item in DO}
INQUAM = {item: 'inquam' for item in INQUAM}

IRREGULAR_VERBS = dict(ChainMap(SUM, POSSUM, EO, VOLO, MALO, NOLO, FERO, FIO, DO, INQUAM))

PUNCTUATION = {item: 'punc' for item in PUNCTUATION}

MODEL_LIST = CONJUNCTIONS + PREPOSITIONS + INTERJECTIONS 
MODEL = {item: item for item in MODEL_LIST}
MODEL = dict(ChainMap(MODEL,CONJUNCTIONS_2))

LATIN_MODEL = dict(ChainMap(MODEL, IRREGULAR_VERBS, PUNCTUATION))

