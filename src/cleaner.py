# Phaistos Disc Project
# Dclaration of greekToSyllable function and calling of it
# Uses cltk

def greektoSyllables(file_path):
    from cltk.prosody.grc import Scansion
    from cltk import NLP
    import sys
    sys.path.append("cltk")

    scanner = Scansion()
    with open(file_path, 'r', encoding="utf8") as file:
        file_content = file.read()

    cltk_nlp = NLP(language="grc")
    cltk_doc = cltk_nlp.analyze(file_content)
    tokens = cltk_doc.tokens
    clean_accents = Scansion()._clean_accents(tokens)
    syllables = Scansion()._make_syllables(clean_accents)
    condensed = Scansion()._syllable_condenser(syllables)
    return condensed

print(greektoSyllables("researchProject/texts/shortTheogeny.txt"))