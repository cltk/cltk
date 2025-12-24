"""Functional end-to-end check for CLTK NLP pipeline."""

import pickle

from cltk import NLP
from cltk.languages.example_texts import get_example_text
from cltk.utils.file_outputs import format_readers_guide

lang_code = "anci1242"
text = get_example_text(lang_code)
# print(text)
# input()
# text = text[:77]  # first colon
text = text[:642]  # first four sentences
print("Text:", text)
nlp = NLP(language_code=lang_code, backend="openai")
doc = nlp.analyze(text)
print(doc.sentences[0])
# input()

# pickle_file: str = f"scripts/temp_{lang_code}_doc.pkl"
# with open(pickle_file, "wb") as f:
#     pickle.dump(doc, f)
# print("Pickle file written to:", pickle_file)

md: str = format_readers_guide(doc=doc)

md_file: str = "scripts/example_greek_readers_guide.md"
with open(md_file, "w") as f:
    f.write(md)
print("Readers' guide written to:", md_file)
