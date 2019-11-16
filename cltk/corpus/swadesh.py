"""Generate Swadesh lists for classical languages"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

swadesh_eng_old = ['ic, iċċ, ih', 'þū', 'hē', 'wē', 'ġē', 'hīe', 'þēs, þēos, þis', 'sē, sēo, þæt', 'hēr',
                   'þār, þāra, þǣr, þēr', 'hwā', 'hwā, hwæt', 'hwǣr', 'hwanne, hwænne, hwenne', 'hū', 'ne', 'eall',
                   'maniġ, feola, fela', 'sum', 'fēaw, lyt', 'ōþer', 'ān', 'twēġen, twā, tū', 'þrīe, þrēo', 'fēower',
                   'fīf', 'grēat, stōr', 'lang, long', 'wīd, brād', 'þicce', 'hefiġ', 'smæl', 'scort, sceort',
                   'eng, nearu', 'þynn', 'ides, cwēn, wīfmann', 'wer, guma', 'mann', 'ċild, bearn, umbor', 'wīf',
                   'bunda, banda, hūsbonda', 'mōdor', 'fæder', 'dēor', 'fisc', 'fugol', 'hund', 'lūs', 'snaca', 'wyrm',
                   'trēo, bēam', 'weald, fyrhþ', 'sticca', 'wæstm, blǣd, ofett', 'sǣd', 'blæd, lēaf', 'wyrt', 'rind',
                   'blǣd, blōstma', 'græs, gærs', 'rāp, līne, sāl', 'hȳd', 'flǣsc', 'blōd', 'bān', 'fǣtt', 'ǣġ', 'horn',
                   'steort, tæġl', 'feþer', 'hǣr, hēr', 'hēafod, hafola', 'ēare', 'ēaġe', 'nosu', 'mūþ', 'tōþ', 'tunge',
                   'fingernæġel', 'fōt', 'scanca', 'cnēo', 'hand', 'feþera', 'būc', 'þearm', 'heals, hnecca',
                   'hryċġ, bæc', 'brēost', 'heorte', 'lifer', 'drincan', 'etan', 'bītan', 'sūgan, sūcan',
                   'spittan, hrǣċan', 'spīwan', 'blāwan', 'ōþian, ēþian', 'hliehhan', 'sēon', 'hīeran', 'witan, cnāwan',
                   'þenċan', 'ēþian, stincan', 'andrǣdan', 'slǣpan', 'libban, lifian', 'steorfan', 'cwellan', 'feohtan',
                   'huntian', 'hittan, slēan', 'snīþan', 'splātan, clēofan', 'snǣsan, stingan, stician',
                   'screpan, clifrian, pliċġan, clāwian', 'grafan', 'swimman, flēotan', 'flēoġan', 'gangan, onsteppan',
                   'cuman', 'liċġan', 'sittan', 'standan', 'ċierran, hwierfan', 'feallan', 'ġiefan', 'healdan',
                   'þringan, cwȳsan', 'gnīdan', 'wascan', 'wīpian', 'dragan, pullian',
                   'scūfan, þyddan, hrindan, potian', 'weorpan', 'bindan, tīeġan', 'sīwian, sēowian', 'tellan',
                   'cweþan, seċġan', 'singan', 'lācan, pleġan', 'flēotan, flotian, floterian', 'flōwan', 'frēosan',
                   'swellan', 'sōl, sunne', 'mōna', 'steorra, tungol', 'wæter', 'reġn', 'ēa, flōd, strēam',
                   'mere, lacu', 'sǣ', 'sealt', 'stān', 'sand', 'dūst, dust', 'eorþe', 'wolcen', 'mist', 'rodor, lyft',
                   'wind', 'snāw', 'īs', 'rēc, smoca', 'fȳr', 'æsc', 'beornan, biernan, bærnan, ǣlan', 'weġ, pæþ',
                   'beorg', 'rēad', 'grēne', 'ġeolu', 'hwīt', 'sweart, blæc', 'neaht, niht', 'dōgor, dæġ', 'ġēar',
                   'wearm', 'ceald', 'full', 'nēowe, nīwe', 'gamol, eald', 'gōd', 'yfel', 'fūl', 'ādeliht, sol',
                   'ġerād, ġereclīc', 'hwyrflede, seonuwealt', 'scearp', 'dol, dwæs', 'slīc, slieht, smēþe, smōþ',
                   'wǣt', 'sēar, drȳġe', 'riht', 'nēah', 'wīd, feor', 'reht, riht', 'winstre', 'on, æt', 'in', 'mid',
                   'and', 'ġif', 'forþon', 'nama']

swadesh_gr = ['ἐγώ', 'σύ', 'αὐτός, οὗ, ὅς, ὁ, οὗτος', 'ἡμεῖς', 'ὑμεῖς', 'αὐτοί', 'ὅδε', 'ἐκεῖνος',
              'ἔνθα, ἐνθάδε, ἐνταῦθα', 'ἐκεῖ', 'τίς', 'τί', 'ποῦ, πόθι', 'πότε, πῆμος', 'πῶς', 'οὐ, μή', 'πᾶς, ἅπᾱς',
              'πολύς', 'τις', 'ὀλίγος, βαιός, παῦρος', 'ἄλλος, ἕτερος', 'εἷς', 'δύο', 'τρεῖς', 'τέσσαρες', 'πέντε',
              'μέγας', 'μακρός', 'εὐρύς', 'πυκνός', 'βαρύς', 'μῑκρός', 'βραχύς', 'στενός', 'μανός', 'γυνή', 'ἀνήρ',
              'ἄνθρωπος', 'τέκνον, παῖς, παιδίον', 'γυνή', 'ἀνήρ', 'μήτηρ', 'πατήρ', 'ζῷον', 'ἰχθύς', 'ὄρνις, πετεινόν',
              'κύων', 'φθείρ', 'ὄφις', 'ἑρπετόν, σκώληξ, ἕλμινς', 'δένδρον', 'ὕλη', 'βακτηρία, ῥάβδος', 'καρπός',
              'σπέρμα', 'φύλλον', 'ῥίζα', 'φλοιός', 'ἄνθος', 'χλόη', 'δεσμός, σχοινίον', 'δέρμα', 'κρέας', 'αἷμα',
              'ὀστοῦν', 'δημός', 'ᾠόν', 'κέρας', 'οὐρά, κέρκος', 'πτερόν', 'θρίξ, κόμη', 'κεφαλή', 'οὖς', 'ὀφθαλμός',
              'ῥίς', 'στόμα', 'ὀδούς', 'γλῶσσα', 'ὄνυξ', 'πούς', 'κῶλον, σκέλος', 'γόνυ', 'χείρ', 'πτέρυξ',
              'γαστήρ, κοιλία', 'ἔντερα, σπλάγχνα', 'αὐχήν, τράχηλος', 'νῶτον', 'μαστός, στῆθος', 'καρδία', 'ἧπαρ',
              'πίνω', 'ἐσθίω, ἔφαγον', 'δάκνω', 'σπάω', 'πτύω', 'ἐμέω', 'φυσάω', 'πνέω', 'γελάω', 'βλέπω, ὁράω, εἶδον',
              'ἀκούω, ἀΐω', 'οἶδα, γιγνώσκω', 'νομίζω, δοκέω, νοέω, οἴομαι', 'ὀσφραίνομαι', 'φοβέομαι',
              'καθεύδω, εὕδω, εὐνάζομαι, κοιμάομαι, ἰαύω', 'ζάω, βιόω, οἰκέω', 'ἀποθνῄσκω, θνῄσκω, τελευτάω, ὄλομαι',
              'ἀποκτείνω, ἔπεφνον', 'μάχομαι', 'θηρεύω, θηράω, ἰχνεύω, κυνηγετέω, κυνηγέω, σεύω', 'τύπτω', 'τέμνω',
              'σχίζω', 'κεντέω', 'κνάω', 'ὀρύσσω, σκᾰ́πτω', 'νέω, κολυμβάω', 'πέτομαι',
              'περιπατέω, πατέω, στείχω, βαίνω, βαδίζω, πεζεύω, πορεύω', 'ἱκνέομαι, ἵκω, ἔρχομαι, εἶμι', 'κεῖμαι',
              'καθίζω', 'ἵστημι', 'τρέπω', 'πίπτω', 'παρέχω, δίδωμι', 'ἔχω', 'πιέζω', 'τρίβω', 'λούω, πλύνω, νίπτω',
              'ἀπομάσσω', 'ἕλκω', 'ὠθέω', 'ῥίπτω, βάλλω', 'δέω', 'ῥάπτω', 'ἀριθμέω', 'φημί, λέγω, ἐνέπω', 'ἀείδω',
              'παίζω', 'νέω', 'ῥέω', 'πήγνυμαι', 'αὐξάνω', 'ἥλιος', 'σελήνη', 'ἀστήρ', 'ὕδωρ', 'ὑετός, βροχή',
              'ποταμός', 'λίμνη', 'θάλασσα, πέλαγος, πόντος', 'ἅλς', 'λίθος', 'ἄμμος', 'κόνις', 'γῆ, χθών', 'νέφος',
              'ὀμίχλη', 'οὐρανός', 'ἄνεμος', 'χιών', 'κρύσταλλος', 'καπνός', 'πῦρ', 'τέφρα', 'καίω', 'ὁδός',
              'ἄκρα, ὄρος, βουνός', 'ἐρυθρός, πυρρός', 'χλωρός', 'ξανθός', 'λευκός', 'μέλας', 'νύξ', 'ἡμέρα, ἦμαρ',
              'ἔτος', 'θερμός', 'ψυχρός', 'μεστός, πλήρης', 'νέος', 'παλαιός', 'ἀγαθός', 'κακός', 'σαπρός', 'θολερός',
              'εὐθύς, ὀρθός', 'κυκλοτερής', 'τομός, ὀξύς', 'ἀμβλύς, βαρύς', 'λεῖος', 'ὑγρός', 'ξηρός', 'δίκαιος',
              'ἐγγύς', 'μακράν', 'δεξιός', 'ἀριστερός, εὐώνυμος', 'ἐν', 'ἐν', 'μετά, σύν', 'καί, τε', 'εἰ', 'ὅτι',
              'ὄνομα']

swadesh_hi = ['मैं', 'तू', 'वह', 'हम', 'तुम', 'वे', 'यह', 'वह', 'यहाँ', 'वहाँ', 'कौन', 'क्या', 'कहाँ', 'कब', 'कैसा',
              'नहीं', 'सब', 'बहुत', 'कुछ', 'थोड़ा', 'दूसरा', 'एक', 'दो', 'तीन', 'चार', 'पाँच', 'बड़ा', 'लम्बा', 'चौड़ा',
              'गाढ़ा', 'भारी', 'छोटा', 'छोटा', 'तंग', 'पतला', 'औरत', 'आदमी', 'इंसान', 'बच्चा', 'पत्नी', 'पति', 'माता',
              'पिता', 'जानवर', 'मछली', 'चिड़िया', 'कुत्ता', 'जूँ', 'साँप', 'कीड़ा', 'पेड़', 'जंगल', 'डण्डा', 'फल',
              'बीज', 'पत्ता', 'जड़', 'छाल', 'फूल', 'घास', 'रस्सी', 'त्वचा', 'माँस', 'ख़ून', 'हड्डी', 'चरबी', 'अंडा',
              'सींग', 'पूँछ', 'पंख', 'बाल', 'सर', 'कान', 'आँख', 'नाक', 'मुँह', 'दाँत', 'जीभ', 'नाख़ुन', 'पैर', 'टांग',
              'घुटना', 'हाथ', 'पंख', 'पेट', 'अंतड़ी', 'गरदन', 'पीठ', 'छाती', 'दिल', 'जिगर', 'पीना', 'खाना', 'काटना',
              'चूसना', 'थूकना', 'उल्टी करना', 'फूँक मारना', 'साँस लेना', 'हँसना', 'देखना', 'सुनना', 'जानना', 'सोचना',
              'सूंघना', '(से) डरना ((se) ḍarnā', 'सोना', 'जीना', 'मरना', 'मारना', 'लड़ना', 'शिकार करना', 'मारना',
              'काटना', 'बंटना', 'भोंकना', 'खरोंचना', 'खोदना', 'तैरना', 'उड़ना', 'चलना', 'आना', 'लेटना', 'बैठना',
              'खड़ा होना', 'मुड़ना', 'गिरना', 'देना', 'पकड़ना', 'घुसा देना', 'मलना', 'धोना', 'पोंछना', 'खींचना',
              'धक्का देना', 'फेंकना', 'बाँधना', 'सीना', 'गिनना', 'कहना', 'गाना', 'खेलना', 'तैरना', 'बहना', 'जमना',
              'सूजना', 'सूरज', 'चांद', 'तारा', 'पानी', 'बारिश', 'नदी', 'झील', 'समन्दर', 'नमक', 'पत्थर', 'रेत', 'धूल',
              'धरती', 'बादल', 'धुंध', 'आसमान', 'हवा', 'बर्फ़', 'बर्फ़', 'धुआँ', 'आग', 'राख', 'जलना', 'सड़क', 'पहाड़',
              'लाल', 'हरा', 'पीला', 'सफ़ेद', 'काला', 'रात', 'दिन', 'साल', 'गर्म', 'ठंडा', 'पूरा', 'नया', 'पुराना',
              'अच्छा', 'बुरा', 'सड़ा', 'गन्दा', 'सीधा', 'गोल', 'तीखा', 'कुंद', 'चिकना', 'गीला', 'सूखा', 'सही', 'नज़दीक',
              'दूर', 'दायाँ', 'बायाँ', 'पे', 'में', 'के साथ', 'और', 'अगर', 'क्योंकि', 'नाम']


swadesh_la = ['ego', 'tū', 'is, ea, id', 'nōs', 'vōs', 'eī, iī, eae, ea', 'hic, haec, hoc', 'ille, illa, illud', 'hīc',
              'illic, ibi', 'quis, quae', 'quid', 'ubi', 'cum', 'quōmodō', 'nōn, nē', 'omnēs, omnia',
              'multī, multae, multa', 'aliquī, aliqua, aliquod', 'paucī, paucae, pauca', 'alter, alius', 'ūnus', 'duō',
              'trēs', 'quattuor', 'quīnque', 'magnus', 'longus', 'lātus', 'crassus', 'gravis', 'parvus', 'brevis',
              'angustus', 'gracilis', 'fēmina', 'vir', 'homō', 'puer', 'uxor, mulier', 'marītus', 'māter', 'pater',
              'animal', 'piscis', 'avis', 'canis', 'pēdīculus', 'serpens', 'vermis', 'arbor', 'silva', 'hasta, pālus',
              'fructus', 'sēmen', 'folium', 'rādix', 'cortex', 'flōs', 'herba', 'chorda', 'cutis', 'carō', 'sanguis',
              'os', 'pinguāmen', 'ōvum', 'cornū', 'cauda', 'penna', 'pilus', 'caput', 'auris', 'oculus', 'nāsus, nāris',
              'ōs', 'dens', 'lingua', 'unguis', 'pēs', 'crūs', 'genū', 'manus', 'āla', 'venter, abdōmen', 'viscera',
              'cervix', 'dorsum', 'mamma', 'cor', 'iecur', 'bibere', 'edere', 'mordēre', 'sūgere', 'spuere', 'vomere',
              'īnflāre', 'respīrāre', 'rīdēre', 'vidēre', 'audīre', 'scīre', 'cōgitāre, putāre, existimāre', 'olfacere',
              'timēre', 'dormīre', 'vīvere', 'morī', 'necāre', 'luctārī', 'vēnārī', 'pellere', 'secāre', 'dīvidere',
              'pungere', 'scabere', 'fodere', 'nāre, natāre', 'volāre', 'ambulāre', 'venīre', 'cubāre', 'sedēre',
              'stāre', 'vertere', 'cadere', 'dare', 'tenēre', 'exprimere', 'fricāre', 'lavāre', 'tergēre', 'trahere',
              'pellere', 'iacere', 'ligāre', 'cōnsuere', 'computāre, numerāre', 'dīcere', 'canere', 'ludere',
              'fluctuāre', 'fluere', 'gelāre', 'augēre', 'sol', 'lūna', 'stella', 'aqua', 'pluvia',
              'flūmen, fluvius, amnis', 'lacus', 'mare', 'sal', 'saxum, lapis, petra', 'harēna', 'pulvis',
              'humus, terra, ager', 'nūbēs, nebula', 'cālīgō, nebula, tenebrae', 'caelum', 'ventus', 'nix', 'gelū',
              'fūmus', 'ignis', 'cinis', 'ūrere, flammāre', 'via', 'mons', 'ruber, rūfus', 'viridis', 'croceus',
              'albus, candidus', 'āter, niger', 'nox', 'dies', 'annus', 'calidus', 'frigidus', 'plēnus', 'novus',
              'vetus', 'bonus', 'malus', 'putridus', 'immundus', 'rectus', 'rotundus', 'acūtus', 'hebes', 'suāvis',
              'humidus, aqueus', 'siccus', 'rectus', 'propinquus, proximus', 'longus', 'dexter', 'laevus, sinister',
              'ad, in', 'in', 'cum', 'et, -que', 'si', 'quod', 'nōmen']


swadesh_old_norse = ["ek", "þú", "hann", "vér", "þér", "þeir", "sjá, þessi", "sá", "hér", "þar", "hvar", "hvat", "hvar",
                     "hvenær", "hvé", "eigi", "allr", "margr", "nǫkkurr", "fár", "annarr", "einn", "tveir", "þrír",
                     "fjórir", "fimm", "stórr", "langr", "breiðr", "þykkr", "þungr", "lítill", "stuttr", "mjór",
                     "þunnr", "kona", "karl", "maðr", "barn", "kona", "bóndi", 'móðir', "faðir", "dýrr", "fiskr",
                     "fugl", "hundr", "lús", "snókr", "ormr", "tré", "skógr", "stafr", "ávǫxtr", "fræ", "lauf", "rót",
                     "bǫrkr", "blóm", "gras", "reip", "húð", "kjǫt", "blóð", "bein", "fita", "egg", "horn", "hali",
                     "fjǫðr", "hár", "hǫfuð", "eyra", "auga", "nef", "munnr", "tǫnn", "tunga", "nagl", "fótr", "leggr",
                     "kné", "hǫnd", "vængr", "magi", "iinyfli", "hals", "bak", "brjóst", "hjarta", "lifr", "drekka",
                     "eta", "bíta", "súga", "spýta", ", hrækja", "", "blása", "anda", "hlæja", "sjá", "heyra", "vita",
                     "þýkkja", "þefa", "ugga", "sofa", "lifa", "deyja", "drepa", "hals", "bak", "berja", "skera",
                     "kljúfa""stinga", "klóra", "grafa", "synda", "fljúga", "ganga", "koma", "liggja", "sitja",
                     "standa", "snúa", "falla", "gefa", "halda", "kreista", "gnúa", "þvá", "þurka", "draga", "ýta",
                     "kasta", "kasta", "binda", "sauma", "telja", "segja", "syngja", "leika", "flóta", "streyma",
                     "frjósa", "þrútna", "sól", "tungl", "stjarna", "vatn", "regn", "á", "vatn", "hav", "salt",
                     "steinn", "sandr", "ryk", "jörð", "ský", "þoka", "himinn", "vindr", "snjór", "íss", "reykr", "ild",
                     "eldr", "aska", "brenna", "vegr", "fjall", "rauðr", "grœnn", "gulr", "hvítr", "svartr", "nótt",
                     "dagr", "ár", "heitr", "kaldr", "fullr", "nýr", "gamall", "góðr", "illr", "rottin", "skitinn",
                     "beinn", "kringlóttr", "beittr", "", "sleipr", "blautr", "þurr", "réttr", "nálægr", "langr",
                     "hœgr", "vinstri", "hjá", "í", "með", "ok", "ef", "því at",
                     "nafn"]  # pylint: disable=line-too-long

swadesh_pt_old = ['eu', 'tu', 'ele', 'nos', 'vos', 'eles', 'esto, aquesto', 'aquelo', 'aqui', 'ali', 'quen', 'que', 'u',
                  'quando', 'como', 'non', 'todo', 'muito', 'algũus', 'pouco', 'outro', 'un, ũu', 'dous', 'tres',
                  'quatro', 'cinco', 'grande, gran', 'longo', 'ancho', 'grosso', 'pesado', 'pequeno', 'curto',
                  'estreito', 'magro', 'moller, dona', 'ome', 'ome, pessõa', 'infante, meninno, creatura', 'moller',
                  'marido', 'madre, mãi', 'padre, pai', 'besta, bestia, bescha', 'peixe', 'ave', 'can', 'peollo',
                  'coobra', 'vermen', 'arvor', 'furesta, mata, monte', 'baston, pao', 'fruita, fruito', 'semente',
                  'folla', 'raiz', 'cortiça', 'fror, flor', 'erva', 'corda', 'pele', 'carne', 'sangui, sangue', 'osso',
                  'gordura', 'ovo', 'corno', 'rabo', 'pena', 'cabelo', 'cabeça', 'orella', 'ollo', 'nariz', 'boca',
                  'dente', 'lingua', 'unna, unlla', 'pee, pe', 'perna', 'gẽollo', 'mão', 'aa', 'ventre', 'tripas',
                  'colo', 'costas', 'peito, sẽo', 'coraçon', 'figado', 'bever', 'comer', 'morder', 'mamar', 'cospir',
                  '', 'soprar', '', 'riir', 'veer', 'ouvir, oir, ascuitar', 'saber', 'pensar', 'cheirar', 'temer',
                  'dormir', 'viver', 'morrer', 'matar', 'pelejar', 'caçar', 'bater', 'cortar, partir', '', 'acuitelar',
                  'rascar', 'cavar', 'nadar', 'voar', 'andar', 'vĩir', 'jazer, deitar', 'sentar', 'levantar', '',
                  'caer', 'dar', 'tẽer', 'apertar', '', 'lavar', 'terger, enxugar', 'puxar', 'empuxar', 'lançar',
                  'atar', 'coser', 'contar', 'contar, dizer, falar', 'cantar', 'jogar', 'boiar', 'correr',
                  'gelar, *gear', 'inchar', 'sol', 'lũa', 'estrela', 'agua', 'chuvia', 'rio', 'lago', 'mar', 'sal',
                  'pedra', 'arẽa', 'poo', 'terra', 'nuve', 'nevoeiro', 'ceo', 'vento', 'neve', 'geo', 'fumo, fumaz',
                  'fogo', 'cĩisa', 'queimar, arder', 'caminno, via', 'montanna, monte', 'vermello', 'verde', 'amarelo',
                  'branco', 'negro', 'noite', 'dia', 'ano', 'caente', 'frio', 'chẽo', 'novo', 'vello, antigo',
                  'bon, bõo', 'mal, mao', 'podre', 'lixoso', 'estreito', 'redondo', 'amoado', 'romo', 'chão', 'mollado',
                  'seco', 'reito, dereito', 'preto', 'longe', 'dereita', 'sẽestra', 'a', 'en', 'con', 'e', 'se',
                  'porque', 'nome']

swadesh_sa = ['अहम्', 'त्वम्', 'स', 'वयम्, नस्', 'यूयम्, वस्', 'ते', 'इदम्', 'तत्', 'अत्र', 'तत्र', 'क', 'किम्',
              'कुत्र', 'कदा', 'कथम्', 'न', 'सर्व', 'बहु', 'किञ्चिद्', 'अल्प', 'अन्य', 'एक', 'द्वि', 'त्रि', 'चतुर्',
              'पञ्चन्', 'महत्', 'दीर्घ', 'उरु', 'घन', 'गुरु', 'अल्प', 'ह्रस्व', 'अंहु', 'तनु', 'स्त्री', 'पुरुष, नर',
              'मनुष्य, मानव', 'बाल, शिशु', 'पत्नी, भार्या', 'पति', 'मातृ', 'पितृ', 'पशु', 'मत्स्य', 'वि, पक्षिन्',
              'श्वन्', 'यूका', 'सर्प', 'कृमि', 'वृक्ष, तरु', 'वन', 'दण्ड', 'फल', 'बीज', 'पत्त्र', 'मूल', 'त्वच्',
              'पुष्प', 'तृण', 'रज्जु', 'चर्मन्, त्वच्', 'मांस', 'रक्त, असृज्', 'अस्थि', 'पीवस्, मेदस्', 'अण्ड', 'शृङ्ग',
              'पुच्छ', 'पर्ण', 'केश', 'शिरस्', 'कर्ण', 'अक्षि', 'नासा', 'वक्त्र, मुख', 'दन्त', 'जिह्वा', 'नख', 'पद',
              'जङ्घ', 'जानु', 'हस्त, पाणि', 'पक्ष', 'उदर', 'अन्त्र, आन्त्र, गुद', 'गल, ग्रीवा', 'पृष्ठ', 'स्तन', 'हृदय',
              'यकृत्', 'पिबति', 'खादति, अत्ति', 'दशति', 'धयति', 'ष्ठीवति', 'वमति', 'वाति', 'अनिति', 'स्मयते, हसति',
              'पश्यति, √दृश्', 'शृणोति', 'जानाति', 'मन्यते, चिन्तयति', 'जिघ्रति', 'बिभेति, भयते', 'स्वपिति', 'जीवति',
              'म्रियते', 'हन्ति', 'युध्यते', 'वेति', 'हन्ति, ताडयति', 'कृन्तति', 'भिनत्ति', 'विधति', 'लिखति', 'खनति',
              'प्लवते', 'पतति', 'एति, गच्छति, चरति', 'आगच्छति', 'शेते', 'सीदति', 'तिष्ठति', 'वर्तते', 'पद्यते', 'ददाति',
              'धरति', 'मृद्नाति', 'घर्षति', 'क्षालयति', 'मार्ष्टि', 'कर्षति', 'नुदति', 'क्षिपति', 'बध्नाति, बन्धति',
              'सीव्यति', 'गणयति, कलते', 'वक्ति', 'गायति', 'दीव्यति', 'प्लवते', 'सरति, क्षरति', 'शीयते', 'श्वयति',
              'सूर्य, रवि, सूर, भास्कर', 'मास, चन्द्रमस्, चन्द्र', 'नक्षत्र, स्तृ, तारा',
              'जल, अप्, पानीय, वारि, उदन्, तोज', 'वर्ष', 'नदी', 'सरस्', 'समुद्र', 'लवण', 'अश्मन्', 'पांसु, शिकता',
              'रेणु', 'क्षम्, पृथ्वी', 'नभस्, मेघ', 'मिह्', 'आकाश', 'वायु, वात', 'हिम, तुषार, तुहिन', 'हिम', 'धूम',
              'अग्नि', 'आस', 'दहति', 'पथ, अध्वन्, मार्ग', 'गिरि, पर्वत', 'रक्त, रोहित', 'हरित्, हरित, पालाश, पलाश',
              'पीत, पीतल', 'श्वेत', 'कृष्ण', 'रात्रि, नक्ति, क्षप्, रजनी', 'दिन, अहर्, दिवस', 'वर्ष, संवत्सर', 'तप्त',
              'शीत', 'पूर्ण', 'नव, नूतन', 'जीर्ण, वृद्ध, पुरातन', 'वसु, भद्र', 'पाप, दुष्ट', 'पूति', 'मलिन, समल',
              'ऋजु, साधु', 'वृत्त, वर्तुल', 'तीक्ष्ण', 'कुण्ठ', 'श्लक्ष्ण, स्निग्ध', 'आर्द्र, क्लिन्न', 'शुष्क',
              'शुद्ध, सत्य', 'नेद, प्रति', 'दूर', 'दक्षिण', 'सव्य', 'काश्यां', 'अंतरे, मध्ये', 'सह', 'च', 'यदि', 'हि',
              'नामन्']

swadesh_txb = ['ñäś', 'tuwe', 'su', 'wes', 'yes', 'cey', 'se', 'su, samp', 'tane', 'tane, omp', 'kᵤse', 'kᵤse', 'ente',
               'ente', 'mäkte', 'mā', 'poñc', 'māka', 'ṣemi', 'totka', 'allek', 'ṣe', 'wi', 'trey', 'śtwer', 'piś',
               'orotstse', 'pärkare', 'aurtstse', '', 'kramartse', 'lykaśke, totka', '', '', '', 'klyiye, śana',
               'eṅkwe', 'śaumo', 'śamaśke', 'śana', 'petso', 'mācer', 'pācer', 'luwo', 'laks', 'salamo luwo', 'ku',
               'pärśeriñ', 'arṣāklo, auk', 'yel', 'stām', 'wartto, karāś', 'śakātai', 'oko', 'sārm, śäktālye', 'pilta',
               'witsako', 'enmetre', 'pyāpyo', 'atiyai', '', 'ewe, yetse', 'misa', 'yasar', 'āy, āsta pl', 'ṣalype', '',
               'krorīyai', 'pako', 'paruwa', 'matsi', 'āśce', 'klautso', 'ek', 'meli', 'koyṃ', 'keme', 'kantwo', '',
               'paiyye', 'ckāckai', 'keni', 'ṣar', '', 'kātso', 'kātso', 'kor', 'sark', 'päścane', 'arañce', 'wästarye',
               'yokäṃ', 'śuwaṃ', '', '', 'pitke', 'aṅkaiṃ', 'pinaṣṣnäṃ', 'anāṣṣäṃ, satāṣṣäṃ', 'ker-', 'lkāṣṣäṃ',
               'klyauṣäṃ', 'aiśtär, kärsanaṃ', 'pälskanaṃ', 'warṣṣäṃ', 'prāskaṃ', 'kläntsaṃ', 'śaiṃ', 'sruketär',
               'kauṣäṃ', 'witāre', 'śerītsi', 'karnäṣṣäṃ', 'karsnaṃ, latkanaṃ', 'kautanaṃ', 'tsopäṃ', '', 'rapanaṃ',
               'nāṣṣäṃ', 'pluṣäṃ', 'yaṃ', 'känmaṣṣäṃ', 'lyaśäṃ', 'ṣamäṃ, āṣṣäṃ', 'kaltär', 'kluttaṅktär, sporttotär',
               'kloyotär', 'aiṣṣäṃ', '', 'klupnātär, nuskaṣṣäṃ', 'lyuwetär, kantanatär', 'laikanatär', 'lyyāstär',
               'slaṅktär', 'nätkanaṃ', 'karṣṣäṃ, saläṣṣäṃ', 'śanmästär, kärkaṣṣäṃ', '', 'ṣäṃṣtär', 'weṣṣäṃ', 'piyaṃ',
               'kāñmäṃ', 'pluṣäṃ', 'reṣṣäṃ', '', 'staukkanatär', 'kauṃ', 'meñe', 'ścirye', 'war', 'swese', 'cake',
               'lyam', 'samudtär', 'salyiye', 'kärweñe', 'warañc', 'tweye, taur', 'keṃ', 'tarkär', '', 'iprer', 'yente',
               'śiñcatstse', '', '', 'puwar', 'taur, tweye', 'tsakṣtär,pälketär', 'ytārye', 'ṣale', 'ratre',
               'motartstse', 'tute', 'ārkwi', 'erkent-', 'yṣiye', 'kauṃ', 'pikul', 'emalle', 'krośce', 'ite', 'ñuwe',
               'ktsaitstse', 'kartse', 'yolo, pakwāre', 'āmpau', 'sal, kraketstse', '', '', 'mātre, akwatse', 'mālle',
               'ṣmare', 'karītstse', 'asāre', '', 'akartte, ysape, etsuwai', 'lau, lauke', 'saiwai', 'śwālyai', '-ne',
               '-ne', 'śle', 'ṣp', 'krui, ente', 'kuce, mäkte', 'ñem']

swadesh_syc = ['ܐܢܐ‎', 'ܐܢܬ‎, ܐܢܬܝ‎', 'ܗܘ‎', 'ܚܢܢ‎,, ܐܢܚܢܢ‎', 'ܐܢܬܘܢ‎ , ܐܢܬܝܢ‎ ', 'ܗܢܘܢ‎ , ܗܢܝܢ‎', 'ܗܢܐ‎, ܗܕܐ‎',
               'ܗܘ‎, ܗܝ‎', 'ܗܪܟܐ‎', 'ܬܡܢ‎', 'ܡܢ‎', 'ܡܐ‎, ܡܢ‎, ܡܢܐ‎, ܡܘܢ‎', 'ܐܝܟܐ‎', 'ܐܡܬܝ‎', 'ܐܝܟܢ‎,, ܐܝܟܢܐ‎', 'ܠܐ‎',
               'ܟܠ‎', 'ܣܓܝ‎	', 'ܟܡܐ‎	', 'ܒܨܝܪܐ‎', 'ܐܚܪܢܐ‎, ܐܚܪܬܐ‎', 'ܚܕ‎ , ܚܕܐ‎', 'ܬܪܝܢ‎, ܬܪܬܝܢ‎', 'ܬܠܬܐ‎, ܬܠܬ‎',
               'ܐܪܒܥܐ‎, ܐܪܒܥ‎', 'ܚܡܫܐ‎, ܚܡܫ‎', 'ܪܒܐ‎, ܟܒܝܪܐ‎	', 'ܐܪܝܟܐ‎', 'ܪܘܝܚܐ‎, ܦܬܝܐ‎', 'ܥܒܝܛܐ‎',
               'ܢܛܝܠܐ‎, ܝܩܘܪܐ‎	', 'ܙܥܘܪܐ‎', 'ܟܪܝܐ‎', 'ܥܝܩܐ‎', 'ܪܩܝܩܐ‎, ܛܠܝܚܐ‎', 'ܐܢܬܬܐ‎', 'ܓܒܪܐ‎', 'ܐܢܫܐ‎', 'ܝܠܘܕܐ‎',
               'ܐܢܬܬܐ‎', 'ܒܥܠܐ‎', 'ܐܡܐ‎', 'ܐܒܐ‎', 'ܚܝܘܬܐ‎', 'ܢܘܢܐ‎', 'ܛܝܪܐ‎, ܨܦܪܐ‎', 'ܟܠܒܐ‎', 'ܩܠܡܐ‎', 'ܚܘܝܐ‎',
               'ܬܘܠܥܐ‎', 'ܐܝܠܢܐ‎', 'ܥܒܐ‎', 'ܩܝܣܐ‎', 'ܦܐܪܐ‎', 'ܙܪܥܐ‎', 'ܛܪܦܐ‎', 'ܫܪܫܐ‎	', 'ܩܠܦܬܐ‎', 'ܗܒܒܐ‎', 'ܓܠܐ‎',
               'ܚܒܠܐ‎', 'ܓܠܕܐ‎	', 'ܒܣܪܐ‎', 'ܕܡܐ‎', 'ܓܪܡܐ‎', 'ܕܗܢܐ‎, ܫܘܡܢܐ‎', 'ܒܝܥܬܐ‎', 'ܩܪܢܐ‎', 'ܕܘܢܒܐ‎', 'ܐܒܪܐ‎',
               'ܣܥܪܐ‎', 'ܪܝܫܐ‎', 'ܐܕܢܐ‎', 'ܥܝܢܐ‎', 'ܢܚܝܪܐ‎	', 'ܦܘܡܐ‎', 'ܫܢܐ‎, ܟܟܐ‎', 'ܠܫܢܐ‎', 'ܛܦܪܐ‎	', 'ܥܩܠܐ‎',
               'ܪܓܠܐ‎', 'ܒܘܪܟܐ‎', 'ܐܝܕܐ‎', 'ܟܢܦܐ‎	', 'ܒܛܢܐ‎, ܟܪܣܐ‎	', 'ܡܥܝܐ‎, ܓܘܐ‎', 'ܨܘܪܐ‎, ܩܕܠܐ‎',
               'ܚܨܐ‎, ܒܣܬܪܐ‎', 'ܚܕܝܐ‎', 'ܠܒܐ‎', 'ܟܒܕܐ‎', 'ܫܬܐ‎', 'ܐܟܠ‎', 'ܢܟܬ‎', 'ܡܨ‎	', 'ܪܩ‎', 'ܓܥܛ‎', 'ܢܦܚ‎',
               'ܢܦܫ‎, ܢܫܡ‎', 'ܓܚܟ‎	', 'ܚܙܐ‎', 'ܫܡܥ‎', 'ܝܕܥ‎', 'ܚܫܒ‎', 'ܡܚ‎, ܣܩ‎', 'ܕܚܠ‎, ܟܘܪ‎', 'ܕܡܟ‎', 'ܚܝܐ‎	',
               'ܡܝܬ‎', 'ܩܛܠ‎', 'ܟܬܫ‎', 'ܨܝܕ‎	', 'ܡܚܐ‎, ܢܩܫ‎', 'ܓܕܡ‎, ܩܛܥ‎', 'ܫܪܩ‎, ܦܕܥ‎, ܦܪܬ‎', 'ܕܓܫ‎', 'ܚܟ‎, ܣܪܛ‎',
               'ܚܦܪ‎', 'ܣܚܐ‎', 'ܦܪܚ‎	', 'ܗܠܟ‎	', 'ܐܬܐ‎	', 'ܫܟܒ‎, ܡܟ‎', 'ܝܬܒ‎', 'ܬܪܨ‎', 'ܦܢܐ‎, ܥܛܦ‎	',
               'ܢܦܠ‎', 'ܝܗܒ‎, ܢܬܠ‎', 'ܐܚܕ‎', 'ܩܡܛ‎, ܥܨܪ‎', 'ܫܦ‎, ܚܟ‎', 'ܚܠܠ‎, ܦܝܥ‎', 'ܟܦܪ‎', 'ܓܪܫ‎', 'ܙܥܦ‎	', 'ܪܡܐ‎',
               'ܐܣܪ‎, ܩܛܪ‎', 'ܚܝܛ‎', 'ܡܢܐ‎', 'ܐܡܪ‎', 'ܙܡܪ‎', 'ܫܥܐ‎', 'ܛܦ‎', 'ܪܣܡ‎, ܫܚܠ‎', 'ܓܠܕ‎, ܩܪܫ‎', 'ܙܘܐ‎, ܥܒܐ‎',
               'ܫܡܫܐ‎', 'ܣܗܪܐ‎', 'ܟܘܟܒܐ‎', 'ܡܝܐ‎	', 'ܡܛܪܐ‎', 'ܢܗܪܐ‎', 'ܝܡܬܐ‎', 'ܝܡܐ‎', 'ܡܠܚܐ‎	',
               'ܟܐܦܐ‎, ܐܒܢܐ‎, ܫܘܥܐ‎', 'ܚܠܐ‎', 'ܐܒܩܐ‎, ܕܩܬܐ‎', 'ܐܪܥܐ‎', 'ܥܢܢܐ‎, ܥܝܡܐ‎, ܥܝܒܐ‎', 'ܥܪܦܠܐ‎	', 'ܫܡܝܐ‎',
               'ܪܘܚܐ‎	', 'ܬܠܓܐ‎', 'ܓܠܝܕܐ‎', 'ܬܢܢܐ‎	', 'ܢܘܪܐ‎, ܐܫܬܐ‎', 'ܩܛܡܐ‎	', 'ܝܩܕ‎', 'ܐܘܪܚܐ‎', 'ܛܘܪܐ‎',
               'ܣܘܡܩܐ‎', 'ܝܘܪܩܐ‎', 'ܫܥܘܬܐ‎', 'ܚܘܪܐ‎', 'ܐܘܟܡܐ‎	', 'ܠܠܝܐ‎	', 'ܝܘܡܐ‎	', 'ܫܢܬܐ‎', 'ܫܚܝܢܐ‎',
               'ܩܪܝܪܐ‎', 'ܡܠܝܐ‎', 'ܚܕܬܐ‎', 'ܥܬܝܩܐ‎', 'ܛܒܐ‎', 'ܒܝܫܐ‎', 'ܒܩܝܩܐ‎ ܚܪܝܒܐ‎', 'ܫܘܚܬܢܐ‎', 'ܬܪܝܨܐ‎	',
               'ܚܘܕܪܢܝܐ‎', 'ܚܪܝܦܐ‎', 'ܩܗܝܐ‎', 'ܦܫܝܩܐ‎', 'ܪܛܝܒܐ‎, ܬܠܝܠܐ‎', 'ܝܒܝܫܐ‎', 'ܬܪܝܨܐ‎	', 'ܩܪܝܒܐ‎', 'ܪܚܝܩܐ‎',
               'ܝܡܝܢܐ‎', 'ܣܡܠܐ‎', 'ܒ-‎, ܠܘܬ‎', 'ܥܡ‎', 'ܐܢ‎', '-ܡܛܠ ܕ‎, ܒܥܠܬ‎', 'ܫܡܐ‎']

swadesh_ar = ["أنا", "أنت‎, أنتِ‎", "هو‎,هي", "نحن", "أنتم‎,‎ أنتن‎,‎ أنتما‎", "هم‎,‎ هن‎,‎ هما", "هذا",
              "ذلك", "هنا‎", "هناك‎", "من‎", "ما‎, ماذا", "أين‎", "متى", "كيف", "لا‎,‎‎ لم‎,‎ ما‎", "كل", "كثير",
              "كم‎", "قليل‎", "آخر‎", "واحد‎", "‏اثنان‎", "ثلاثة‎", "أربعة‎", "خمسة‎", "كبير‎", "طويل‎", "رحب‎,‎ واسع",
              "سميك‎", "ثقيل‎", "صغير", "قصير", "ضيق", "رقيق‎", "‏‏امرأة‎", "رجل‎", "إنسان‎", "طفل‎", "زوجة‎", "بعل‎",
              "أم‎", "أب‎", "حيوان‎", "سمك‎", "طير‎", "كلب‎", "قملة‎", "أفعى‎, ثعبان‎", "دودة‎", "شجرة‎", "غابة‎",
              "عود‎,‎‎ حطب", "فاكهة‎", "زرع‎", "ورقة‎", "جذر‎", "قلف‎، لحاء", "زهرة‎", "عشب‎", "حبل‎", "جلد‎", "لحم‎",
              "دم‎", "عظم‎", "سمن‎", "بيض‎", "قرن‎", "ذَنَب‎", "ريشة‎", "شعر‎", "رأس‎", "أذن‎", "عين‎", "أنف‎", "فم‎",
              "سن‎", "لسان‎", "ظفر‎", "قدم‎", "ساق‎", "ركبة‎", "يد‎", "جَنَاح‎", "بطن‎", "أمعاء‎", "عنق‎", "ظهر‎",
              "صدر‎", "قلب‎", "كبد‎", "شرب‎", "أكل‎", "عض‎", "مص‎", "بصق‎", "تقيأ‎", "نفخ‎", "تنفس‎", "ضحك‎", "رأى‎",
              "سمع‎", "علم‎", "اعتقد‎", "شم‎", "خاف‎", "نام‎", "عاش‎", "مات‎", "قتل‎", "قاتل‎", "صاد‎", "ضرب‎", "قطع‎",
              "قَسَمَ‎", "طَعَنَ‎", "خدش‎", "حفر‎", "سبح‎", "طار‎", "مشى‎", "أتى‎", "استلقى‎", "جلس‎", "قام‎", "دار‎",
              "سقط‎", "أعطى‎", "أخذ‎", "عصر‎", "حف‎", "غسل‎", "محا‎", "جر‎", "دفع‎", "رمى‎", "ربط‎", "قطب‎", "أنا",
              "عد‎", "قال‎", "غنى‎", "لعب‎", "طفا‎", "سال‎", "أجلد‎", "انتفخ‎", "شمس‎", "أخضر‎", "نجم‎", "ماء‎", "مطر‎",
              "بـ‎", "في‎", "مع‎", "و‎", "إن‎ ,إذا ‎,‎ لو", "لأن‎,‎ بسبب‎", "اسم",
              ]

swadesh_uga = [ '‘l' , '‘ảḫr' , 'kl' , 'mdbḥ' , 'w' , 'mšḥ' , '‘ny' , 'qrb' , 'dr’' , 'ṣbủ' , 'š’l' , 'żr' , 'bỉšt' , '‘py' , 'š’r' , 'k2' , 'kn' , 'šmḫ' , ['ḥnn' , 'rḥm'] , 'dqn' , ['lpn' , 'qdm'], ['krs' , 'ḥmt'] , 'yd' , 'bn' , ['ảdr?' , 'rb'] , ["ṣr" ,'’p'], 'brkD' , "dm" , "ẓm" , ["’b", 'ps' ,'ś'] , ['sp' ,'mmskn', 'ṣ’'] , 'lḥm' , 'ṯbr' , 'ảḫ' , 'bny' , ['bnt' , 'bnwn'] , 'ṯr' , ['b’r' , 'šrp' , 'ḥrk' , 'ḥrr'] , 'qny' , '‘gl' , 'qr’' , 'mỉnš' , 'ybl', ['mrkbt' , 'rkb'] , ['rb','ulp'] , ['yld','mt1'], ['‘r' , 'qrt'] , ['sgr' , 'kl’' , 'ṭbq'], ['lb' , 'pš'], '’rpt' , 'pqd' ,['bw’' , '‘tw' , '‘mġy'] , ['kll D', 'tmm'] , 'qdš' , 'bšl' , 'ṯlṯ' , 'spr' , 'ḥẓr' , ['ksy' , '’mm'] , 'ḥrš' , ['qny' , 'kwn Š'] , 'ṭrtrṭ' , 'bky' , ['ks' , 'qb’t' , 'gl' ,'bk'] , 'ảlt' , ['bṣ’' , 'bt'] , ['ġlmt' , 'ẓlmt'] , 'bt' , 'ym' , 'yrd' , ['‘bd' , 'ḫlq D' , 'ršš' , 'ṣmt'] , 'mwt' , 'kry' , 'p’l' , 'klb' , ['ṯġr', 'ptḥ'] ,'ḥlm' , 'lhš' ,'', 'grš' , 'škn' , 'ủdn1' , 'ảrṣ' , 'qdm' , ['’kl' , 'lḥm'] , 'qṣ’' , ['ṯmn' , 'ṯmnt'] , ['ỉb' , 'šnủ' , 'ṣrt'] ,[ '’rb' , 'bw’'] , ['nṣb' , 'qyn' , 'rwm L' , 'rwm D'] , 'ảp' , 'prš' , 'n' , ['pn' , 'pnm'] , 'npl' , ['špḥ' , 'ủmt'] , 'rḥq' , 'šmn' ,[ 'ảb' , 'ảd'] , ['yr’', 'ṯt’'] , 'šd' , 'lḥm Gt' , 'ml’' , ['škḥ’ , ‘mẓ'] , ['dq' , 'rq'] , 'ỉšt' , 'dg' , ['ḥmš' , 'ḥmšt'] , ['bšr','šỉr'] , 'qmḥ' , ['nws' , 'ndd'] , ['‘p' , 'd’w'] , 'p’n' , ['ảrb’','ảrb‘t'], ['ḥbr' , 'r’'] , 'l' , 'pr' , 'gn' , '’sp' , 'ytn' , 'yld' , 'hlk' , ['yẓ' , 'yṣ'] , '‘ly' , '‘z' , 'ỉl' , 'ḫrṣ' , 'ṭb' , 'š’rt' , 'yd' , 'išryt' , 'šn’' , 'hw' , 'rỉš', ['ḥmr' , 'ảtn'] , 'rp’' , 'šm’' , 'lb' , 'ḏr' , ['hn' , 'p?'] , 'rm' , 'škr' , ['hlm' , 'mḫš'] , 'qdš' , 'nbt' , 'qrn' , 'kbd D' , ['ỉk', 'ỉy'] , 'ssw' , 'bt' , 'mỉt' , 'ṣd', ['ản' , 'ảnk'] , ['hm' , 'ỉm'] , 'b' , 'yrṯ' , 'brḏl' , ['kd' , 'rḥbt'] , ['ṯpt',  'dyn'] , ['gd' , 'gy'] , ['hrg' , 'ġtr2'] , 'mlk' , 'brk' , 'yd’' ,'ỉmr', ['ṣhq' , 'ẓḥq'] , 'šmảl' , ['šq' , 'ỉsd' , 'rgl'] , 'škb' , 'nš’' , ['ả' , 'ỉr'] , ['k' , 'km'] , 'ảrw' , 'ḥwy' , '‘ms' , 'ảrkt' , ['ảdn' , 'b’l'] , 'ảhb' , ['’rk', 'm’d D'] , 'mt' , ['mỉd' , 'ẓm'] ,  'mkr' , ['tk' , 'qrb'] , 'ḥlb' , ['yrḫ' , 'ḥdṯ'] , 'um' , ['hr', 'ġr'] , 'p' , 'šm' , 'ḥdṯ' , 'll' , 'tš’' , ['l' ,'ảl2'] , 'spr' , ['mnḥ' , 'mny' , 'ytnt'], 'šmn' , 'yṯn' , ['ảḥd' , 'ảḥt'] , 'ptḥ' , ['‘ny D' , 'dll D'] , 'ủ' , 'ṯn' , 'hpk' , '‘br' , 'šlm D' , 'lỉm' , ['ảdm', 'bnš'] , 'ḥrṯ' , ['dl' , 'ảbyn'] , ['ntk N' , 'nsk', 'D' , 'šdy' ,'yṣq'] ,  'yṣr' , ['khn' , 'kmr'] , 'zbl' , 'nġr' , 'ns’' , ['ṭhr' , 'brr' , 'ỉb'] , ['šyt' , 'skn' ,'’db'] ,['mṭr','gšm'] ,['il' , 'kr'] , ['ḥmr','ỉdm?'] , 'ḫss' ,['D', 'hbṭ G','mḥy'] ,'ṯb' ,'rkb' ,'ymn', 'ṣdq' , 'nhr' , ['mrdmt' , 'ntb'] , 'gg' , 'ḥdr', 'šrš' , 'mlk' , ['dbḥ' ,'qdš Š', 'ṭbḫ'] , 'qdš' ,'rgm' , 'ym' , ['bqṯ' , 'ngṯ D'] , 'phy' , 'dr’' , 'mkr N' , 'lk' , ['šrd D’, ‘‘bd'] , ['šb’' , 'šb’t'] , 'hy' ,['r’y', 'nqd'] , ['ảny' , 'ảnt'] ,'qṣr', 'ksp' , 'ḫt’' ,['šyr', 'ḏmr' , '’ny'] , 'ảḫt' , 'yṯb', ['ṯṯ' , 'ṯṯt'] , ['ġr' , 'msg'] , 'šmm' , 'ṭbḫ' , '‘bd' , 'ảmt' , 'yšn' , ['ṣỉn' , 'š' , 'ḫprt'] , 'ṣgr' , ['ảp’' , 'nḥš' , 'bṯn' , 'tnn1'] , 'glt' ,'bn' , 'npš' , ['mnt' , 'lḫšt'] , '’n' , 'qwm' , 'kbkb' , 'ảbn' , 'štk' , ['‘z'  , '’dr'] , 'špš' , ['’ḫd', 'lḥq'] , ['‘šr' , '‘šrt'] , 'ỉdk' , 'ṯm' , 'hm(t)' , 'hnd' , ['ṯlṯ' , 'ṯlṯt'] , ['kḥt' ,'ksu' , 'ṯbt'] , ['rmy' , 'yry'] , '‘lp' , ['‘sr' , 'rks'] , '’d' , 'l' , 'qbr' , 'lšn' , 'sbb' , ['ṯn' , 'ṯt'] , 'tḥt' , '‘d' ,['mq' , 'bq'],['g', 'ql'] ,[ 'nd' , 'ḏr'] ,'rḥs', ['qr' , 'ḥmt'] , ['my' , 'mh'] , ['bỉir' , 'mqr'] , 'm’rb' , ['mn' , 'mh' , 'mhy'] ,'ḥtt', ['km' , 'k2'] , ['ỉy' , 'ỉ'] , 'lbn' , 'my' , 'rḥ'  , ['yn' , 'ḫmr' , 'trṯ'] , 'hkm' , '‘rš' , '’m' ,  'ảṯt' , ['rgm' , 'hwt1'] , '‘bd' ,'‘ṣ' , 'ktb' , 'ảt' , ['ġlmt' , 'pġt' , 'mṯt'] , ['ġlm' ,'n’r' ,'kdd'] , 'šnt' ]

swadesh_phn = [ '‘l' , '‘ḥr' , 'kl' , 'mzbḥ' , 'w' , 'mšḥ' , '‘ny' , 'qrb?' , 'zr’' , 'ṣb’' , 'š’l' , 'ṣd?' , ['r’' , 'mlṣ'] , '‘py','', 'ky' , 'kn' , '‘lṣ' , 'ḥnn' , 'zqn' , ['lpn' , 'pnt'],'', '‘ṣl?','' , '‘dr?' , 'ṣpr' , ['brkG' , 'brkD'] , 'dm' , '‘ṣm' , 'gbl' , ['sp' , 'dqrt'] , 'lḥm' , 'šbr' , '‘ḥ' , 'bny' , ['bn’' , 'mbnh'] , '‘lp' , 'b’r?' , ['sḥr Part.' , 'qny?'] , '‘gl' , 'qr’' , 'mḥnt' , '‘ms' , ['‘glt' , 'mrkbt'] , ['‘dr' , 'rb' , 'b’l?'] , ['yld' , '‘l'] , ['‘r' , 'qrt'] , 'sgr K' , ['mswy’t' , 'kst'],'','' , ['bw’' , '‘ty?'] , ['kly D', 'tmm'] , ['qdš' , 'ḥnk'] , '‘py' , 'nḥšt' , 'mny' , 'ḥṣr' , 'ksy D' , 'ḥrš' , 'qny' , '‘ṭrt' , 'yll K' , ['ks' , 'qb’' , 'gln'] , ['‘lt' , 'qbt'] , 'btt’' , 'ḥšk?' , 'bt' , 'ym' , 'yrd' , ['‘bd' , '‘kr' ], 'mwt' , 'kry' , 'p’l' , 'klb' , ['dlt' , 'ptḥ'],'','' , 'grš' , 'škn' , '','‘rṣ' , 'mwṣ’' , ['‘kl' , 'lḥm?'] , 'qṣt' , 'šmn' , '‘b' , 'drk' , ['nṣb' , 'ṭn’'] , '‘p' , ['rḥb K' , 'rwḥ K'] , '’n' , ['pn' , 'pnm'] , 'npl?' , 'špḥ' , 'rḥq' , ['šmn' , 'ḥlb'] , '‘b' , 'št’' , 'šd' , 'lḥm N' , 'ml’' , 'pwq K' , 'dqt' , '‘š','' , ['ḥmš' , 'ḥmšt'] , ['bšr' , 'š’r'] , 'qmḥ' , 'brḥ' , '‘wp?' , 'p’m' , ['‘rb’' , '’rb‘t'] , 'ḥbr' , 'mn' , ['pr' , '‘bb?'] , 'gnt' , '’sp N' , 'ntn' , 'yld G' , 'hlk' , 'yṣ’' , '‘ly' , '‘z' , '’l' , 'ḥrṣ' , 'ṭb' , 'š’rt' , 'yd' , '’šr' ,'', 'h’' , 'r’š','', 'rp’' , 'šm’' , 'lb' , '‘zr' , 'ph' , 'rm' , 'škr' , 'hlm' , 'qdš' , 'npt' , 'qrn' , 'kbd D','' , 'ss' , 'bt' , 'm’t' , 'ṣd', ['’n' , '‘nk'] , '’m' , 'b' , 'nḥl' , 'brzl?' , 'kd' , 'špṭ' , 'gd’' ,'', 'mlk' , 'brk2?' , 'yd’' , '’mr','','','' , ['škb' , 'npl?'] , 'nš’' , '‘r' , ['k' , 'km'] , '’rw' , 'ḥwy' , '‘ms' , '‘rk' , ['’dn' , 'b’l'] , ['ḥbb K' , 'rḥm K'] , '‘rk K' , 'grb' , 'rb' , ['mkr' , 'sḥr'] , ['tkt' , 'gw'] , 'ḥlb' ,'ḥdš' , '‘m' , 'hr' , 'py' , 'šm' , 'ḥdš' , 'll' , 'tš’' , 'bl' , 'mspr' , 'mnḥt' , 'šmn' , 'rš’t' , ['’ḥd' , '’ḥt'] , 'ptḥ' , '‘ny' , '’w' , 'zr' , 'hpk Gt' , '‘br' , 'šlm' , '‘m' , ['’dm' , 'qn’m'],'' , 'dl' , ['ysk N' , 'nsk'] , 'yṣr' , ['khn' , 'kmr'] , ['zbl' , 'šr'] , ['nṣr' , 'šmr'] , 'ns’' , ['ṭhr' , 'ṭr' , 'zky'] , ['šym' , 'šyt'],'' , ['‘yl' , 'ybl'] , '‘dm5?' , 'zkr' , 'skr' , ['mḥy' , 'swr K'],'' , 'rkb' ,'', ['ṣdq' , 'yšr'],'' , 'drk' , 'gg' , ['ḥdr' , 'sgrt'] , 'šrš' , ['mlk' , 'mšl'] , 'zbḥ' , ['qdš' , 'mqdš'] , ['‘mr' , 'dbr D'] , 'ym' , 'bqš D' , ['ḥzy' , 'r’y?'] , 'zr’' , 'mkr' , 'šlḥ' , ['šrt D ‘bd' , 'šmš D'] , ['šb’' , 'šb’t'] , 'h’' , 'r’' , 'škt?','' , 'ksp','' , 'šyr', '‘ht' , ['yšb G', 'K'] , ['šš' , 'ššt'] , '‘rt' , 'šmym' , 'nks' , '‘bd' , '’mt' , 'lyn Gt' , 'ṣ’n' , 's’r','','' , 'bn' , 'npš' , ['ksp' , 'lḥšt' , 'mnt'] , '’n' , 'qwm' , 'kkb' , '‘bn' , 'šbt K' , ['‘zz' , '‘ṣm'] , 'šmš' , ['‘ḥz' , 'lqh' , 'tmk'] , ['‘šr' , '‘šrt'] , '‘z' , 'šm' , 'hmt' , 'z' , 'zn' , ['šlš' , 'šlšt'] , ['ks’t' ,'yšb' , 'mšb'],'' , '‘lp' , '‘sr' , '’t' , 'l' , 'qbr' , 'lšn' , 'sbb' , 'šnym' , ['tḥt' , 'mṭ'] , '‘d' , 'ql' , 'ndr' , ['gdr' , 'hgr' , 'qr'],'' , 'mym' , 'b’r' , ['m’rb' , 'mb’' ], ['m' , 'mh'],'' , 'km2' , '‘y' , 'lbn' , 'my' ,'', ['yn' , 'ḥmr' , 'trš'],'' , '‘rš' , ['dl' , '’t'] , '’št' , 'dbr' , '‘bd' , '‘ṣ' , 'ktb' , '’t' , ['‘lmt' , '‘lm'] ,'n’r?' , 'št' ]

swadesh_old_norse = ["ek", "þú", "hann", "vér", "þér", "þeir", "sjá, þessi", "sá", "hér", "þar", "hvar", "hvat", "hvar", "hvenær", "hvé", "eigi", "allr", "margr", "nǫkkurr", "fár", "annarr", "einn", "tveir", "þrír", "fjórir", "fimm", "stórr", "langr", "breiðr", "þykkr", "þungr", "lítill", "stuttr", "mjór", "þunnr", "kona", "karl", "maðr", "barn", "kona", "bóndi", 'móðir', "faðir", "dýrr", "fiskr", "fugl", "hundr", "lús", "snókr", "ormr", "tré", "skógr", "stafr", "ávǫxtr", "fræ", "lauf", "rót", "bǫrkr", "blóm", "gras", "reip", "húð", "kjǫt", "blóð", "bein", "fita", "egg", "horn", "hali", "fjǫðr", "hár", "hǫfuð", "eyra", "auga", "nef", "munnr", "tǫnn", "tunga", "nagl", "fótr", "leggr", "kné", "hǫnd", "vængr", "magi", "iinyfli", "hals" , "bak", "brjóst", "hjarta", "lifr", "drekka", "eta", "bíta", "súga", "spýta", ", hrækja", None, "blása", "anda", "hlæja", "sjá", "heyra", "vita", "þýkkja", "þefa", "ugga", "sofa", "lifa", "deyja", "drepa", "hals", "bak", "berja", "skera", "kljúfa""stinga", "klóra", "grafa", "synda", "fljúga", "ganga", "koma", "liggja", "sitja", "standa", "snúa", "falla", "gefa", "halda", "kreista", "gnúa","þvá", "þurka", "draga", "ýta", "kasta", "kasta", "binda", "sauma", "telja", "segja", "syngja", "leika", "flóta", "streyma", "frjósa", "þrútna", "sól", "tungl", "stjarna", "vatn", "regn", "á", "vatn", "hav", "salt", "steinn", "sandr", "ryk", "jörð", "ský", "þoka", "himinn", "vindr", "snjór", "íss", "reykr", "ild", "eldr", "aska", "brenna", "vegr", "fjall", "rauðr", "grœnn", "gulr", "hvítr", "svartr", "nótt", "dagr", "ár", "heitr", "kaldr", "fullr", "nýr", "gamall", "góðr", "illr", "rottin", "skitinn", "beinn", "kringlóttr", "beittr", None, "sleipr", "blautr", "	þurr", "réttr", "nálægr", "langr", "hœgr", "vinstri", "hjá","í", "með", "ok", "ef", "því at", "nafn"]  # pylint: disable=line-too-long

swadesh_cop = ['ⲁⲛⲟⲕ', 'ⲛⲧⲟⲕ, ⲛⲧⲟ', 'ⲛⲧⲟϥ, ⲛⲧⲟⲥ', 'ⲁⲛⲟⲛ', 'ⲛⲧⲟⲧⲛ', 'ⲛⲧⲟⲩ', '-ⲉⲓ', 'ⲡⲓ-, ϯ-, ⲛⲓ-', 'ⲡⲉⲓⲙⲁ',
              'ⲙⲙⲁⲩ', 'ⲛⲓⲙ', 'ⲁϣ', 'ⲧⲱⲛ', 'ⲧⲛⲛⲁⲩ', 'ⲡⲱⲥ', 'ⲛ, ⲁⲛ', 'ⲧⲏⲣ', 'ⲟϣ', 'ϩⲟⲉⲓⲛⲉ', ['ⲕⲟⲩⲓ', 'ϣⲏⲙ'],
              'ⲕⲉ', 'ⲟⲩⲁ', 'ⲥⲛⲁⲩ', 'ϣⲟⲙⲧ', 'ϥⲧⲟⲩ', 'ϯⲟⲩ', 'ⲛⲟϭ', 'ϣⲓⲁⲓ', ['ⲟⲩⲟⲥⲧⲛ', 'ⲟⲩⲱϣⲥ'],
              'ⲟⲩⲙⲟⲧ', 'ϩⲣⲟϣ', ['ⲕⲟⲩⲓ', 'ϣⲏⲙ', 'ϣⲓⲣⲉ'], 'ϣⲏⲙ', 'ϫⲏⲧ', 'ⲡⲁⲕⲉ', 'ⲥϩⲓⲙⲉ', 'ϩⲟⲟⲩⲧ', 'ⲣⲱⲙⲉ',
              'ϣⲏⲣⲉ', 'ⲥϩⲓⲙⲉ', 'ϩⲁⲓ', 'ⲙⲁⲁⲩ', 'ⲉⲓⲱⲧ', 'ⲧⲃⲛⲏ', 'ⲧⲃⲧ', 'ϩⲁⲗⲏⲧ', 'ⲟⲩϩⲟⲣ', 'ϩⲗⲱⲙ', 'ϩⲟϥ', 'ϥⲛⲧg',
              'ϣⲏⲛ', 'ⲉⲓⲁϩ ϣⲏⲛ', 'ⲟⲩⲁϩ', 'ⲟⲩⲧⲁϩ', 'ϫⲣⲟϫ', 'ϭⲱⲱⲃⲉ', 'ⲛⲟⲩⲛⲉ', 'ⲕⲟⲩⲕⲉ', 'ϩⲣⲏⲣⲉ', 'ⲥⲓⲙ', 'ⲛⲟⲩϩ',
              'ϣⲁⲁⲣ', 'ⲁϥ', 'ⲥⲛⲟϥ', 'ⲕⲁⲥ', 'ⲱⲧ', 'ⲥⲟⲟⲩϩⲉ', 'ⲥⲃⲟⲕ', 'ⲥⲁⲧ', 'ⲙⲏϩⲉ', 'ϥⲱ', 'ⲁⲡⲉ', 'ⲙⲁⲁϫⲉ',
              'ⲉⲓⲁ', 'ϣⲁ', 'ⲣⲟ', ['ϣⲟⲗ', 'ⲛⲁϫϩⲉ'], 'ⲗⲁⲥ', 'ⲉⲓⲃ', ['ⲟⲩⲉⲣⲏⲧⲉ', 'ⲣⲁⲧ'], 'ⲣⲁⲧ', 'ⲕⲗⲗⲉ', 'ϭⲓϫ, ',
              'ⲧⲛϩ', 'ϩⲏ(ⲧ)', ['ⲙⲁϩⲧ', 'ⲙⲉϩⲧⲟ'], 'ⲙⲁⲕϩ', 'ϫⲓⲥⲉ', 'ⲉⲕⲓⲃⲉ', 'ϩⲏⲧ', 'ⲟⲩⲫⲁϫⲓ', 'ⲥⲱ', 'ⲟⲩⲱⲙ',
              'ⲗⲱⲕⲥ', 'ⲥⲱⲛⲕ', 'ⲛⲉϫⲧⲁϥ', 'ⲕⲁⲃⲟⲗ', 'ⲛⲓϥⲉ', 'ⲥⲉⲕⲧⲏⲩ', 'ⲥⲱⲃⲉ', 'ⲛⲁⲩ', 'ⲥⲱⲧⲙ', 'ⲉⲓⲙⲉ', 'ⲙⲉⲉⲩⲉ', 'ϣⲱⲗⲙ',
              'ⲣϩⲟⲧⲉ', 'ϩⲓⲛⲏⲃ', 'ⲟⲟⲩ-', 'ⲙⲟⲩ', 'ⲙⲟⲩⲟⲩⲧ', 'ⲙⲓϣⲉ', 'ⲙⲉⲧϫⲉⲣⲏϫ', 'ϯ', 'ϣⲟⲧϣⲧ', 'ⲡⲱϩ',
              'ⲗⲟⲅⲭⲓⲍⲉ', 'ϩⲱϩ', 'ϣⲓⲕⲉ', 'ⲛⲏⲏⲃⲉ', 'ϩⲁⲗⲁⲓ', 'ⲙⲟⲟϣⲉ', 'ⲉⲓ', 'ⲛⲕⲟⲧⲕ', 'ϩⲙⲟⲟⲥ',
              'ⲱϩⲉ', ['ⲡⲱⲱⲛⲉ', 'ⲕⲧⲟ'], 'ϩⲉ', 'ϯ', 'ⲁⲙⲁϩⲧⲉ', '', 'ⲗⲟϫⲗϫ', ['ⲣⲱϩⲉ', 'ⲉⲓⲱ'], 'ϥⲱⲧⲉ', 'ⲥⲟⲕⲥⲉⲕ',
              'ϭⲱⲟⲩ', 'ⲛⲟⲩϫⲉ', 'ⲙⲟⲩⲣ', ['ⲧⲱⲣⲡ', 'ⲱⲧϩ', 'ϫⲱⲗⲕ'], 'ⲱⲡ', ['ϣⲁϫⲉ', 'ϫⲱ'], ['ϭⲛϭⲛ', 'ϩⲱⲥ'], 'ⲥⲱⲃⲉ',
              ['ⲛⲏⲏⲃⲉ', 'ϩⲗⲟⲉⲓⲗⲉ'], 'ϣⲱⲗ', 'ⲱϭⲣ', 'ⲛⲟⲩϥⲧ', 'ⲣⲏ', 'ⲟⲟϩ', 'ⲥⲓⲟⲩ', 'ⲙⲟⲟⲩ', 'ϩⲱⲟⲩ',
              'ⲉⲓⲉⲣⲟ', ['ⲑⲁⲗⲁⲥⲥⲁ', 'ⲗⲓⲙⲛⲏ'], 'ⲉⲓⲟⲙ', ['ⲙⲗϩ', 'ϩⲙⲟⲩ'], 'ⲱⲛⲉ', 'ϣⲱ', 'ϣⲟⲉⲓϣ',
              ['ⲉⲓⲧⲛ', 'ⲕⲁϩ', 'ⲧⲟ'], ['ⲕⲗⲟⲟⲗⲉ', 'ϭⲏⲡⲉ'], 'ⲧⲙⲧⲙ', ['ⲡⲉ', 'ⲡⲏⲩⲉ'], 'ⲧⲏⲩ', 'ⲭⲓⲱⲛ', 'ⲕⲣⲩⲥⲧⲁⲗⲗⲟⲥ',
              ['ⲕⲣⲙⲧⲥ', 'ⲧⲙⲧⲙ'], ['ⲕⲱϩⲧ', 'ⲕⲣⲱⲛ'], 'ⲕⲣⲙⲉⲥ', 'ⲣⲱⲕϩ', ['ϩⲓⲏ', 'ϩⲓⲟⲟⲩⲉ'], 'ⲧⲟⲟⲩ', 'ⲧⲱⲣϣ', 'ⲟⲩⲟⲧ', '',
              'ⲟⲩⲟⲃϣ', 'ⲕⲏⲙ', 'ⲟⲩϣⲏ', 'ϩⲟⲟⲩ', ['ⲣⲟⲙⲡⲉ', 'ⲣⲙⲡⲟⲟⲩⲉ'], 'ⲑⲉⲣⲙⲟⲛ', 'ⲟⲣϣ', 'ⲙⲏϩ', 'ⲃⲣⲣⲉ',
              'ⲁⲥ', 'ⲛⲟⲩϥⲉ', ['ϩⲟⲟⲩ', 'ⲃⲱⲱⲛ'], 'ⲗⲱⲙⲥ', 'ϫⲱϩⲙ', 'ⲥⲟⲩⲧⲱⲙ', '', 'ⲧⲱⲙ', '', 'ⲗⲉⲕⲗⲱⲕ',
              'ϩⲟⲣⲡ', 'ⲃⲟⲥⲧ', 'ⲥⲟⲟϩⲉ', 'ϩⲏⲛ', 'ⲟⲩⲉ', 'ⲟⲩⲛⲁⲙ', 'ϩⲃⲟⲩⲣ',
              '', '', 'ⲙⲛ', 'ⲁⲩⲱ', '', 'ⲉⲣϣⲁⲛ', 'ⲣⲁⲛ']

class Swadesh():
    def __init__(self, language):
        self.language = language

    def words(self):
        if self.language == 'la':
            return swadesh_la
        elif self.language == 'gr':
            return swadesh_gr
        elif self.language == 'sa':
            return swadesh_sa
        elif self.language == 'txb':
            return swadesh_txb
        elif self.language == 'pt_old':
            return swadesh_pt_old
        elif self.language == 'eng_old':
            return swadesh_eng_old
        elif self.language == 'old_norse':
            return swadesh_old_norse
        elif self.language == 'syc':
            return swadesh_syc
        elif self.language == 'hi':
            return swadesh_hi
        elif self.language == 'ar':
            return swadesh_ar
        elif self.language == 'cop':
            return swadesh_cop
