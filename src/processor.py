# Phaistos Disc Project
# Declaration of processor function and calling of it
# Uses cltk, Fran did most of this

def greekToScansion(file_path):
    from cltk.prosody.grc import Scansion
    from cltk import NLP
    import sys
    sys.path.append("cltk")

    scanner = Scansion()
    with open(file_path, 'r', encoding="utf8") as file:
        file_content = file.read()

    # https://github.com/cltk/cltk/issues/1247
    # Including this here just in case
    cltk_nlp = NLP(language="grc")
    cltk_doc = cltk_nlp.analyze(file_content)
    tokens = cltk_doc.tokens
    clean_accents = Scansion()._clean_accents(tokens)
    syllables = Scansion()._make_syllables(clean_accents)
    condensed = Scansion()._syllable_condenser(syllables)
    scanned = Scansion()._scansion(condensed)
    return scanned

print(greekToScansion("researchProject/texts/shortTheogeny.txt"))