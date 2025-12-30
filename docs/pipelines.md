# Pipelines

This page reflects the CLTK's pre-defined language `Pipelines`.

## Stanza

Stanza models (for moprhology and syntax labeling) are available for the following languages.

<!-- PIPELINES:STANZA:START -->
<details>
<summary>Current Stanza pipeline map (generated from `src/cltk/languages/pipelines.py`)</summary>

```python
MAP_LANGUAGE_CODE_TO_STANZA_PIPELINE: dict[str, type[Pipeline]] = {
    # Seed a few languages where Stanza has robust models
    "lati1261": LatinStanzaPipeline,
    "anci1242": AncientGreekStanzaPipeline,
    "chur1257": ChurchSlavonicStanzaPipeline,
    "oldf1239": OldFrenchStanzaPipeline,
    "goth1244": GothicStanzaPipeline,
    "lite1248": LiteraryChineseStanzaPipeline,
    "olde1238": OldEnglishStanzaPipeline,
    "otto1234": OttomanTurkishStanzaPipeline,
    "clas1256": ClassicalArmenianStanzaPipeline,
    "copt1239": CopticStanzaPipeline,
    "oldr1238": OldRussianStanzaPipeline,  # Old East Slavic
}
```

</details>
<!-- PIPELINES:STANZA:END -->


## Generative AI

The CLTK has defined `Pipeline` for the following languages. These may be invoked by any generative LLM backend (i.e., `"openai"`, `"mistral"`, `"ollama"`).

<!-- PIPELINES:GENAI:START -->
<details>
<summary>Current generative pipeline map (generated from `src/cltk/languages/pipelines.py`)</summary>

