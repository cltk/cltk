"""Convert a word from Greek orthography into its hypothesized 
pronunciation in the International Phonetic Alphabet (IPA).

https://raw.githubusercontent.com/j-duff/cltk/ipa/
cltk/phonology/greek/transcription.py
"""

from cltk.utils.cltk_logger import logger

from nltk.tokenize import wordpunct_tokenize

import re
import unicodedata

try:
    # James Tauber's greek_accentuation package
    from greek_accentuation import characters as chars
except ImportError as import_error:
    print('Missing "greek_accentuation" package. Install with '  
        + '`pip install greek-accentuation`.')
    logger.error(import_error)
    raise

__author__ = 'Jack Duff <jmunroeduff@gmail.com>'
__license__ = 'MIT License. See LICENSE.'


# Dictionaries of phonological reconstructions for use in transcribing.
# Probert, Philomen. 2010. Phonology, in E. Bakker, A Companion to the \
# Ancient Greek Language.
# (Entries which are commented out are realized through diacritic analysis.)

GREEK = {
    'Attic': {
        'Probert': {
            'correspondence': {
                'α': 'ɑ',
                # 'ᾱ' : 'ɑː',
                'β': 'b',
                'γ': 'g',
                'δ': 'd',
                'ε': 'e',
                'ζ': 'sd',
                'η': 'ɛː',
                'θ': 'tʰ',
                'ι': 'i',
                # 'ῑ' : 'iː',
                'κ': 'k',
                'λ': 'l',
                'μ': 'm',
                'ν': 'n',
                'ξ': 'ks',
                'ο': 'o',
                'π': 'p',
                'ρ': 'r',
                'σ': 's',
                'ς': 's',
                'τ': 't',
                'υ': 'y',
                # 'ῡ' : 'yː',
                'φ': 'pʰ',
                'χ': 'kʰ',
                'ψ': 'ps',
                'ω': 'ɔː',
                'αι': 'ɑj',
                # 'ᾱι' : 'ɑːj',
                # 'ᾳ' : 'ɑːj',
                'ει': 'ẹː',
                'ηι': 'ɛːj',
                # 'ῃ' : 'ɛːj',
                'οι': 'oj',
                'ωι': 'ɔːj',
                # 'ῳ' : 'ɔːj',
                'υι': 'yj',
                'αυ': 'ɑw',
                'ευ': 'ew',
                'ηυ': 'ɛːw',
                'ου': 'ọː'
            },
            'diphthongs': [ 
            # and digraphs
                'αι', 'ει', 'ηι', 'οι', 'ωι', 'υι', 
                'αυ', 'ευ', 'ηυ', 'ου'
            ],
            'punctuation': [
                '.', ',', '·', '•', ':', '!', ';', "(", ")", 
                "[", "]", "'", '᾽', "\""
            ],     
            # Should the h value generated by the diacritic analysis
            # be moved to the front of possible diphthongs?
            'front_h': True,
            # Should iota subscripts be pronounced as diphthongs 
            # or simply ignored?
            # (dependent on Greek reconstruction)
            'pronounce_iota_sub': True,
            # What contextual pronunciation rules apply?
            'alternations': [
                'r_devoice',
                's_voice_assimilation',
                'nasal_place_assimilation',
                'g_nasality_assimilation'
            ]
        }
    }
}

# All IPA characters used sorted by natural classes.
# WILL NEED ADDITIONS AS MORE RECONSTRUCTIONS USED

IPA = {'voiced':  # [+voice]
           ['b', 'd', 'g',
            'm', 'n', 'ŋ'
            'l', 'r', 'z'],
       'labial':  # [+labial]
           ['b', 'p', 'pʰ', 'm'],
       'coronal':  # [+coronal]
           ['d', 't', 'tʰ', 'n', 's', 'z', 'r', 'r̥', 'l'],
       'velar':  # [+velar]
           ['g', 'k', 'kʰ', 'ŋ'],
       'nasal':  # [+nasal]
           ['m', 'n', 'ŋ'],
       'approximant':  # [+approximant]
           ['l', 'r', 'r̥', 'j', 'w'],
       'continuant':  # [+continuant, +consonantal]
           ['h', 's', 'z', 'l', 'r', 'r̥'],
       'vowel':  # [-consonantal -approximant]
           ['ɑ', 'ɑː', 'e', 'ẹː', 'ɛː', 'i', 'iː', 
           'o', 'ọː', 'y', 'yː', 'ɔː'],
       'high':  # [-consonantal, +high]
           ['i', 'iː', 'y', 'yː'],
       'low':  # [-consonantal, +low]
           ['ɑ', 'ɛː', 'ɔː', 'ɑː'],
       'front':  # [-consonantal, +front]
           ['i', 'iː', 'y', 'yː', 'e', 'ẹː', 'ɛː'],
       'back':  # [-consonantal, +back]
           ['o', 'ọː', 'ɑ', 'ɑː', 'ɔː'],
       'boundary':
           ['#']}

