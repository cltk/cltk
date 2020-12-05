"""Module for calculating rhyme scheme for a MHG stanza."""

from cltk.alphabet.gmh import normalize_middle_high_german as normalizer
from cltk.phonology.gmh.transcription import Transcriber
from cltk.phonology.syllabify import Syllabifier

syllabifier = Syllabifier(language="gmh")


class Verse:
    """Calculate rhyme scheme for a MHG stanza."""

    def __init__(self, text):
        self.text = [
            normalizer(line, to_lower_all=True, punct=True, alpha_conv=True).split(" ")
            for line in text
        ]
        self.syllabified = [
            [syllabifier.syllabify(w) for w in line] for line in self.text
        ]
        self.transcribed_phonetics = None

    def to_phonetics(self):
        """Transcribe phonetics."""
        tr = Transcriber()
        self.transcribed_phonetics = [tr.transcribe(line) for line in self.text]

    def rhyme_scheme(self, rhyme_size=3):
        """
        Calculates the rhyme scheme of a given stanza. It doesn't yet support
        phonetical rhyming (homophones) and thus is still error-prone

        Example:
            >>> stanza = ['Ein rîchiu küneginne, frou Uote ir muoter hiez.', 'ir vater der hiez Dancrât, der in diu erbe liez', 'sît nâch sîme lebene, ein ellens rîcher man,', 'der ouch in sîner jugende grôzer êren vil gewan.']

            >>> S = Verse(stanza)

            >>> S.rhyme_scheme(2)
            'AABB'
        """
        rhymes = dict()
        i = 64
        strs = ""

        for line in self.syllabified:

            w = line[-1][-1][-rhyme_size:]

            for r in rhymes.keys():
                if r.endswith(w) or w.endswith(r):
                    rhymes[w] = rhymes[r]
                    break

            if w in rhymes:
                strs += rhymes[w]
            else:
                i += 1
                rhymes[w] = chr(i)
                strs += chr(i)

        return strs
