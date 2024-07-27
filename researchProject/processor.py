# Parker Holland
# Phaistos Disc Project
# Declaration of processor function and calling of it
# Uses cltk, Fran did most of this

def greekToScansion(file_path):
    from phaistos.src.cltk.prosody.grc import Scansion
    from phaistos import NLP

    scanner = Scansion()
    with open(file_path, 'r', encoding="utf8") as file:
        file_content = file.read()

    cltk_nlp = NLP(language="grc")
    cltk_doc = cltk_nlp.analyze(file_content)
    tokens = cltk_doc.tokens
    clean_accents = Scansion()._clean_accents(tokens)
    syllables = Scansion()._make_syllables(clean_accents)
    condensed = Scansion()._syllable_condenser(syllables)
    scanned = Scansion()._scansion(condensed)
    return scanned
    #return scanner.scan_text(file_content)

print(greekToScansion("texts/shortTheogeny.txt"))