class Phone:
    'A phonological unit to be manipulated and represented as an IPA string.'

    # Has a bundle of feature values that help classify it so that it can
    # trigger contextual pronunciation changes.

    def __init__(self, ipa_ch):

        # Additions to greek_accentuation.characters for use in this class:
        IPA_CIRCUMFLEX = "\u0302"  # ˆ, the IPA tonal notation for ῀
        tones = chars.extract_diacritic(chars.ACUTE, IPA_CIRCUMFLEX)  
        # Collects IPA tonal diacritics
        clear_tones = chars.remove_diacritic(chars.ACUTE, IPA_CIRCUMFLEX)  
        # Clears IPA tonal diacritics

        # eventually exported to output string
        self.ipa = unicodedata.normalize('NFC', ipa_ch)
        # without IPA diacritics
        self.bare = unicodedata.normalize('NFC', clear_tones(ipa_ch))
        # selects the IPA diacritics  
        self.tone = tones(ipa_ch) 
        # will be assigned once in Word, as the pre-context of this phone 
        self.left = ""  
        # .... as the post-context of this phone
        self.right = ""  

        # bundle of features, stored as booleans:
        self.vce = self.bare in IPA['voiced']
        self.lab = self.bare in IPA['labial']
        self.cor = self.bare in IPA['coronal']
        self.vel = self.bare in IPA['velar']
        self.nas = self.bare in IPA['nasal']
        self.app = self.bare in IPA['approximant']
        self.cont = self.bare in IPA['continuant']
        self.vow = self.bare in IPA['vowel']
        self.hi = self.bare in IPA['high']
        self.lo = self.bare in IPA['low']
        self.fr = self.bare in IPA['front']
        self.bk = self.bare in IPA['back']
        self.bound = self.bare in IPA['boundary']


