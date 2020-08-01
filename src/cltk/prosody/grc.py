"""
This program returns the prosimetric scansion of Greek texts.

A user is first prompted to supply the file path of the text they wish to scan.
Note that this text must be a relatively 'clean' text, as the opening function
(i.e., tokenize) will only remove numbers and all punctuation that is not a
period. The tokenizer will also force lower case on the text. The text will
then be tokenized and syllabified. Before the text undergoes the actual
scansion functions, the text will be re-tokenized into a simple list of words
and syllables. Finally, the simplified tokenized text will be scanned according
to typical Greek scansion rules. The details of these rules are delineated in
the docstrings of the specific scansion functions. The final output is the
resulting scansion.

.. warning::
    Known bug: Reduplicated syllables in a single sentence are not scanned separately.
"""

from typing import List

from cltk.core.cltk_logger import logger

__author__ = ["Tyler Kirby <tyler.kirby9398@gmail.com>"]
__license__ = "MIT License"


# noinspection PyProtectedMember
class Scansion:
    """Scans Greek texts that already contain macronized
    (i.e., long and shorts) texts.
    """

    def __init__(self) -> None:
        """Setup class variables."""
        self.vowels = ["ε", "ι", "ο", "α", "η", "ω", "υ", "ῖ", "ᾶ"]  # type: List[str]
        self.sing_cons = [
            "ς",
            "ρ",
            "τ",
            "θ",
            "π",
            "σ",
            "δ",
            "φ",
            "γ",
            "ξ",
            "κ",
            "λ",
            "χ",
            "β",
            "ν",
            "μ",
        ]  # type: List[str]
        self.doub_cons = ["ξ", "ζ", "ψ"]  # type: List[str]
        self.long_vowels = ["η", "ω", "ῖ", "ᾶ", "ῦ"]  # type: List[str]
        self.diphthongs = [
            "αι",
            "αῖ",
            "ευ",
            "εῦ",
            "αυ",
            "αῦ",
            "οι",
            "οῖ",
            "ου",
            "οῦ",
            "ει",
            "εῖ",
            "υι",
            "υῖ",
            "ηῦ",
        ]  # type: List[str]
        self.stops = ["π", "τ", "κ", "β", "δ", "γ"]  # type: List[str]
        self.liquids = ["ρ", "λ"]  # type: List[str]
        self.punc = [
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "=",
            "+",
            "}",
            "{",
            "[",
            "]",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
            ",",
            "'",
            "᾽",
            "（",
            "）",
        ]  # type: List[str]
        self.punc_stops = ["·", ":", ";"]  # type: List[str]

    def scan_text(self, input_string: str) -> List[str]:
        """The primary method for the class.

        Args:
            input_string: A string of macronized text.

        Returns:
            List representation of each word's long (``¯``) and short (``˘``) values.

        >>> from cltk.prosody.grc import Scansion
        >>> text_string = "νέος μὲν καὶ ἄπειρος, δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος."
        >>> Scansion().scan_text(text_string)
        ['˘¯¯¯˘¯¯˘¯˘¯˘˘x', '¯¯˘¯x']
        """
        syllables = self._make_syllables(input_string)
        sentence_syllables = self._syllable_condenser(syllables)
        meter = self._scansion(sentence_syllables)
        return meter

    def _clean_text(self, text: str) -> str:
        """Remove input text of extraneous (non-stop) punction (e.g., ``","``).
        By default, ``":"``, ``";"``, and ``"."`` are defined as stops.

        Args:
            text: Text string containing non-stop punctuation.

        Returns:
            Text with unnecessary punctuation removed

        >>> from cltk.prosody.grc import Scansion
        >>> not_clean = "νέος μὲν καὶ ἄπειρος, δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος."
        >>> Scansion()._clean_text(not_clean)
        'νέος μὲν καὶ ἄπειρος δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος.'
        """
        clean = list()  # type: List[str]
        for char in text:
            if char in self.punc_stops:
                clean += "."
            elif char not in self.punc:
                clean += char
            else:
                pass
        return ("".join(clean)).lower()

    def _clean_accents(self, text: str) -> str:
        """Remove most accent marks. This the circumflexes
        over alphas and iotas in the text since they mark
        vocalic quantity.

        Args:
            text: Text string with accents.

        Returns:
            Text string with only accents required for processing.

        >>> from cltk.prosody.grc import Scansion
        >>> unclean_accents = "νέος μὲν καὶ ἄπειρος, δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος."
        >>> Scansion()._clean_accents(unclean_accents)
        'νεος μεν και απειρος δικων εγωγε ετι. μεν και απειρος.'
        """
        accents = {
            "ὲέἐἑἒἓἕἔ": "ε",
            "ὺύὑὐὒὓὔὕ": "υ",
            "ὸόὀὁὂὃὄὅ": "ο",
            "ὶίἰἱἲἳἵἴ": "ι",
            "ὰάἁἀἂἃἅἄᾳᾂᾃ": "α",
            "ὴήἠἡἢἣἥἤἧἦῆῄῂῇῃᾓᾒᾗᾖᾑᾐ": "η",
            "ὼώὠὡὢὣὤὥὦὧῶῲῴῷῳᾧᾦᾢᾣᾡᾠ": "ω",
            "ἶἷ": "ῖ",
            "ἆἇᾷᾆᾇ": "ᾶ",
            "ὖὗ": "ῦ",
        }
        text = self._clean_text(text)
        for char in text:
            for key in accents:
                if char in key:
                    accent = accents.get(key)
                    if accent:
                        text = text.replace(char, accent)
                else:
                    pass
        return text

    def _tokenize(self, text: str) -> List[List[str]]:
        """Tokenize the text into a list of sentences with a list of words.

        Args:
            text: Text string

        Returns:
            List of words within a list of sentences

        >>> from cltk.prosody.grc import Scansion
        >>> not_tokenized = "νέος μὲν καὶ ἄπειρος, δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος."
        >>> Scansion()._tokenize(not_tokenized)
        [['νεος', 'μεν', 'και', 'απειρος', 'δικων', 'εγωγε', 'ετι.'], ['μεν', 'και', 'απειρος.']]
        """
        sentences = list()
        tokens = list()
        for word in self._clean_accents(text).split(" "):
            tokens.append(word)
            if "." in word:
                sentences.append(tokens)
                tokens = list()
        return sentences

    @staticmethod
    def _syllable_condenser(words_syllables: List[List[List[str]]]) -> List[List[str]]:
        """Reduce a list of ``[sentence[word[syllable]]]`` to ``[sentence[syllable]]``.

        Args:
            words_syllables: List of syllables

        Returns:
            List of words

        >>> from cltk.prosody.grc import Scansion
        >>> input_syllables = [[["νε", "ος"], ["μεν"], ["και"], ["α", "πει", "ρος"], ["δι", "κων"], ["ε", "γω", "γε"], ["ε", "τι"]], [["μεν"], ["και"], ["α", "πει", "ρος"]]]
        >>> Scansion()._syllable_condenser(input_syllables)
        [['νε', 'ος', 'μεν', 'και', 'α', 'πει', 'ρος', 'δι', 'κων', 'ε', 'γω', 'γε', 'ε', 'τι'], ['μεν', 'και', 'α', 'πει', 'ρος']]
        """
        sentences_syllables = list()
        for sentence in words_syllables:
            syllables_sentence = list()  # type: List[str]
            for word in sentence:
                syllables_sentence += word
            sentences_syllables.append(syllables_sentence)
        return sentences_syllables

    def _long_by_nature(self, syllable: str) -> bool:
        """Check if syllable is long by nature. Long by nature includes:

        1. Syllable contains a diphthong
        2. Syllable contains a long vowel

        Args:
            syllable: A syllable

        Returns:
            Whether or not input is long by nature.

        >>> from cltk.prosody.grc import Scansion
        >>> syllables = ["νε", "ος", "μεν", "και", "α", "πει", "ρος", "δι", "κων", "ε", "γω", "γε", "ε", "τι", "μεν", "και", "α", "πει", "ρος"]
        >>> [Scansion()._long_by_nature(syllable) for syllable in syllables]
        [False, False, False, True, False, True, False, False, True, False, True, False, False, False, False, True, False, True, False]
        """
        # Find diphthongs
        vowel_group = list()  # type: List[str]
        for char in syllable:
            if char in self.long_vowels:
                return True
            if char not in self.sing_cons and char not in self.doub_cons:
                vowel_group += char
        return bool("".join(vowel_group) in self.diphthongs)

    def _long_by_position(self, syllable: str, sentence: List[str]) -> bool:
        """Check if syllable is long by position. Returns ``True``
        if syllable is long by position Long by position
        includes contexts when:

        1. Next syllable begins with two consonants, unless those consonants are a stop + liquid combination
        2. Next syllable begins with a double consonant
        3. Syllable ends with a consonant and the next syllable begins with a consonant

        Args:
            syllable: Current syllable
            sentence: Sentence in which syllable appears

        Returns:
            Whether or not a syllable is long by position

        >>> from cltk.prosody.grc import Scansion
        >>> syllables_sentence = ["μεν", "και", "α", "πει", "ρος"]
        >>> [Scansion()._long_by_position(syllable=syllable, sentence=syllables_sentence) for syllable in syllables_sentence]
        [True, False, False, False, False]
        """
        try:
            next_syll = sentence[sentence.index(syllable) + 1]
            # Long by position by case 1
            if (next_syll[0] in self.sing_cons and next_syll[1] in self.sing_cons) and (
                next_syll[0] not in self.stops and next_syll[1] not in self.liquids
            ):
                return True
            # Long by position by case 2
            if syllable[-1] in self.vowels and next_syll[0] in self.doub_cons:
                return True
            # Long by position by case 3
            if syllable[-1] in self.sing_cons and (next_syll[0] in self.sing_cons):
                return True
        except IndexError:
            logger.info(
                "IndexError while checking if syllable '%s' is long. Continuing.",
                syllable,
            )
        return False

    def _scansion(self, sentence_syllables: List[List[str]]) -> List[str]:
        """Replace long and short values for each input syllable.

        Args:
            sentence_syllables: List of word tokens

        Returns:
            ``"˘"`` and ``"¯"`` to represent short and long syllables, respectively

        >>> from cltk.prosody.grc import Scansion
        >>> syllables_sentence = [["νε", "ος", "μεν", "και", "α", "πει", "ρος", "δι", "κων", "ε", "γω", "γε", "ε", "τι"], ["μεν", "και", "α", "πει", "ρος"]]
        >>> Scansion()._scansion(syllables_sentence)
        ['˘¯¯¯˘¯¯˘¯˘¯˘˘x', '¯¯˘¯x']
        """
        scanned_text = list()
        for sentence in sentence_syllables:
            scanned_sent = list()
            for syllable in sentence:
                if self._long_by_position(syllable, sentence) or self._long_by_nature(
                    syllable
                ):
                    scanned_sent.append("¯")
                else:
                    scanned_sent.append("˘")
            if len(scanned_sent) > 1:
                del scanned_sent[-1]
                scanned_sent.append("x")
            scanned_text.append("".join(scanned_sent))
        return scanned_text

    def _make_syllables(self, sentences_words: str) -> List[List[List[str]]]:
        """First tokenize, then divide word tokens into a list of syllables.
        Note that a syllable in this instance is defined as a vocalic
        group (i.e., vowel or a diphthong). This means that all
        syllables which are not the last syllable in the word
        will end with a vowel or diphthong.

        Todo:
            * Determine whether a CLTK syllabifier could replace this.

        Args:
            sentences_words: Text string

        Returns:
            List of list of list of syllables

        >>> from cltk.prosody.grc import Scansion
        >>> text_string = "νέος μὲν καὶ ἄπειρος, δικῶν ἔγωγε ἔτι. μὲν καὶ ἄπειρος."
        >>> Scansion()._make_syllables(text_string)
        [[['νε', 'ος'], ['μεν'], ['και'], ['α', 'πει', 'ρος'], ['δι', 'κων'], ['ε', 'γω', 'γε'], ['ε', 'τι']], [['μεν'], ['και'], ['α', 'πει', 'ρος']]]
        """
        text = self._tokenize(sentences_words)
        all_syllables = list()
        for sentence in text:
            syll_per_sent = list()
            for word in sentence:
                syll_start = 0  # Begins syllable iterator
                syll_per_word = list()
                cur_letter_in = 0  # Begins general iterator
                while cur_letter_in < len(word):
                    letter = word[cur_letter_in]
                    if (cur_letter_in != len(word) - 1) and (
                        word[cur_letter_in] + word[cur_letter_in + 1]
                    ) in self.diphthongs:
                        cur_letter_in += 1
                        # Syllable ends with a diphthong
                        syll_per_word.append(word[syll_start : cur_letter_in + 1])
                        syll_start = cur_letter_in + 1
                    elif (letter in self.vowels) or (letter in self.long_vowels):
                        # Syllable ends with a vowel
                        syll_per_word.append(word[syll_start : cur_letter_in + 1])
                        syll_start = cur_letter_in + 1
                    cur_letter_in += 1
                try:
                    last_vowel = syll_per_word[-1][-1]  # Last vowel of a word
                    # Modifies general iterator to accomodate consonants after
                    # the last syllable in a word
                    cur_letter_in = len(word) - 1
                    # Contains all of the consonants after the last vowel in a word
                    leftovers = ""
                    while word[cur_letter_in] != last_vowel:
                        if word[cur_letter_in] != ".":
                            # Adds consonants to leftovers
                            leftovers = word[cur_letter_in] + leftovers
                        cur_letter_in -= 1
                    # Adds leftovers to last syllable in a word
                    syll_per_word[-1] += leftovers
                    syll_per_sent.append(syll_per_word)
                except IndexError:
                    logger.info(
                        "IndexError while making syllables of '%s'. Continuing.", word
                    )
            all_syllables.append(syll_per_sent)
        return all_syllables
