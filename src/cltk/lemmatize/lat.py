"""Module for lemmatizing Latin
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License. See LICENSE."

import os
import re
from typing import List

from cltk.lemmatize.backoff import (
    DefaultLemmatizer,
    DictLemmatizer,
    IdentityLemmatizer,
    RegexpLemmatizer,
    UnigramLemmatizer,
)
from cltk.utils import CLTK_DATA_DIR
from cltk.utils.file_operations import open_pickle

latin_sub_patterns = [
    ("(bil)(is|i|em|e|es|ium|ibus)$", r"\1is"),
    ("(.)tat(is|i|em|e|es|um|ibus)$", r"\1tas"),
    ("(.)tut(is|i|em|e|es|um|ibus)$", r"\1tus"),
    ("(.)ab(o|is|it|imus|itis|unt)$", r"\1o"),
    ("(.)(s|t)or(is|i|em|e|es|um|ibus)$", r"\1\2or"),
    ("(.)tric(is|i|em|e|es|um|ibus)$", r"\1trix"),
    ("(.)ion(is|i|em|e|es|um|ibus)$", r"\1io"),
    ("(.)tudin(is|i|em|e|es|um|ibus)$", r"\1tudo"),
    ("(.)din(is|i|em|e|es|um|ibus)$", r"\1do"),
    ("(.)gin(is|i|em|e|es|um|ibus)$", r"\1go"),
    ("(al)(is|i|em|e|es|um|ibus)$", r"\1"),
    ("(ar)(is|i|em|e|es|um|ibus)$", r"\1is"),
    ("(el)(is|i|em|e|es|um|ibus)$", r"\1is"),
    ("(sil)(is|i|em|e|es|um|ibus)$", r"\1is"),
    ("(til)(is|i|em|e|es|um|ibus)$", r"\1is"),
    ("(il)(is|i|em|e|es|um|ibus)$", r"\1is"),
    ("(ul)(is|i|em|e|es|um|ibus)$", r"\1is"),
    ("(.)antissim(us|a|um|i|ae|am|o|orum|arum|is|os|as)$", r"\1o"),
]


latin_pps = {
    "abluo": [3, "ablu", "abluere", "ablu", "ablut"],
    "accedo": [3, "acced", "accedere", "access", "access"],
    "accendo": [3, "accend", "accendere", "accend", "accens"],
    "accidit": [3, "accidi", "accidere", "accidi", None],
    "accipio": [3, "accipi", "accipere", "accep", "accept"],
    "adiuto": [1, "adiut", "adiutare", "adiutau", "adiutat"],
    "aduenio": [4, "adueni", "aduenire", "aduen", "aduent"],
    "aedifico": [1, "aedific", "aedificare", "aedificau", "aedificat"],
    "ago": [3, "ag", "agere", "eg", "act"],
    "ambulo": [1, "ambul", "ambulare", "ambulau", "ambulat"],
    "amo": [1, "am", "amare", "amau", "amat"],
    "aperio": [4, "aperi", "aperire", "aperu", "apert"],
    "appello": [1, "appell", "appellare", "appellau", "appellat"],
    "arceo": [3, "arce", "arcere", "arcu", None],
    "ardeo": [2, "arde", "ardere", "ars", "ars"],
    "areo": [3, "are", "arere", None, None],
    "ascendo": [3, "ascend", "ascendere", "ascend", "ascens"],
    "audio": [4, "audi", "audire", "audiu", "audit"],
    "augeo": [2, "auge", "augere", "aux", "auct"],
    "bibo": [3, "bib", "bibere", "bib", None],
    "cado": [3, "cad", "cadere", "cecid", "cas"],
    "caedo": [3, "caed", "caedere", "cecid", "caes"],
    "candeo": [3, "cande", "candere", "candu", None],
    "cano": [3, "can", "canere", "cecin", "cant"],
    "capio": [3, "capi", "capere", "cep", "capt"],
    "caueo": [3, "caue", "cauere", "cau", "caut"],
    "cedo": [3, "ced", "cedere", "cess", "cess"],
    "ceno": [1, "cen", "cenare", "cenau", "cenat"],
    "cieo": [3, "cie", "ciere", "ciu", "cit"],
    "circumuenio": [4, "circumueni", "circumuenire", "circumuen", "circumuent"],
    "clamo": [1, "clam", "clamare", "clamau", "clamat"],
    "claudo": [3, "claud", "claudere", "claus", "claus"],
    "cognosco": [3, "cognosc", "cognoscere", "cognou", "cognit"],
    "colligo": [3, "collig", "colligere", "colleg", "collect"],
    "colo": [3, "col", "colere", "colu", "cult"],
    "comedo": [3, "comed", "comedere", "comed", "comes"],
    "compello": [1, "compell", "compellare", "compellau", "compellat"],
    "condo": [3, "cond", "condere", "condid", "condit"],
    "conficio": [3, "confici", "conficere", "confec", "confect"],
    "confido": [3, "confid", "confidere", None, "confis"],
    "conicio": [3, "conici", "conicere", "coniec", "coniect"],
    "consequor": [3, "consequ", "consequi", "consect", None],
    "conspicio": [3, "conspici", "conspicere", "conspex", "conspect"],
    "constituo": [3, "constitu", "constituere", "constitu", "constitut"],
    "contendo": [3, "contend", "contendere", "contend", "content"],
    "conuenio": [4, "conueni", "conuenire", "conuen", "conuent"],
    "conuoco": [1, "conuoc", "conuocare", "conuocau", "conuocat"],
    "credo": [3, "cred", "credere", "credid", "credit"],
    "cresco": [3, "cresc", "crescere", "creu", "cret"],
    "cupio": [4, "cupi", "cupire", "cupiu", "cupit"],
    "curo": [1, "cur", "curare", "curau", "curat"],
    "curro": [3, "curr", "currere", "cucurr", "curs"],
    "custodio": [4, "custodi", "custodire", "custodiu", "custodit"],
    "debeo": [3, "debe", "debere", "debu", "debit"],
    "dedo": [3, "ded", "dedere", "dedid", "dedit"],
    "defendo": [3, "defend", "defendere", "defend", "defens"],
    "depono": [3, "depon", "deponere", "deposu", "deposit"],
    "desidero": [1, "desider", "desiderare", "desiderau", "desiderat"],
    "despero": [1, "desper", "desperare", "desperau", "desperat"],
    "dico": [3, "dic", "dicere", "dix", "dict"],
    "dicto": [1, "dict", "dictare", "dictau", "dictat"],
    "dimitto": [3, "dimitt", "dimittere", "dimis", "dimiss"],
    "discedo": [3, "disced", "discedere", "discess", "discess"],
    "disco": [3, "disc", "discere", "didic", None],
    "do": [1, "d", "dare", "ded", "dat"],
    "doceo": [2, "doce", "docere", "docu", "doct"],
    "dormio": [4, "dormi", "dormire", "dormiu", "dormit"],
    "duco": [3, "duc", "ducere", "dux", "duct"],
    "efficio": [3, "effici", "efficere", "effec", "effect"],
    "emo": [3, "em", "emere", "em", "empt"],
    "erro": [1, "err", "errare", "errau", "errat"],
    "euado": [3, "euad", "euadere", "euas", "euas"],
    "euigilo": [1, "euigil", "euigilare", "euigilau", "euigilat"],
    "excito": [1, "excit", "excitare", "excitau", "excitat"],
    "exerceo": [3, "exerce", "exercere", "exercu", "exercit"],
    "expugno": [1, "expugn", "expugnare", "expugnau", "expugnat"],
    "exspecto": [1, "exspect", "exspectare", "exspectau", "exspectat"],
    "exstinguo": [3, "exstingu", "exstinguere", "exstingu", "exstinct"],
    "facio": [3, "faci", "facere", "fec", "fact"],
    "faueo": [3, "faue", "fauere", "fau", "faut"],
    "festino": [1, "festin", "festinare", "festinau", "festinat"],
    "fido": [3, "fid", "fidere", None, "fis"],
    "fio": [3, "fi", "fieri", None, "fact"],
    "fleo": [2, "fle", "flere", "fleu", "flet"],
    "frango": [3, "frang", "frangere", "freg", "fract"],
    "fugio": [3, "fugi", "fugere", "fug", "fugit"],
    "gaudeo": [3, "gaude", "gaudere", None, "gauis"],
    "gero": [3, "ger", "gerere", "gess", "gest"],
    "habeo": [2, "habe", "habere", "habu", "habit"],
    "habito": [1, "habit", "habitare", "habitau", "habitat"],
    "iaceo": [3, "iace", "iacere", "iacu", "iacit"],
    "iacio": [3, "iaci", "iacere", "iec", "iact"],
    "impero": [1, "imper", "imperare", "imperau", "imperat"],
    "incendo": [3, "incend", "incendere", "incend", "incens"],
    "induo": [3, "indu", "induere", "indu", "indut"],
    "intellego": [3, "intelleg", "intellegere", "intellex", "intellect"],
    "intro": [1, "intr", "intrare", "intrau", "intrat"],
    "inuenio": [4, "inueni", "inuenire", "inuen", "inuent"],
    "inuideo": [3, "inuide", "inuidere", "inuid", "inuisu"],
    "iubeo": [2, "iube", "iubere", "iuss", "iuss"],
    "iuuo": [1, "iuu", "iuuare", "iuuau", "iuuat"],
    "laboro": [1, "labor", "laborare", "laborau", "laborat"],
    "laudo": [1, "laud", "laudare", "laudau", "laudat"],
    "lauo": [1, "lau", "lauare", "lauau", "laut"],
    "lego": [3, "leg", "legere", "leg", "lect"],
    "libero": [1, "liber", "liberare", "liberau", "liberat"],
    "linquo": [2, "linqu", "linquere", "liqu", None],
    "luco": [3, "luc", "lucere", "lux", None],
    "ludo": [3, "lud", "ludere", "lus", "lus"],
    "luo": [3, "lu", "luere", "lu", None],
    "maneo": [2, "mane", "manere", "mans", "mans"],
    "mitto": [3, "mitt", "mittere", "mis", "miss"],
    "moneo": [3, "mone", "monere", "monu", "monit"],
    "narro": [1, "narr", "narrare", "narrau", "narrat"],
    "nauigo": [1, "nauig", "nauigare", "nauigau", "nauigat"],
    "noceo": [3, "noce", "nocere", "nocu", "nocit"],
    "numero": [1, "numer", "numerare", "numerau", "numerat"],
    "occido": [3, "occid", "occidere", "occid", "occis"],
    "occulo": [3, "occul", "occulere", "occulu", "occult"],
    "occurro": [3, "occurr", "occurrere", "occurr", "occurs"],
    "offendo": [3, "offend", "offendere", "offend", "offens"],
    "oppugno": [1, "oppugn", "oppugnare", "oppugnau", "oppugnat"],
    "opprimo": [3, "opprim", "opprimere", "oppress", "oppress"],
    "oro": [1, "or", "orare", "orau", "orat"],
    "ostendo": [3, "ostend", "ostendere", "ostend", "ostent"],
    "pareo": [3, "pare", "parere", "paru", "parit"],
    "paro": [1, "par", "parare", "parau", "parat"],
    "pello": [3, "pell", "pellere", "pepul", "puls"],
    "perdo": [3, "perd", "perdere", "perdid", "perdit"],
    "perficio": [3, "perfici", "perficere", "perfec", "perfect"],
    "peruenio": [4, "perueni", "peruenire", "peruen", "peruent"],
    "peto": [3, "pet", "petere", "petiu", "petit"],
    "placeo": [3, "place", "placere", "placu", "placit"],
    "plico": [1, "plic", "plicare", "plicau", "plicat"],
    "pono": [3, "pon", "ponere", "posu", "posit"],
    "portendo": [3, "portend", "portendere", "portent", "portent"],
    "porto": [1, "port", "portare", "portau", "portat"],
    "posco": [3, "posc", "poscere", "poposc", None],
    "praetereo": [4, "praetere", "praeterire", "praeteri", "praeterit"],
    "procedo": [3, "proced", "procedere", "process", "process"],
    "promitto": [3, "promitt", "promittere", "promis", "promiss"],
    "prouideo": [3, "prouide", "prouidere", "prouis", "prouis"],
    "pugno": [1, "pugn", "pugnare", "pugnau", "pugnat"],
    "pungo": [3, "pung", "pungere", "pupung", "punct"],
    "quaero": [3, "quaer", "quaerere", "quaesiu", "quaesit"],
    "quiesco": [3, "quiesc", "quiescere", "quieu", "quiet"],
    "rapio": [3, "rapi", "rapere", "rapu", "rapt"],
    "recito": [1, "recit", "recitare", "recitau", "recitat"],
    "reddo": [3, "redd", "reddere", "reddid", "reddit"],
    "redeo": [4, "rede", "redire", "redi", "redit"],
    "rego": [3, "reg", "regere", "rex", "rect"],
    "relinquo": [3, "relinqu", "relinquere", "reliqu", "relict"],
    "repello": [3, "repell", "repellere", "reppul", "repuls"],
    "resisto": [3, "resist", "resistere", "restit", "restit"],
    "respondeo": [2, "responde", "respondere", "respond", "respons"],
    "retineo": [3, "retine", "retinere", "retinu", "retent"],
    "reuerto": [3, "reuert", "reuertere", "reuert", "reuers"],
    "rideo": [2, "ride", "ridere", "ris", "ris"],
    "rogo": [1, "rog", "rogare", "rogau", "rogat"],
    "rumpo": [3, "rump", "rumpere", "rup", "rupt"],
    "ruo": [3, "ru", "ruere", "ru", "rut"],
    "saluto": [1, "salut", "salutare", "salutau", "salutat"],
    "scando": [3, "scand", "scandere", "scand", "scans"],
    "scribo": [3, "scrib", "scribere", "scrips", "script"],
    "sedeo": [2, "sede", "sedere", "sed", "sess"],
    "sequor": [3, "sequ", "sequi", "sect", None],
    "seruio": [4, "serui", "seruire", "serui", "seruit"],
    "seruo": [1, "seru", "seruare", "seruau", "seruat"],
    "significo": [1, "signific", "significare", "significau", "significat"],
    "sino": [3, "sin", "sinere", "siu", "sit"],
    "sisto": [3, "sist", "sistere", "stit", "stat"],
    "soluo": [3, "solu", "soluere", "solu", "solut"],
    "specio": [3, "speci", "specere", "spex", "spect"],
    "specto": [1, "spect", "spectare", "spectau", "spectat"],
    "spero": [1, "sper", "sperare", "sperau", "sperat"],
    "spondeo": [3, "sponde", "spondere", "spopond", "spons"],
    "statuo": [3, "statu", "statuere", "statu", "statut"],
    "sto": [1, "st", "stare", "stet", "stat"],
    "studeo": [3, "stude", "studere", "studu", None],
    "suadeo": [3, "suade", "suadere", "suas", "suas"],
    "succurro": [3, "succurr", "succurrere", "succurr", "succurs"],
    "sumo": [3, "sum", "sumere", "sumps", "sumpt"],
    "supero": [1, "super", "superare", "superau", "superat"],
    "surgo": [3, "surg", "surgere", "surrex", "surrect"],
    "taceo": [3, "tace", "tacere", "tacu", "tacit"],
    "tempto": [1, "tempt", "temptare", "temptau", "temptat"],
    "tendo": [3, "tend", "tendere", "tetend", "tent"],
    "teneo": [2, "tene", "tenere", "tenu", "tent"],
    "tollo": [3, "toll", "tollere", "sustul", "sublat"],
    "trado": [3, "trad", "tradere", "tradid", "tradit"],
    "transeo": [4, "transe", "transire", "transi", "transit"],
    "utor": [3, "ut", "uti", "us", None],
    "uado": [3, "uad", "uadere", "uas", None],
    "ueho": [3, "ueh", "uehere", "uex", "uect"],
    "uendo": [3, "uend", "uendere", "uendid", "uendit"],
    "uenio": [4, "ueni", "uenire", "uen", "uent"],
    "uerso": [1, "uers", "uersare", "uersau", "uersat"],
    "uersor": [1, "uerso", "uersari", "uersatus su", None],
    "uerto": [3, "uert", "uertere", "uert", "uers"],
    "uexo": [1, "uex", "uexare", "uexau", "uexat"],
    "uideo": [2, "uide", "uidere", "uid", "uis"],
    "uigilo": [1, "uigil", "uigilare", "uigilau", "uigilat"],
    "uinco": [3, "uinc", "uincere", "uic", "uict"],
    "uisito": [1, "uisit", "uisitare", "uisitau", "uisitat"],
    "uiso": [3, "uis", "uisere", "uis", "uis"],
    "uiuo": [3, "uiu", "uiuere", "uix", "uict"],
    "uoco": [1, "uoc", "uocare", "uocau", "uocat"],
    "uolo": [1, "uol", "uolare", "uolau", "uolat"],
}

### Regexps for Latin verb endings; default patterns for use with PPLemmatizer
### Todo: Refactor to be more compact

pia_patterns = [
    (r"(\w*)o\b", 1),
    (r"(\w*)[a|e|i]?s\b", 1),
    (r"(\w*)[a|e|i]?t\b", 1),
    (r"(\w*)[a|e|i]?mus\b", 1),
    (r"(\w*)[a|e|i]?tis\b", 1),
    (r"(\w*)[a|e|u]nt\b", 1),
]

pip_patterns = [
    (r"(\w*)or\b", 1),
    (r"(\w*)[a|e]ris\b", 1),
    (r"(\w*e)ris\b", 1),
    (r"(\w*)[a|e|i]tur\b", 1),
    (r"(\w*e)tur\b", 1),
    (r"(\w*)[a|e|i]?mur\b", 1),
    (r"(\w*)[a|e|i]mini\b", 1),
    (r"(\w*)[a|e|u]ntur\b", 1),
]

psa_patterns = [
    (r"(\w*)em\b", 1),
    (r"(\w*)[a|e|ia]s\b", 1),
    (r"(\w*)[a|e|ia]t\b", 1),
    (r"(\w*)[a|e|ia]mus\b", 1),
    (r"(\w*)[a|e|ia]?tis\b", 1),
    (r"(\w*)[a|e|ia]nt\b", 1),
]

iia_patterns = [
    (r"(\w*)[a|ie]bam", 1),
    (r"(\w*)[a|ie]bas\b", 1),
    (r"(\w*)[a|ie]bat\b", 1),
    (r"(\w*)[a|ie]bamus\b", 1),
    (r"(\w*)[a|ie]batis\b", 1),
    (r"(\w*)[a|ie]bant\b", 1),
    (r"(\w*e?)bam\b", 1),
    (r"(\w*e?)bas\b", 1),
    (r"(\w*e?)bat\b", 1),
    (r"(\w*e?)bamus\b", 1),
    (r"(\w*e?)batis\b", 1),
    (r"(\w*e?)bant\b", 1),
]

isa_patterns = [
    (r"(\w*)m", 2),
    (r"(\w*)s\b", 2),
    (r"(\w*)t\b", 2),
    (r"(\w*)mus\b", 2),
    (r"(\w*)ris\b", 2),
    (r"(\w*)nt\b", 2),
]

iip_patterns = [
    (r"(\w*)[a|ie]bar", 1),
    (r"(\w*)[a|ie]baris\b", 1),
    (r"(\w*)[a|ie]batur\b", 1),
    (r"(\w*)[a|ie]bamur\b", 1),
    (r"(\w*)[a|ie]bamini\b", 1),
    (r"(\w*)[a|ie]bant\b", 1),
    (r"(\w*e?)bar\b", 1),
    (r"(\w*e?)baris\b", 1),
    (r"(\w*e?)batur\b", 1),
    (r"(\w*e?)bamur\b", 1),
    (r"(\w*e?)bamini\b", 1),
    (r"(\w*e?)bantur\b", 1),
]

isp_patterns = [
    (r"(\w*)r", 2),
    (r"(\w*)ris\b", 2),
    (r"(\w*)tur\b", 2),
    (r"(\w*)mur\b", 2),
    (r"(\w*)mini\b", 2),
    (r"(\w*)ntur\b", 2),
]

fia_patterns = [
    (r"(\w*)[a|ie]bo\b", 1),
    (r"(\w*)[a|ie]bis\b", 1),
    (r"(\w*)[a|ie]bit\b", 1),
    (r"(\w*)[a|ie]bimus\b", 1),
    (r"(\w*)[a|ie]bitis\b", 1),
    (r"(\w*)[a|ie]bunt\b", 1),
    (r"(\w*e)bo\b", 1),
    (r"(\w*e?)bis\b", 1),
    (r"(\w*e?)bit\b", 1),
    (r"(\w*e?)bimus\b", 1),
    (r"(\w*e?)bitis\b", 1),
    (r"(\w*e?)bunt\b", 1),
    (r"(\w*)am\b", 1),
    (r"(\w*)es\b", 1),
    (r"(\w*)et\b", 1),
    (r"(\w*)emus\b", 1),
    (r"(\w*)etis\b", 1),
    (r"(\w*)ent\b", 1),
]

fip_patterns = [
    (r"(\w*)[a|ie]bor\b", 1),
    (r"(\w*)[a|ie]beris\b", 1),
    (r"(\w*)[a|ie]bitur\b", 1),
    (r"(\w*)[a|ie]bimur\b", 1),
    (r"(\w*)[a|ie]bimini\b", 1),
    (r"(\w*)[a|ie]buntur\b", 1),
    (r"(\w*e)bor\b", 1),
    (r"(\w*e?)beris\b", 1),
    (r"(\w*e?)bitur\b", 1),
    (r"(\w*e?)bimur\b", 1),
    (r"(\w*e?)bimini\b", 1),
    (r"(\w*e?)buntur\b", 1),
    (r"(\w*)ar\b", 1),
    (r"(\w*)eris\b", 1),
    (r"(\w*)etur\b", 1),
    (r"(\w*)emur\b", 1),
    (r"(\w*)emini\b", 1),
    (r"(\w*)entur\b", 1),
]

pfia_patterns = [
    (r"(\w*)i\b", 3),
    (r"(\w*)isti\b", 3),
    (r"(\w*)it\b", 3),
    (r"(\w*)imus\b", 3),
    (r"(\w*)istis\b", 3),
    (r"(\w*)erunt\b", 3),
]

pfsa_patterns = []

ppfa_patterns = [
    (r"(\w*)eram\b", 3),
    (r"(\w*)eras\b", 3),
    (r"(\w*)erat\b", 3),
    (r"(\w*)eramus\b", 3),
    (r"(\w*)eratis\b", 3),
    (r"(\w*)erant\b", 3),
]

ppfsa_patterns = [
    (r"(\w*)issem", 3),
    (r"(\w*)isses\b", 3),
    (r"(\w*)isset\b", 3),
    (r"(\w*)issemus\b", 3),
    (r"(\w*)issetis\b", 3),
    (r"(\w*)issent\b", 3),
    (r"(\w*)asset\b", 1),
]

fpfa_patterns = [
    (r"(\w*)erim\b", 3),
    (r"(\w*)eris\b", 3),
    (r"(\w*)erit\b", 3),
    (r"(\w*)erimus\b", 3),
    (r"(\w*)eritis\b", 3),
    (r"(\w*)erint\b", 3),
]

latin_verb_patterns = (
    fpfa_patterns
    + ppfa_patterns
    + pfia_patterns
    + iia_patterns
    + fia_patterns
    + pia_patterns
    + pip_patterns
    + iip_patterns
    + psa_patterns
    + isa_patterns
    + isp_patterns
    + pfsa_patterns
    + ppfsa_patterns
)


rn_patterns = [
    (
        r"(?=^[MDCLXVUI]+$)(?=^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|IU|V?I{0,3}|U?I{0,3})$)",
        "NUM",
    ),
    (
        r"(?=^[mdclxvui]+$)(?=^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|iu|v?i{0,3}|u?i{0,3})$)",
        "NUM",
    ),
]


class RomanNumeralLemmatizer(RegexpLemmatizer):
    """Lemmatizer for identifying roman numerals in Latin text based on
    regex.

    >>> lemmatizer = RomanNumeralLemmatizer()
    >>> lemmatizer.lemmatize("i ii iii iv v vi vii vii ix x xx xxx xl l lx c cc".split())
    [('i', 'NUM'), ('ii', 'NUM'), ('iii', 'NUM'), ('iv', 'NUM'), ('v', 'NUM'), ('vi', 'NUM'), \
('vii', 'NUM'), ('vii', 'NUM'), ('ix', 'NUM'), ('x', 'NUM'), ('xx', 'NUM'), ('xxx', 'NUM'), \
('xl', 'NUM'), ('l', 'NUM'), ('lx', 'NUM'), ('c', 'NUM'), ('cc', 'NUM')]

    >>> lemmatizer = RomanNumeralLemmatizer(default="RN")
    >>> lemmatizer.lemmatize('i ii iii'.split())
    [('i', 'RN'), ('ii', 'RN'), ('iii', 'RN')]
    """

    def __init__(self: object, default: str = None, backoff: object = None):
        """
        RomanNumeralLemmatizer
        :type default: str
        :param default: Default replacement for lemma; 'NUM' in given pattern
        """
        regexps = [
            (
                r"(?=^[MDCLXVUI]+$)(?=^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|IU|V?I{0,3}|U?I{0,3})$)",
                "NUM",
            ),
            (
                r"(?=^[mdclxvui]+$)(?=^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|iu|v?i{0,3}|u?i{0,3})$)",
                "NUM",
            ),
        ]
        RegexpLemmatizer.__init__(self, regexps, backoff)
        self._regexs = [(re.compile(regexp), pattern) for regexp, pattern in regexps]
        self.default = default

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """Use regular expressions for rules-based lemmatizing based on word endings;
        tokens are matched for patterns with the base kept as a group; an word ending
        replacement is added to the (base) group.
        :rtype: str
        :type tokens: list
        :param tokens: List of tokens to be lemmatized
        :type index: int
        :param index: Int with current token
        :type history: list
        :param history: List with tokens that have already been lemmatized; NOT USED
        """
        for pattern, replace in self._regexs:
            if re.search(pattern, tokens[index]):
                if self.default:
                    return self.default
                else:
                    return replace

    def __repr__(self: object):
        return f"<{type(self).__name__}: CLTK Roman Numeral Patterns>"


models_path = os.path.normpath(
    os.path.join(CLTK_DATA_DIR, "lat/model/lat_models_cltk/lemmata/backoff")
)


class LatinBackoffLemmatizer:
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer AKA BackoffLatinLemmatizer
    ### For comparison, there is also a TrainLemmatizer that replicates the
    ###    original Latin lemmatizer from cltk.stem
    """

    def __init__(
        self: object, train: List[list] = None, seed: int = 3, verbose: bool = False
    ):
        self.models_path = models_path

        missing_models_message = "LatinBackoffLemmatizer requires the ```latin_models_cltk``` to be in cltk_data. Please load this corpus."

        try:
            self.train = open_pickle(
                os.path.join(self.models_path, "latin_pos_lemmatized_sents.pickle")
            )
            self.LATIN_OLD_MODEL = open_pickle(
                os.path.join(self.models_path, "latin_lemmata_cltk.pickle")
            )
            self.LATIN_MODEL = open_pickle(
                os.path.join(self.models_path, "latin_model.pickle")
            )
        except FileNotFoundError as err:
            raise type(err)(missing_models_message)

        self.latin_sub_patterns = latin_sub_patterns  # Move to latin_models_cltk

        self.seed = seed
        self.VERBOSE = verbose

        def _randomize_data(train: List[list], seed: int):
            import random

            random.seed(seed)
            random.shuffle(train)
            train_size = int(0.9 * len(train))
            pos_train_sents = train[:train_size]
            lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
            train_sents = lem_train_sents[:train_size]
            test_sents = lem_train_sents[train_size:]

            return pos_train_sents, train_sents, test_sents

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(
            self.train, self.seed
        )
        self._define_lemmatizer()

    def _define_lemmatizer(self: object):
        # Suggested backoff chain--should be tested for optimal order
        self.backoff0 = None
        self.backoff1 = IdentityLemmatizer(verbose=self.VERBOSE)
        self.backoff2 = DictLemmatizer(
            lemmas=self.LATIN_OLD_MODEL,
            source="Morpheus Lemmas",
            backoff=self.backoff1,
            verbose=self.VERBOSE,
        )
        self.backoff3 = RegexpLemmatizer(
            self.latin_sub_patterns,
            source="CLTK Latin Regex Patterns",
            backoff=self.backoff2,
            verbose=self.VERBOSE,
        )
        self.backoff4 = UnigramLemmatizer(
            self.train_sents,
            source="CLTK Sentence Training Data",
            backoff=self.backoff3,
            verbose=self.VERBOSE,
        )
        self.backoff5 = DictLemmatizer(
            lemmas=self.LATIN_MODEL,
            source="Latin Model",
            backoff=self.backoff4,
            verbose=self.VERBOSE,
        )
        self.lemmatizer = self.backoff5

    def lemmatize(self: object, tokens: List[str]):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self: object):
        if self.VERBOSE:
            raise AssertionError(
                "evaluate() method only works when verbose: bool = False"
            )
        return self.lemmatizer.evaluate(self.test_sents)

    def __repr__(self: object):
        return f"<BackoffLatinLemmatizer v0.2>"

    def __call__(self, token: str) -> str:
        return self.lemmatize([token])[0][0]
