#encoding : utf-8
import re

text = "Pendre m'otroi ou essiller sui es"

text = text.lower()

#reduced forms

text = re.sub(r"n'", "ne ", text)
text = re.sub(r"s'", "si ", text)
text = re.sub(r"t'", "te ", text)
text = re.sub(r"qu'", "que ", text)
# l' can stand for la or lui or le
text = re.sub(r"l'", "lui ", text)
text = re.sub(r"m'", "me ", text)



#NOUNS : regular grammatical forms

# e.g. "mur" (Brunot & Bruneau, 1949 :192)
text = re.sub(r"\Bs\b", "", text)
# e.g. "none" (Einhorn, 1975: 15)
text = re.sub(r"ain\b", "", text)
text = re.sub(r"ains\b", "", text)
# e.g. "baron" (Einhorn, 1975: 15)
text = re.sub(r"aron\b", r"er", text)
text = re.sub(r"arons\b", r"er", text)

#VERBS : regular grammatical forms
#être
#indic
text = re.sub(r"\bsui\b|\bies\b|\bes\b|\best\b|\bsons\b|\bsomes\b|\bestes\b|\bsont\b", "être", text)
#subj
text = re.sub(r"\bseie\b|\bsoie\b|\bseies\b|\bsoies\b|\bseiet\b|\bseit\b|\bsoit\b|")
#infinitive
text = re.sub(r"er\b", "", text)
# indicative - 2s, 3s, 1pl, 2pl, 3pl
text = re.sub(r"\Bes\b", "", text) # problematic - text = re.sub(r"e\b", "", text)
text = re.sub(r"ons\b", "", text)
text = re.sub(r"ez\b", "", text)
text = re.sub(r"eiz\b", "", text)
text = re.sub(r"ent\b", "", text)



print(text)