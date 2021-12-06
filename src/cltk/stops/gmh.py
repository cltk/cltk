"""
Middle High German: 
"Eleftheria Chatziargyriou <ele.hatzy@gmail.com>" using TFIDF method. Source of texts: http://www.gutenberg.org/files/22636/22636-h/22636-h.htm , http://texte.mediaevum.de/12mhd.htm
"Peter Hinkelmanns <peter.hinkelmanns@plus.ac.at" added 278 stops from most frequent words of MHDBDB corpus (http://www.mhdbdb.sbg.ac.at/).
"""
STOPS = [
	"!",
	"(",
	")",
	",",
	"-",
	".",
	"...",
	"/",
	":",
	";",
	"<",
	">",
	"?",
	"ab",
	"abe",
	"aber",
	"ach",
	"ain",
	"ainem",
	"ainen",
	"al",
	"all",
	"alle",
	"allem",
	"allen",
	"aller",
	"alles",
	"allez",
	"alleȥ",
	"als",
	"alsam",
	"alse",
	"also",
	"alsus",
	"alsô",
	"alz",
	"an",
	"ander",
	"andern",
	"anders",
	"ane",
	"auch",
	"auf",
	"auff",
	"aus",
	"bald",
	"balde",
	"baz",
	"beide",
	"beiden",
	"beider",
	"beidiu",
	"bereit",
	"besten",
	"besunder",
	"bi",
	"bin",
	"bist",
	"biz",
	"biß",
	"by",
	"bî",
	"czu",
	"da",
	"dan",
	"dann",
	"danne",
	"dannen",
	"dannoch",
	"dar",
	"daran",
	"darnach",
	"darumb",
	"darumbe",
	"darzuo",
	"das",
	"dat",
	"daz",
	"daȥ",
	"dehein",
	"dem",
	"deme",
	"den",
	"denn",
	"denne",
	"der",
	"des",
	"deste",
	"det",
	"dez",
	"di",
	"dich",
	"die",
	"din",
	"dir",
	"dirre",
	"dis",
	"dise",
	"disem",
	"diseme",
	"disen",
	"diser",
	"dises",
	"disiu",
	"ditz",
	"ditze",
	"diu",
	"div",
	"diz",
	"diȥ",
	"do",
	"doch",
	"dort",
	"du",
	"dur",
	"durch",
	"durfen",
	"dy",
	"dâ",
	"dâr",
	"dâvon",
	"dën",
	"dër",
	"dëre",
	"dîme",
	"dîn",
	"dînme",
	"dô",
	"dû",
	"e",
	"eim",
	"eime",
	"ein",
	"eine",
	"einem",
	"einen",
	"einer",
	"eines",
	"eins",
	"elliu",
	"en",
	"ende",
	"er",
	"es",
	"et",
	"euch",
	"eyn",
	"eynen",
	"ez",
	"eȥ",
	"fi",
	"fuer",
	"fur",
	"für",
	"gar",
	"gerne",
	"got",
	"güete",
	"hab",
	"habe",
	"haben",
	"habent",
	"habt",
	"haete",
	"han",
	"hat",
	"hatt",
	"he",
	"her",
	"het",
	"hete",
	"heten",
	"hett",
	"hette",
	"hetten",
	"hie",
	"hin",
	"hinnen",
	"hiute",
	"hân",
	"hâst",
	"hât",
	"hâte",
	"hêre",
	"hêt",
	"hîz",
	"ich",
	"icht",
	"ie",
	"iedoch",
	"ieman",
	"iemen",
	"iemer",
	"iht",
	"im",
	"ime",
	"immer",
	"in",
	"ind",
	"inn",
	"inne",
	"ir",
	"iren",
	"irn",
	"irs",
	"is",
	"ist",
	"iu",
	"iuch",
	"iuwer",
	"iuwern",
	"iv",
	"iwer",
	"iz",
	"ja",
	"jn",
	"jâ",
	"kan",
	"kein",
	"klage",
	"kleine",
	"kunnen",
	"künnen",
	"lange",
	"leide",
	"lîhte",
	"mag",
	"magen",
	"man",
	"manic",
	"manig",
	"manigen",
	"maniger",
	"me",
	"megen",
	"mein",
	"mer",
	"mere",
	"mich",
	"michel",
	"min",
	"mine",
	"minen",
	"miner",
	"mir",
	"mit",
	"mite",
	"mitt",
	"mocht",
	"moht",
	"mohte",
	"mohten",
	"mohten ",
	"mugen",
	"muost",
	"muoste",
	"muoz",
	"muoȥ",
	"muß",
	"myn",
	"mê",
	"mêr",
	"mêre",
	"mîn",
	"mîne",
	"mînem",
	"mînen",
	"mîner",
	"möht",
	"möhte",
	"müezen",
	"mügen",
	"nach",
	"ne",
	"nein",
	"nicht",
	"nie",
	"nieman",
	"niemen",
	"niemer",
	"niht",
	"nit",
	"noch",
	"nu",
	"nun",
	"nv",
	"nye",
	"nâch",
	"nû",
	"ob",
	"och",
	"oder",
	"off",
	"on",
	"ouch",
	"ovch",
	"owe",
	"owê",
	"rede",
	"rehte",
	"schiere",
	"schon",
	"schone",
	"schône",
	"sei",
	"sein",
	"seinem",
	"seinen",
	"seiner",
	"seit",
	"selb",
	"selbe",
	"selben",
	"selber",
	"selbes",
	"sere",
	"sey",
	"si",
	"sich",
	"sie",
	"siht",
	"sin",
	"sind",
	"sine",
	"sinem",
	"sinen",
	"siner",
	"sint",
	"sit",
	"site",
	"siten",
	"siu",
	"so",
	"sol",
	"solde",
	"solden",
	"solen",
	"solt",
	"solte",
	"solten",
	"suln",
	"sult",
	"sunder",
	"sus",
	"swa",
	"swaz",
	"swenn",
	"swenne",
	"swer",
	"swes",
	"swie",
	"swâ",
	"sy",
	"syn",
	"synen",
	"sêre",
	"sî",
	"sîme",
	"sîn",
	"sîne",
	"sînem",
	"sînen",
	"sîner",
	"sînes",
	"sînme",
	"sît",
	"sô",
	"süln",
	"tet",
	"tete",
	"thun",
	"tuo",
	"tuon",
	"tuot",
	"tzu",
	"uch",
	"uf",
	"uff",
	"umb",
	"umbe",
	"und",
	"unde",
	"under",
	"uns",
	"unser",
	"unt",
	"unz",
	"uwer",
	"uz",
	"uß",
	"vaste",
	"vber",
	"vil",
	"vmb",
	"vnd",
	"vnde",
	"vnder",
	"vns",
	"vnser",
	"vol",
	"von",
	"vor",
	"vô",
	"vür",
	"wa",
	"waer",
	"waere",
	"wan",
	"wand",
	"wande",
	"wann",
	"want",
	"war",
	"ward",
	"waren",
	"warn",
	"wart",
	"was",
	"waz",
	"waȥ",
	"we",
	"weder",
	"wegen",
	"welle",
	"wellen",
	"wen",
	"wenn",
	"wenne",
	"wer",
	"werd",
	"werde",
	"werden",
	"werdent",
	"werder",
	"were",
	"weren",
	"wert",
	"wes",
	"wesen",
	"who",
	"wider",
	"wie",
	"wiedder",
	"wil",
	"willen",
	"wir",
	"wirde",
	"wirt",
	"wiu",
	"wo",
	"wol",
	"wolde",
	"wolden",
	"wolt",
	"wolte",
	"wolten",
	"worden",
	"wurd",
	"wurde",
	"wurden",
	"wâ",
	"wâr",
	"wâren",
	"wârn",
	"wær",
	"wære",
	"wê",
	"wëm",
	"wëme",
	"wën",
	"wër",
	"wës",
	"würde",
	"ye",
	"ym",
	"yme",
	"yn",
	"yne",
	"zcu",
	"ze",
	"zehant",
	"zer",
	"zu",
	"zuo",
	"zwischen",
	"zû",
	"zü",
	"«",
	"»",
	"ân",
	"âne",
	"ê",
	"êren",
	"în",
	"ûf",
	"ûz",
	"über"
]
