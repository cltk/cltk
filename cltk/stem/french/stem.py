import re

text = "Pendre m'otroi ou essiller"

#reduced forms
text = re.sub(r"N'", "Ne ", text)
text = re.sub(r"n'", "ne ", text)

text = re.sub(r"S'", "Si ", text)
text = re.sub(r"s'", "si ", text)

text = re.sub(r"T'", "Te ", text)
text = re.sub(r"t'", "te ", text)

text = re.sub(r"Qu'", "Que ", text)
text = re.sub(r"qu'", "que ", text)

text = re.sub(r"L'", "Li ", text)
text = re.sub(r"L'", "li ", text)

#NOUNS : regular grammatical forms

# e.g. "mur" (Brunot & Bruneau, 1949 :192)
text = re.sub(r"s$", "", text)
# e.g. "none" (Einhorn, 1975: 15)
text = re.sub(r"ain", "", text)
text = re.sub(r"ains", "", text)
# e.g. "baron" (Einhorn, 1975: 15)
text = re.sub(r"aron", r"er", text)
text = re.sub(r"arons", r"er", text)