class Word:
    'Max. phonological unit, contains phones and triggers alternations.'

    # An ordered collection of Phones, 
    # which are bundles of features/IPA strings.

    def __init__(self, ipa_str, root):
        self.string = unicodedata.normalize('NFC', ipa_str)
        # Appropriate directory in the reconstruction dictionary
        self.root = root  
        # list of contextual pronunciation alternations
        self.alts = self.root['alternations']

        # Turns string of IPA characters into list of Phones
        self.phones = [Phone(c) for c in 
            re.findall(r'.[̥́̂ʰ]?ː?', self.string)]

    def _refresh(self):
        # Assigns left and right contexts for every phone
        for n in range(len(self.phones)):
            p = self.phones[n]
            if n != 0:
                p.left = self.phones[n - 1]
            else:
                p.left = Phone("#")
            if n != len(self.phones) - 1:
                p.right = self.phones[n + 1]
            else:
                p.right = Phone("#")

    def _r_devoice(self):
        # Pronounce r as voiceless word-init or after another r.
        out_phones = self.phones
        target = Phone("r̥")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.left.bound and p.ipa == "r":
                out_phones[n] = target
            if p.left.ipa == "r" and p.ipa == "r":
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _s_voice_assimilation(self):
        # Pronounce s as voiced (z) when followed by voiced.
        out_phones = self.phones
        target = Phone("z")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa == "s" and p.right.vce:
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _nasal_place_assimilation(self):
        # Pronounce nasals/g as velar nasals when followed by velar.
        out_phones = self.phones
        target = Phone("ŋ")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if (p.nas or p.ipa == 'g') and p.right.vel:
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    def _g_nasality_assimilation(self):
        # Pronounce g as (velar) nasal when followed by nasal.
        out_phones = self.phones
        target = Phone("ŋ")
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.ipa == "g" and p.right.nas:
                out_phones[n] = target
        self.phones = out_phones
        self._refresh()

    # list of all possible alternations
    ALTERNATIONS = [('r_devoice', _r_devoice),
                    ('s_voice_assimilation', _s_voice_assimilation),
                    ('nasal_place_assimilation', _nasal_place_assimilation),
                    ('g_nasality_assimilation', _g_nasality_assimilation)]

    def _alternate(self):
        self._refresh()
        # runs all alternations
        for a in Word.ALTERNATIONS:
            if a[0] in self.alts:
                a[1](self)

    def _syllabify(self):
        nuclei = []
        for n in range(len(self.phones)):
            p = self.phones[n]
            if p.vow:
                nuclei.append(n)
        # initialize syllables with a tuple for the first syllable
        # where onset is everything before the first nucleus
        # and coda remains unknown.
        syllables = [[self.phones[0:nuclei[0]], 
            [self.phones[nuclei[0]]], []]]
        # continue for every nucleus, assuming that everything between
        # the previous nucleus and it is the onset.
        for x in range(len(nuclei)-1):
            i = nuclei[x+1]
            onset = self.phones[nuclei[x]+1:i]
            nucleus = [self.phones[i]]
            syllables.append([onset, nucleus, []])
        # assume that everything after the final nucleus is final coda.   
        syllables[-1][2] = self.phones[nuclei[-1]+1:]
        # now go through and check onset viability
        for x in range(len(syllables)-1):
            onset = syllables[x+1][0]
            nucleus = syllables[x+1][1]
            coda = syllables[x+1][2]
            # trim all onsets greater than the maximum 2 phones
            # removing extra phones from the left
            # and appending them to the previous coda
            if len(onset) > 2:
                trim = onset[:-2]
                del onset[:-2] 
                syllables[x][2] = trim
            # once onset is 2 phones...
            if len(onset) == 2:
                # voiceless oral stop + nasal or liquid 
                # is a viable sequence, and passes
                if ((not onset[0].cont) and (not onset[0].vce)
                        and (not onset[0].app) and (not onset[0].nas) 
                        and (onset[1].nas or onset[1].app)):
                    break
                # voiced stop + liquid is also a viable sequence, and passes
                elif (not onset[0].cont) and onset[1].app:
                    break
                # otherwise, onset must be right Phone only
                # the left phone is appended to the previous coda
                else:
                    trim = onset[0]
                    del onset[0]
                    syllables[x][2] += [trim]
        self.syllables = syllables  
        return(syllables)

    def _print_ipa(self, syllabify):
        out = ""
        # if syllabification flag is present
        # print IPA by syllable segment
        if syllabify:
            syllables = self._syllabify()
            # ultima is final syllable
            ultima = syllables[-1]
            for s in syllables:
                for n in s:
                    for p in n:
                        out += p.ipa
                # after every non-final syllable
                # print IPA syll punctuation: '.' 
                if s != ultima:
                    out += "."     
        # otherwise print unsyllabified IPA       
        else:
            for p in self.phones:
                out += p.ipa
        return out


