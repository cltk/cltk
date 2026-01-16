"""Centralized language definitions for CLTK.

This module contains the canonical list of supported languages with their
Glottolog IDs and display names. It serves as the single source of truth
for generating language-specific process classes.

Adding a New Language
---------------------
To add support for a new language, add a single line to LANGUAGE_DEFINITIONS:

    LanguageDef("Sumerian", "sume1241", "Sumerian"),

This will automatically generate:
- SumerianGenAIMorphosyntaxProcess
- SumerianGenAIDependencyProcess

The Glottolog ID must match the pattern [a-z]{4}[0-9]{4} (e.g., "sume1241").
Look up the correct ID at https://glottolog.org/
"""

from typing import NamedTuple


class LanguageDef(NamedTuple):
    """Definition for a supported language.

    Attributes:
        class_prefix: Prefix for generated class names (e.g., "Latin" ->
            LatinGenAIMorphosyntaxProcess).
        glottolog_id: Glottolog identifier (e.g., "lati1261").
        display_name: Human-readable language name for descriptions.

    """

    class_prefix: str
    glottolog_id: str
    display_name: str


# Canonical list of all supported languages
# Sorted alphabetically by class_prefix for maintainability
LANGUAGE_DEFINITIONS: tuple[LanguageDef, ...] = (
    LanguageDef("Akkadian", "akka1240", "Akkadian"),
    LanguageDef("Albanian", "gheg1238", "Albanian"),
    LanguageDef("Ammonite", "ammo1234", "Ammonite"),
    LanguageDef("AncientGreek", "anci1242", "Ancient Greek"),
    LanguageDef("Assamese", "assa1263", "Assamese"),
    LanguageDef("Avestan", "aves1237", "Avestan"),
    LanguageDef("Awadhi", "awad1243", "Awadhi"),
    LanguageDef("Bactrian", "bact1239", "Bactrian"),
    LanguageDef("Bagri", "bagr1243", "Bagri"),
    LanguageDef("BaihuaChinese", "clas1255", "Baihua Chinese"),
    LanguageDef("Bengali", "beng1280", "Bengali"),
    LanguageDef("BiblicalHebrew", "anci1244", "Biblical Hebrew"),
    LanguageDef("Braj", "braj1242", "Braj"),
    LanguageDef("Carian", "cari1274", "Carian"),
    LanguageDef("Chagatai", "chag1247", "Chagatai"),
    LanguageDef("ChurchSlavic", "chur1257", "Church Slavic"),
    LanguageDef("ClassicalArabic", "clas1259", "Classical Arabic"),
    LanguageDef("ClassicalArmenian", "clas1256", "Classical Armenian"),
    LanguageDef("ClassicalBurmese", "nucl1310", "Classical Burmese"),
    LanguageDef("ClassicalMandaic", "clas1253", "Classical Mandaic"),
    LanguageDef("ClassicalMongolian", "mong1331", "Classical Mongolian"),
    LanguageDef("ClassicalSanskrit", "clas1258", "Classical Sanskrit"),
    LanguageDef("ClassicalSyriac", "clas1252", "Classical Syriac"),
    LanguageDef("ClassicalTibetan", "clas1254", "Classical Tibetan"),
    LanguageDef("Coptic", "copt1239", "Coptic"),
    LanguageDef("CuneiformLuwian", "cune1239", "Cuneiform Luwian"),
    LanguageDef("Demotic", "demo1234", "Demotic"),
    LanguageDef("EarlyIrish", "oldi1245", "Early Irish"),
    LanguageDef("EasternPanjabi", "panj1256", "Eastern Panjabi"),
    LanguageDef("Edomite", "edom1234", "Edomite"),
    LanguageDef("Gandhari", "gand1259", "Gandhari"),
    LanguageDef("Geez", "geez1241", "Geez"),
    LanguageDef("Gothic", "goth1244", "Gothic"),
    LanguageDef("Gujarati", "guja1252", "Gujarati"),
    LanguageDef("Hatran", "hatr1234", "Hatran"),
    LanguageDef("Hausa", "haus1257", "Hausa"),
    LanguageDef("HieroglyphicLuwian", "hier1240", "Hieroglyphic Luwian"),
    LanguageDef("Hindi", "hind1269", "Hindi"),
    LanguageDef("Hittite", "hitt1242", "Hittite"),
    LanguageDef("JewishBabylonianAramaic", "jewi1240", "Jewish Babylonian Aramaic"),
    LanguageDef("Kashmiri", "kash1277", "Kashmiri"),
    LanguageDef("KhariBoli", "khad1239", "Khari Boli"),
    LanguageDef("Khotanese", "khot1251", "Khotanese"),
    LanguageDef("LateEgyptian", "late1256", "Late Egyptian"),
    LanguageDef("Latin", "lati1261", "Latin"),
    LanguageDef("Latvian", "latv1249", "Latvian"),
    LanguageDef("LiteraryChinese", "lite1248", "Literary Chinese"),
    LanguageDef("Lithuanian", "lith1251", "Lithuanian"),
    LanguageDef("LycianA", "lyci1241", "Lycian A"),
    LanguageDef("Lydian", "lydi1241", "Lydian"),
    LanguageDef("MagadhiPrakrit", "maga1260", "Magadhi Prakrit"),
    LanguageDef("MaharastriPrakrit", "maha1305", "Maharastri Prakrit"),
    LanguageDef("Marathi", "mara1378", "Marathi"),
    LanguageDef("Meitei", "mani1292", "Meitei"),
    LanguageDef("MiddleAramaic", "midd1366", "Middle Aramaic"),
    LanguageDef("MiddleArmenian", "midd1364", "Middle Armenian"),
    LanguageDef("MiddleBreton", "oldb1244", "Middle Breton"),
    LanguageDef("MiddleChinese", "midd1344", "Middle Chinese"),
    LanguageDef("MiddleCornish", "corn1251", "Middle Cornish"),
    LanguageDef("MiddleEgyptian", "midd1369", "Middle Egyptian"),
    LanguageDef("MiddleEnglish", "midd1317", "Middle English"),
    LanguageDef("MiddleFrench", "midd1316", "Middle French"),
    LanguageDef("MiddleHighGerman", "midd1343", "Middle High German"),
    LanguageDef("MiddleMongol", "mong1329", "Middle Mongol"),
    LanguageDef("MiddlePersian", "pahl1241", "Middle Persian"),
    LanguageDef("Moabite", "moab1234", "Moabite"),
    LanguageDef("Mogholi", "mogh1245", "Mogholi"),
    LanguageDef("Newar", "newa1246", "Newar"),
    LanguageDef("Numidian", "numi1241", "Numidian"),
    LanguageDef("Odia", "oriy1255", "Odia"),
    LanguageDef("OfficialAramaic", "impe1235", "Official Aramaic"),
    LanguageDef("OldAramaic", "olda1246", "Old Aramaic"),
    LanguageDef("OldAramaicSamalian", "olda1245", "Old Aramaic Samalian"),
    LanguageDef("OldBurmese", "oldb1235", "Old Burmese"),
    LanguageDef("OldChinese", "oldc1244", "Old Chinese"),
    LanguageDef("OldEgyptian", "olde1242", "Old Egyptian"),
    LanguageDef("OldEnglish", "olde1238", "Old English"),
    LanguageDef("OldFrench", "oldf1239", "Old French"),
    LanguageDef("OldHighGerman", "oldh1241", "Old High German"),
    LanguageDef("OldHungarian", "oldh1242", "Old Hungarian"),
    LanguageDef("OldJapanese", "japo1237", "Old Japanese"),
    LanguageDef("OldJurchen", "jurc1239", "Old Jurchen"),
    LanguageDef("OldMiddleWelsh", "oldw1239", "Old Middle Welsh"),
    LanguageDef("OldNorse", "oldn1244", "Old Norse"),
    LanguageDef("OldPersian", "oldp1254", "Old Persian"),
    LanguageDef("OldPrussian", "prus1238", "Old Prussian"),
    LanguageDef("OldTamil", "oldt1248", "Old Tamil"),
    LanguageDef("OldTurkic", "oldu1238", "Old Turkic"),
    LanguageDef("Palaic", "pala1331", "Palaic"),
    LanguageDef("Pali", "pali1273", "Pali"),
    LanguageDef("Parthian", "part1239", "Parthian"),
    LanguageDef("Phoenician", "phoe1239", "Phoenician"),
    LanguageDef("Punjabi", "panj1256", "Punjabi"),
    LanguageDef("Samalian", "sama1234", "Samalian"),
    LanguageDef("SauraseniPrakrit", "saur1252", "Sauraseni Prakrit"),
    LanguageDef("SgawKaren", "sgaw1245", "Sgaw Karen"),
    LanguageDef("Sindhi", "sind1272", "Sindhi"),
    LanguageDef("Sinhala", "sinh1246", "Sinhala"),
    LanguageDef("Sogdian", "sogd1245", "Sogdian"),
    LanguageDef("Taita", "tait1247", "Taita"),
    LanguageDef("Tangut", "tang1334", "Tangut"),
    LanguageDef("TokharianA", "toch1238", "Tokharian A"),
    LanguageDef("TokharianB", "toch1237", "Tokharian B"),
    LanguageDef("Tumshuqese", "tums1237", "Tumshuqese"),
    LanguageDef("Ugaritic", "ugar1238", "Ugaritic"),
    LanguageDef("Urdu", "urdu1245", "Urdu"),
    LanguageDef("VedicSanskrit", "vedi1234", "Vedic Sanskrit"),
)

# Quick lookup by glottolog_id
GLOTTOLOG_TO_LANGUAGE: dict[str, LanguageDef] = {
    lang.glottolog_id: lang for lang in LANGUAGE_DEFINITIONS
}

# Quick lookup by class prefix
PREFIX_TO_LANGUAGE: dict[str, LanguageDef] = {
    lang.class_prefix: lang for lang in LANGUAGE_DEFINITIONS
}
