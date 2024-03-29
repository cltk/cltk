"""
Middle High German: "Eleftheria Chatziargyriou <ele.hatzy@gmail.com>" using TFIDF method. Source of texts: http://www.gutenberg.org/files/22636/22636-h/22636-h.htm , http://texte.mediaevum.de/12mhd.htm
"""
STOPS: list[str] = [
    "abe",
    "aber",
    "al",
    "alle",
    "allen",
    "aller",
    "alleȥ",
    "als",
    "alse",
    "alsô",
    "an",
    "ander",
    "andern",
    "anders",
    "ane",
    "âne",
    "beide",
    "besten",
    "bin",
    "bî",
    "dan",
    "danne",
    "dar",
    "daz",
    "daȥ",
    "dem",
    "den",
    "der",
    "des",
    "dich",
    "die",
    "dir",
    "dirre",
    "dise",
    "disem",
    "diseme",
    "disen",
    "diser",
    "dises",
    "disiu",
    "ditze",
    "diu",
    "diz",
    "diȥ",
    "doch",
    "du",
    "durch",
    "durfen",
    "dâ",
    "dën",
    "dër",
    "dëre",
    "dîn",
    "dô",
    "dû",
    "dâ",
    "dâr",
    "dîn",
    "dînme",
    "dîme",
    "ê",
    "ein",
    "eine",
    "einem",
    "einen",
    "einer",
    "en",
    "ende",
    "er",
    "êren",
    "es",
    "ez",
    "eȥ",
    "fi",
    "für",
    "gar",
    "gerne",
    "got",
    "güete",
    "haben",
    "he",
    "her",
    "hete",
    "hie",
    "hin",
    "hiute",
    "hân",
    "hâst",
    "hât",
    "hâte",
    "hêre",
    "hîz",
    "ich",
    "ie",
    "iemen",
    "iemer",
    "iht",
    "im",
    "ime",
    "in",
    "ir",
    "ist",
    "iu",
    "iuch",
    "iuwer",
    "iuwern",
    "kan",
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
    "megen",
    "mich",
    "mir",
    "mit",
    "mite",
    "mohten ",
    "mugen",
    "muoȥ",
    "mîn",
    "möhte",
    "müezen",
    "mügen",
    "mêr",
    "mêre",
    "mîn",
    "mîne",
    "mînen",
    "nicht",
    "nie",
    "nieman",
    "niemer",
    "niht",
    "noch",
    "nu",
    "nâch",
    "nû",
    "ob",
    "oder",
    "ouch",
    "rede",
    "rehte",
    "schiere",
    "selbe",
    "selben",
    "si",
    "sich",
    "sie",
    "sint",
    "sol",
    "solde",
    "solen",
    "solt",
    "suln",
    "sult",
    "sus",
    "sî",
    "sîn",
    "sô",
    "süln",
    "sêre",
    "sî",
    "sîme",
    "sîn",
    "sînen",
    "sînme",
    "sô",
    "tet",
    "tuon",
    "über",
    "ûf",
    "umbe",
    "und",
    "unde",
    "under",
    "uns",
    "unser",
    "unt",
    "unz",
    "ûz",
    "vaste",
    "vil",
    "von",
    "vor",
    "vô",
    "vür",
    "wan",
    "wart",
    "was",
    "waȥ",
    "wellen",
    "wer",
    "werden",
    "who",
    "wider",
    "wie",
    "wil",
    "willen",
    "wir",
    "wiu",
    "wol",
    "wolde",
    "wære",
    "wëm",
    "wëme",
    "wën",
    "wër",
    "wës",
    "ze",
    "zer",
    "zu",
    "zû",
    "zuo",
]