```python
MAP_LANGUAGE_CODE_TO_GENERATIVE_PIPELINE: dict[str, type[Pipeline]] = {
    # Indo-European family
    ## Italic
    "lati1261": LatinGenAIPipeline,
    "oldf1239": OldFrenchGenAIPipeline,
    "midd1316": MiddleFrenchGenAIPipeline,
    # Other Romance languages
    ## Hellenic
    "anci1242": AncientGreekGenAIPipeline,
    # Mycenaean Greek (Linear B tablets, ca. 1400–1200 BCE).
    # Medieval/Byzantine Greek
    "oldi1245": EarlyIrishGenAIPipeline,
    "oldw1239": OldMiddleWelshGenAIPipeline,
    "bret1244": MiddleBretonGenAIPipeline,
    "corn1251": MiddleCornishGenAIPipeline,
    ## Germanic
    # Proto-Norse
    "goth1244": GothicGenAIPipeline,
    "oldh1241": OldHighGermanGenAIPipeline,
    "midd1343": MiddleHighGermanGenAIPipeline,
    "oldn1244": OldNorseGenAIPipeline,
    "olde1238": OldEnglishGenAIPipeline,
    "midd1317": MiddleEnglishGenAIPipeline,
    ## Balto-Slavic
    "chur1257": ChurchSlavonicGenAIPipeline,
    "prus1238": OldPrussianGenAIPipeline,
    "lith1251": LithuanianGenAIPipeline,
    "latv1249": LatvianGenAIPipeline,
    "gheg1238": AlbanianGenAIPipeline,
    ## Armenian, Earliest texts: 5th c. CE (Bible translation by Mesrop Mashtots, who created the script)
    "clas1256": ClassicalArmenianGenAIPipeline,
    "midd1364": MiddleArmenianGenAIPipeline,
    # Note this is only a parent, not true languoid
    ## Anatolian
    "hitt1242": HittiteGenAIPipeline,
    "cune1239": CuneiformLuwianGenAIPipeline,
    "hier1240": HieroglyphicLuwianGenAIPipeline,
    "lyci1241": LycianAGenAIPipeline,
    "lydi1241": LydianGenAIPipeline,
    "pala1331": PalaicGenAIPipeline,
    "cari1274": CarianGenAIPipeline,
    ## Tocharian
    "tokh1242": TocharianAGenAIPipeline,
    "tokh1243": TocharianBGenAIPipeline,
    ## Indo-Iranian
    ## Iranian languages
    ### SW Iranian
    "oldp1254": OldPersianGenAIPipeline,
    "pahl1241": MiddlePersianGenAIPipeline,
    ### NW Iranian
    "part1239": ParthianGenAIPipeline,
    ### E Iranian
    "aves1237": AvestanGenAIPipeline,
    "bact1239": BactrianGenAIPipeline,
    "sogd1245": SogdianGenAIPipeline,
    "khot1251": KhotaneseGenAIPipeline,
    "tums1237": TumshuqeseGenAIPipeline,
    # Indo-Aryan (Indic): Sanskrit (Vedic & Classical), Prakrits, Pali, later medieval languages (Hindi, Bengali, etc.)
    ## Old Indo-Aryan
    "vedi1234": VedicSanskritGenAIPipeline,
    "clas1258": ClassicalSanskritGenAIPipeline,
    # Prakrits (Middle Indo-Aryan, ca. 500 BCE–500 CE)
    "pali1273": PaliGenAIPipeline,
    # Ardhamāgadhī, Śaurasenī, Mahārāṣṭrī, etc. — languages of Jain/Buddhist texts and early drama.
    # ? Glotto says alt_name for Pali; Ardhamāgadhī, literary language associated with Magadha (eastern India); Jain canonical texts (the Āgamas) are written primarily in Ardhamāgadhī
    "saur1252": SauraseniPrakritGenAIPipeline,
    "maha1305": MaharastriPrakritGenAIPipeline,
    "maga1260": MagadhiPrakritGenAIPipeline,
    "gand1259": GandhariGenAIPipeline,  ## Middle Indo-Aryan
    # "Maithili": "mait1250"; Apabhraṃśa; "Apabhramsa" is alt_name; (500–1200 CE); Bridges Prakrits → New Indo-Aryan
    ## New Indo-Aryan
    ## Medieval languages (~1200 CE onward):
    # Early forms of Hindi, Bengali, Gujarati, Marathi, Punjabi, Oriya, Sinhala, etc
    # North-Western / Hindi Belt
    "hind1269": HindiGenAIPipeline,
    "khad1239": KhariBoliGenAIPipeline,
    "braj1242": BrajGenAIPipeline,
    "awad1243": AwadhiGenAIPipeline,
    "urdu1245": UrduGenAIPipeline,
    # Eastern Indo-Aryan
    "beng1280": BengaliGenAIPipeline,
    "oriy1255": OdiaGenAIPipeline,
    "assa1263": AssameseGenAIPipeline,
    # Western Indo-Aryan
    "guja1252": GujaratiGenAIPipeline,
    "mara1378": MarathiGenAIPipeline,
    # Southern Indo-Aryan / adjacency
    "sinh1246": SinhalaGenAIPipeline,
    # Northwestern frontier
    "panj1256": EasternPanjabiGenAIPipeline,
    "sind1272": SindhiGenAIPipeline,
    "kash1277": KashmiriGenAIPipeline,
    "bagr1243": BagriGenAIPipeline,
    # Afroasiatic family
    ## Semitic languages
    ### East Semitic
    "akka1240": AkkadianGenAIPipeline,
    # Eblaite
    ### West Semitic
    "ugar1238": UgariticGenAIPipeline,
    "phoe1239": PhoenicianGenAIPipeline,
    "moab1234": MoabiteGenAIPipeline,
    "ammo1234": AmmoniteGenAIPipeline,
    "edom1234": EdomiteGenAIPipeline,
    "anci1244": BiblicalHebrewGenAIPipeline,
    # Medieval Hebrew: No Glottolog
    # "moab1234": Moabite
    # "ammo1234": Ammonite
    # "edom1234": Edomite
    # Old Aramaic (ca. 1000–700 BCE, inscriptions).
    # "olda1246": "Old Aramaic (up to 700 BCE)",
    # "Old Aramaic-Sam'alian": "olda1245"
    "impe1235": ImperialAramaicGenAIPipeline,
    "olda1246": OldAramaicGenAIPipeline,
    "olda1245": OldAramaicSamalianGenAIPipeline,
    "midd1366": MiddleAramaicGenAIPipeline,
    "clas1253": ClassicalMandaicGenAIPipeline,
    "hatr1234": HatranGenAIPipeline,
    "jewi1240": JewishBabylonianAramaicGenAIPipeline,
    "sama1234": SamalianGenAIPipeline,
    # "midd1366": Middle Aramaic (200 BCE – 700 CE), includes Biblical Aramaic, Palmyrene, Nabataean, Targumic Aramaic.
    # Eastern Middle Aramaic
    ##  Classical Mandaic, Hatran, Jewish Babylonian Aramaic dialects, and Classical Syriac
    "clas1252": ClassicalSyriacGenAIPipeline,
    ### NW Semitic
    ## South Semitic
    # Old South Arabian (OSA)
    "geez1241": GeezGenAIPipeline,
    ### Central Semitic (bridge between NW and South)
    # Pre-Islamic Arabic
    "clas1259": ClassicalArabicGenAIPipeline,  # Dialect
    # Glotto doesn't have medieval arabic; Medieval Arabic: scientific, philosophical, historical works dominate much of the Islamic Golden Age corpus.
    ## Egyptian languages
    "olde1242": OldEgyptianGenAIPipeline,
    "midd1369": MiddleEgyptianGenAIPipeline,
    "late1256": LateEgyptianGenAIPipeline,
    "demo1234": DemoticGenAIPipeline,
    "copt1239": CopticGenAIPipeline,
    ## Berber
    "numi1241": NumidianGenAIPipeline,
    "tait1247": TaitaGenAIPipeline,
    ## Chadic
    # ; "haus1257": "Hausa"; Hausa; Essentially oral until medieval period, when Hausa is written in Ajami (Arabic script).
    "haus1257": HausaGenAIPipeline,
    "lite1248": LiteraryChineseGenAIPipeline,
    "clas1254": ClassicalTibetanPipeline,
    # Sino-Tibetan family
    # | **Early Vernacular Chinese (Baihua)**   | ca. 10th – 18th c. CE | *(under `clas1255`)* |
    # | **Old Tibetan**                         | 7th – 10th c. CE     | *(not separately coded)* |
    "oldc1244": OldChineseGenAIPipeline,
    "midd1344": MiddleChineseGenAIPipeline,
    "clas1255": BaihuaChineseGenAIPipeline,
    "oldb1235": OldBurmeseGenAIPipeline,
    "nucl1310": ClassicalBurmeseGenAIPipeline,
    "tang1334": TangutGenAIPipeline,
    "newa1246": NewarGenAIPipeline,
    "mani1292": MeiteiGenAIPipeline,
    "sgaw1245": SgawKarenGenAIPipeline,
    # Mongolic family
    "mong1329": MiddleMongolGenAIPipeline,
    "mong1331": ClassicalMongolianGenAIPipeline,  #  TODO: No glottolog broken
    "mogh1245": MogholiGenAIPipeline,
    # Altaic-Adj.
    "jurc1239": OldJurchenGenAIPipeline,
    # Japonic
    "japo1237": OldJapaneseGenAIPipeline,
    # Uralic
    "oldh1242": OldHungarianGenAIPipeline,
    # Turkic
    "chag1247": ChagataiGenAIPipeline,
    "oldu1238": OldTurkicGenAIPipeline,
    # TODO: Make pipeline for Ottoman Turkish
    # "otto1234": OttomanTurkishGenAIPipeline,
    # Dravidian
    "oldt1248": OldTamilGenAIPipeline,
    # Pre-Modern Literate Language Families (Non-Euro/Afroasiatic/Sino-Tibetan/Mongolic)
    # | Family         | Language / Stage           | Approx. Period      | Glottocode     |
    # |----------------|-----------------------------|----------------------|----------------|
    # | Dravidian      | Old Tamil                   | ca. 300 BCE–300 CE   | `oldt1248`     |
    # |                | Middle Tamil                | medieval             | *(not coded)*  |
    # |                | Old Kannada                 | from 5th c. CE       | *(not coded)*  |
    # |                | Old Telugu                  | from 6th c. CE       | *(not coded)*  |
    # |                | Old Malayalam               | from 13th c. CE      | *(not coded)*  |
    # | Turkic         | Old Turkic                  | 8th–10th c. CE       | `oldu1238`     |
    # |                | Chagatai                    | 15th–18th c. CE      | `chag1247`     |
    # | Uralic         | Old Hungarian               | 12th–13th c. CE      | `oldh1242`     |
    # | Koreanic       | Old Korean                  | 7th–10th c. CE       | *(not coded)*  |
    # |                | Middle Korean               | 15th c. onward       | *(not coded)*  |
    # | Japonic        | Old Japanese                | 8th c. CE            | `japo1237`     |
    # | Altaic-Adj.    | Old Jurchen                 | 12th–13th c. CE      | *`jurc1239`*  |
    # |                | Manchu                      | 17th–18th c. CE      | *(not coded)*  |
    # | Austroasiatic  | Old Mon                     | from 6th c. CE       | *(not coded)*  |
    # |                | Old Khmer                   | from 7th c. CE       | *(not coded)*  |
    # | Austronesian   | Old Javanese (Kawi)         | from 8th c. CE       | *(not coded)*  |
    # |                | Classical Malay             | from 7th c. CE onward| *(not coded)*  |
    # | Tai–Kadai      | Old Thai                    | from 13th c. CE      | *(not coded)*  |
}
```

</details>
<!-- PIPELINES:GENAI:END -->


## User-Defined Pipelines

See [User-Defined Pipelines](user-defined-pipelines.md) for documentation on how to create a custom `Pipeline`.
