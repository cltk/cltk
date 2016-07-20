from macronizer import Macronizer
import re

with open("test.txt") as file:
    book1Macrons = file.read()

with open("gall1.txt") as file:
    book1NoMacrons = file.read()

macronized = Macronizer("tag_ngram_123_backoff").macronize(book1NoMacrons)
macronized_words = []
for tag in macronized:
    macronized_words.append(tag[2])


def clean_text(text):
    return re.sub('[^a-zA-Z\sāēīōū]+', '', text)

actual = []
for word in clean_text(book1Macrons).split(" "):
    actual.append(word.lower())

print(actual)
print(macronized_words)