class Transcriber:
    'Uses a reconstruction to transcribe a orthographic string into IPA.'

    def __init__(self, dialect, reconstruction):
        self.lect = dialect
        self.recon = reconstruction
        self.root = GREEK[self.lect][self.recon]
        self.table = self.root["correspondence"]
        self.diphs = self.root["diphthongs"]
        self.punc = self.root["punctuation"]
        self.h = self.root["front_h"]
        self.i = self.root["pronounce_iota_sub"]

    def _parse_diacritics(self, ch):
        # Returns a string with seperated and organized diacritics
        # for easier access later.
        # EG: input with base α -> α/ACCENT/ETC/
        # (where ETC includes diaeresis, iota subscripts, and macrons)

        # Additions to greek_accentuation.characters for use here:
        marked_breathing = chars.extract_diacritic(chars.ROUGH)  
        # (Don't need SMOOTH for these purposes)
        marked_accents = chars.extract_diacritic(
            chars.ACUTE, chars.CIRCUMFLEX
        )  
        # (Don't need GRAVE for these purposes)
        marked_length = chars.extract_diacritic(chars.LONG)  
        # (Don't need SHORT for these purposes)

        h = marked_breathing(ch)
        acc = marked_accents(ch)
        etc = [
        chars.diaeresis(ch), chars.iota_subscript(ch), marked_length(ch)
        ]

        out = chars.base(ch).lower()  # Initialize out as base of character.

        if h != None and out != "ρ":  # If any rough breathing, and not rho
            out = "h///" + out  # insert an h/// before the base.
            # ('aspirated' rhos can be ignored,
            # and dealt with seperately.)

        out += "/"  # Create 1st boundary

        if acc != None:  # If any accent, place between 1st and 2nd boundary
            out += acc

        out += "/"  # Create 2nd boundary

        for c in [c for c in etc if c != None]:  # If any other diacritics, 
            out += c  # place between second and final boundary

        out += "/"  # Create final boundary

        return out

    def _prep_text(self, text):
        # Performs preperatory tasks grouping and reordering characters
        # in order to make transcription formulaic.

        string_in = "".join([self._parse_diacritics(ch) for ch in text])
        diph1 = "".join(list(set([d[0] for d in self.diphs])))  
        # (list of all acceptable first chars in diphthongs)
        diph2 = "".join(list(set([d[1] for d in self.diphs])))  
        # (list of all acceptable second chars in diphthongs)

        if self.h:
            # Locates acceptable diphthongs and treats them as single base
            # Combines all diacritics accordingly
            # Also finds any h's stranded in media diphthong (\3) and moves
            # them to the left edge
            pattern = (r"([" + diph1 + r"])\/\/([̄]?\/)(h///)?([" + diph2 
                + r"]\/[́͂]?\/)\/")
            diphshift = re.sub(pattern, r"\3\1\4\2", string_in)
        else:
            # Same as above, minus h-moving
            pattern = (r"([" + diph1 + r"])\/\/([̄]?\/)([" + diph2 
                + r"]\/[́͂]?\/)\/")
            diphshift = re.sub(pattern, r"\1\3\2", string_in)
        if self.i:
            # Locates iota subscripts and treats as base + iota diphthongs
            # Adds macron, since iota subscripts only appear on long vowels
            # (and we need to use all clues to identify long vowels)
            iotashift = re.sub(
                r"([αηω])(\/[́͂]*\/[̄¨]*)ͅ([̄¨]*\/)", r"\1ι\2̄\3", diphshift
            )
        else:
            # Same as above, but deletes iota entirely: only adds macrons
            iotashift = re.sub(
                r"([αηω])(\/[́͂]*\/[̄¨]*)ͅ([̄¨]*\/)", r"\1\2̄\3", diphshift
            )
        tup_out = re.findall(r"(..?)\/([́͂]*)\/([̄¨]*)\/", iotashift)
        return tup_out

    def transcribe(self, text, accentuate=True, syllabify=True):
        # input is word-tokenized, stripped of non-diacritic punctuation, 
        # and diphthongs and diacritics are handled
        inp = [self._prep_text(w) for w in wordpunct_tokenize(text) 
            if w not in self.punc]
        words = []
        for w in inp:
            out = ""
            for c in w:
                ipa = self.table.get(c[0], c[0])
                # if there are macrons in the diacritics, adds the ipa 
                # notation for length (if it isn't there already)
                if chars.LONG in c[2]:
                    if "ː" not in ipa:
                        ipa = ipa[0] + "ː" + ipa[1:]
                if accentuate:
                    # adds proper IPA notation for accents
                    # if circumflex accent, adds appropriate 
                    # ipa tone contour notation
                    if chars.CIRCUMFLEX in c[1]:
                        ipa = ipa[0] + "̂" + ipa[1:]
                    # if acute accent, adds appropriate 
                    # ipa tone contour notation
                    if chars.ACUTE in c[1]:
                        if len(ipa) > 1:
                            ipa = ipa[0] + "́" + ipa[1:]
                        else:
                            ipa += "́"
                out += ipa
            transcription = Word(out, self.root)
            transcription._alternate()
            words.append(transcription)
        # Encloses output in brackets, proper notation for surface form.
        return "[" + " ".join([w._print_ipa(syllabify) for w in words]) + "]"

if __name__ == '__main__':
    blackwell_transcriber = Transcriber("Attic", "Probert")
    example = blackwell_transcriber.transcribe("δέκατον μὲν ἔτος τόδ᾽ ἐπεὶ "
        + "Πριάμου μέγας ἀντίδικος, Μενέλαος ἄναξ ἠδ᾽ Ἀγαμέμνων, διθρόνου " 
        + "Διόθεν καὶ δισκήπτρου τιμῆς ὀχυρὸν ζεῦγος Ἀτρειδᾶν στόλον Ἀργείων"
        + " χιλιοναύτην, τῆσδ᾽ ἀπὸ χώρας")
    print(example)
