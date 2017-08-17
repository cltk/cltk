#encoding: utf-8
import re
from cltk.tokenize.word import WordTokenizer

def normalize(text):
#normalise apostrophes
    text = re.sub(r"’", "'", text)
# make string lower-case
    text = text.lower()
    """Normalize each word of the French text."""

    normalized_text = ''

    word_tokenizer = WordTokenizer('french')
    tokenized_text = word_tokenizer.tokenize(text)

    for word in tokenized_text:
            # remove the simple endings from the target word
        word, was_normalized = matchremove_endings(word)
        # if word didn't match the s
            # imple endings, try verb endings
       # if not was_normalized:
       #     word = match_substitute_others(word)
        # add the stemmed word to the text
        normalized_text += word + ' '
    return normalized_text

#anglo-french variants normalised to "orthographe commune"

#word-final d - e.g. vertud vs vertu

def matchremove_endings(word):

    was_normalized = False

    final_consonants = [r'd']

    for ending in final_consonants:

        if word.endswith(ending):
            word = re.sub(r'{0}$'.format(ending), '', word)
            was_normalized = True
            break

    return word, was_normalized

def match_substitute_others(word):

    alterations = [("eaus$", "eus$"),
                   ("ceaus$", "ceus$"),
                   ("iu", "ieu"),
                   ("(^$)u(^$)", "\weu\w"),
                   ("ie\b", "iee\b"),
                   ("ue\b", "uee\b"),
                   ("ure\b", "eure\b"),
                   ("eo\b", "o\b"),
                   ("iw\b", "ieux\b"),
                   ("ew\b", "ieux\b"),
                   (r"a$", "e"),
                   ("^en", "^an")]


    for initial, later in alterations:
        for alteration in alterations:
            if initial in word:
                word = re.sub(initial, later, word)
                break
    return word

word = "ceaus"

c = match_substitute_others(word)
print(c)

alterations = [("eaus$", "eus"),
                ("ceaus$", "ceus"),
                ("iu", "ieu"),
                #("u", "eu"),
                ("ie", "iee"),
                ("ue", "uee"),
                ("ure$", "eure"),
                ("eo", "o"),
                (r"iw$", "ieux"),
                (r"ew$", "ieux"),
                (r"a$", "e")]

for initial, changed in alterations:
    for alteration in alterations:
        word = re.sub(initial, changed, word)
        break
print(word)


#use of <u> over <ou>

# persistance de <ei>

# <eaus> for <eus>, <ceaus? for <ceus>

#triphtongs:
# <iu> for <ieu>
# <u> for <eu>
# <ie> for <iee>
# <ue> for <uee>
# <ure> for <eure>

#"epenthetic vowels" - averai

# <eo> for <o>
# <iw>, <ew> for <ieux>

#final <a> for <e>
