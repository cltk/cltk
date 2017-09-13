"""Test cltk.prosody.latin Scanner modules."""

__license__ = 'MIT License. See LICENSE.'

import unittest

from cltk.prosody.latin.HexameterScanner import HexameterScanner
from cltk.prosody.latin.PentameterScanner import PentameterScanner
from cltk.prosody.latin.HendecasyllableScanner import HendecasyllableScanner
from cltk.prosody.latin.Syllabifier import Syllabifier

class TestScansionFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_hexameter_scanner(self):
        scanner = HexameterScanner()
        # Some lines will scan without any macrons being provided
        original_line = "impulerit. Tantaene animis caelestibus irae?"
        verse = scanner.scan(original_line)
        self.assertEqual(verse.scansion, '-  U U -    -   -   U U -    - -  U U  -  - ')
        self.assertEqual(verse.meter, "hexameter")
        self.assertEqual(verse.syllable_count, 15)
        self.assertTrue(verse.valid)
        self.assertTrue(verse)
        self.assertEqual(verse.accented, 'īmpulerīt. Tāntaene animīs caelēstibus īrae?')
        self.assertEqual(verse.original, original_line)
        self.assertEqual(repr(verse),
                         "Verse(original='impulerit. Tantaene animis caelestibus irae?', scansion='-  U U -    -   -   U U -    - -  U U  -  - ', meter='hexameter', valid=True, syllable_count=15, accented='īmpulerīt. Tāntaene animīs caelēstibus īrae?', scansion_notes=['Valid by positional stresses.'], syllables = ['īm', 'pu', 'le', 'rīt', 'Tān', 'taen', 'a', 'ni', 'mīs', 'cae', 'lēs', 'ti', 'bus', 'i', 'rae'])")
        # the items of a Verse object may be iterated on
        count = 0
        for idx, val in enumerate(verse):
            count += 1  # one might want to print or process the sequence here...
        self.assertEqual(count, 8)
        # if you give the scanner too little it will return invalid
        self.assertFalse(scanner.scan('pauca verba').valid)
        # same if too many syllables
        self.assertFalse(
            scanner.scan('o multa verba versum hexameterum non facit hodie! visne?').valid)

    def test_pentameter_scanner(self):
        scanner = PentameterScanner()
        # pentameters taken from the pentameter sections of the elegiac couplets of Catullus 76

        # Some lines will scan without any macrons being provided
        original_line = 'ex hoc ingrato gaudia amore tibi.'
        verse = scanner.scan(original_line)
        self.assertTrue(verse.valid)
        self.assertTrue(verse)
        self.assertEqual(verse.original, original_line)
        self.assertEqual(verse.meter, "pentameter")
        self.assertEqual(verse.syllable_count, 12)
        self.assertEqual(repr(verse),
                         "Verse(original='ex hoc ingrato gaudia amore tibi.', scansion='-   -  -   - -   - U  U - U  U U ', meter='pentameter', valid=True, syllable_count=12, accented='ēx hōc īngrātō gaudia amōre tibi.', scansion_notes=['Spondaic pentameter'], syllables = ['ēx', 'hoc', 'īn', 'gra', 'to', 'gau', 'di', 'a', 'mo', 're', 'ti', 'bi'])")
        self.assertEqual(verse.accented, 'ēx hōc īngrātō gaudia amōre tibi.')

        # Note: if a verse will not scan without judicious macrons, then it return as not valid
        verse = scanner.scan("est homini, cum se cogitat esse pium,")
        self.assertFalse(verse.valid)
        # with the correct macrons, the same line will be valid:
        verse = scanner.scan("est hominī, cum sē cōgitat esse pium,")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.scansion, '-    U U -   -   -  - U U  -  U  UU  ')
        self.assertEqual(verse.accented, 'ēst hominī, cūm sē cōgitat ēsse pium,')

        verse = scanner.scan("divum ad fallendos numine abusum hominēs,")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'dīvum ād fāllēndōs nūmine abūsum hominēs,')

        verse = scanner.scan("aut facere, haec ā tē dictaque factaque sunt.")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'aut facere, haec ā tē dīctaque fāctaque sūnt.')

        verse = scanner.scan("et dis invitis desinis esse miser?")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'ēt dīs īnvītīs dēsinis ēsse miser?')

        verse = scanner.scan("difficile est, vērum hoc quā lubet efficiās:")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'dīfficile ēst, vērum hōc quā lubet ēfficiās:')

        # again, a minor accentuation allows for the line to scan properly
        verse = scanner.scan("quārē iam te cur amplius excruciēs?")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'quārē iām tē cūr āmplius ēxcruciēs?')

        verse = scanner.scan("hoc facias, sīve id non pote sīve pote.")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'hōc faciās, sīve īd nōn pote sīve pote.')

        verse = scanner.scan("extremam iam ipsa in morte tulistis opem,")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'ēxtrēmām iam īpsa īn mōrte tulīstis opem,')

        verse = scanner.scan("eripite hanc pestem perniciemque mihi,")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'ēripite hānc pēstēm pērniciēmque mihi,')

        # this is a good example, one accented vowel coerced the line to scan properly, omnī
        verse = scanner.scan("expulit ex omnī pectore laetitiās.")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'ēxpulit ēx ōmnī pēctore laetitiās.')

        verse = scanner.scan("aut, quod non potis est, esse pudica velit:")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'aut, quōd nōn potis ēst, ēsse pudīca velit:')
        # if you give the scanner too little it will return invalid
        self.assertFalse(scanner.scan('pauca verba').valid)
        # same if too many syllables
        self.assertFalse(
            scanner.scan('o multa verba versum hexameterum non facit hodie! visne?').valid)

    def test_hendecasyllable_scanner(self):
        scanner = HendecasyllableScanner()
        # Hendecasyllable verses taken from Catullus 1

        # Some lines will scan without any macrons being provided
        original_line = "Iam tum, cum ausus es unus Italorum"
        verse = scanner.scan(original_line)
        self.assertTrue(verse.valid)
        self.assertTrue(verse)
        self.assertEqual(verse.original, original_line)
        self.assertEqual(verse.meter, "hendecasyllable")
        self.assertEqual(verse.syllable_count, 11)
        self.assertEqual(verse.accented, 'Iām tūm, cum ausus es ūnus Ītalōrum')
        self.assertEqual(repr(verse),
                         "Verse(original='Iam tum, cum ausus es unus Italorum', scansion=' -   -        - U  U  - U  - U - U ', meter='hendecasyllable', valid=True, syllable_count=11, accented='Iām tūm, cum ausus es ūnus Ītalōrum', scansion_notes=['antepenult foot onward normalized.'], syllables = ['Jām', 'tūm', 'c', 'au', 'sus', 'es', 'u', 'nus', 'I', 'ta', 'lo', 'rum'])")

        # Note: if a verse will not scan without a judicious macron, then it return as not valid
        verse = scanner.scan("meas esse aliquid putare nugas.")
        self.assertEqual(verse.scansion, ' UU  -    U U  -   U - U  - U  ')
        self.assertFalse(verse.valid)
        # Submitted with the proper minimal macrons necessary, the verse will scan valid.
        verse = scanner.scan("meās esse aliquid putare nugas.")
        self.assertEqual(verse.scansion, ' U-  -    U U  -   U - U  - U  ')
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'meās ēsse aliquīd putāre nūgas.')
        # another example:
        verse = scanner.scan("arida modo pumice expolitum?")
        self.assertFalse(verse.valid)
        self.assertEqual(verse.accented, 'aridā modo pūmice ēxpolītum?')
        self.assertEqual(verse.scansion, 'U U -  U U  - U   -  U - U  ')
        # with the correct macronization
        verse = scanner.scan("ārida modo pumice expolitum?")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'āridā modo pūmice ēxpolītum?')
        self.assertEqual(verse.scansion, '- U -  U U  - U   -  U - U  ')

        # Usually only the final syllable may need a macron for grammatical correctness;
        # because in latin verse, the final syllable can often be optionally long or short,
        # the scanner classes (Hexameter, Hendecasyllable, Pentameter) do not attempt to
        # coerce that value; if it is given by the user, it will be used;
        # if it is positionally accented, then that value will be used.
        verse = scanner.scan("omne aevum tribus explicare cartis.")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'ōmne aevūm tribus ēxplicāre cārtis.')
        # users may desire a more precise version with the final syllable appropriately macronized:
        verse = scanner.scan("omne aevum tribus explicare cartīs.")
        self.assertTrue(verse.valid)

        verse = scanner.scan("Doctis, Iuppiter, et laboriosis!")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'Dōctīs, Iūppiter, ēt labōriōsis!')

        verse = scanner.scan("Quāre habe tibi quidquid hoc libelli—")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'Quāre habē tibi quīdquid hōc libēlli—')

        verse = scanner.scan("quālecumque, quod, o patrona virgo,")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'quālecūmque, quod, ō patrōna vīrgo,')

        # Note: due to the flexibility of the hendecasyllable pattern, it is possible for a line
        # to scan, and yield grammatically incorrect macronization, however, with a few
        # judicious macron placements, the line may also scan correctly
        verse = scanner.scan("Cui dono lepidum novum libellum")
        self.assertEqual(verse.scansion, '  -  U -  U U -   U -   U -  U ')
        self.assertTrue(verse.valid)
        # also valid with dōno macron:
        verse = scanner.scan("Cui dōno lepidum novum libellum")
        self.assertEqual(verse.scansion, '  -  - -  U U -   U -   U -  U ')
        self.assertTrue(verse.valid)

        verse = scanner.scan("Corneli, tibi: namque tu solebas")
        self.assertEqual(verse.scansion, ' -  U -   U U   -   U  -  U - U ')
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'Cōrnelī, tibi: nāmque tū solēbas')

        # if the e in Cornelius is long, it also scans
        verse = scanner.scan("Cornēli, tibi: namque tu solebās")
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'Cōrnēlī, tibi: nāmque tū solēbās')
        self.assertEqual(verse.scansion, ' -  - -   U U   -   U  -  U - - ')
        self.assertTrue(verse.valid)

        verse = scanner.scan("plūs uno maneat perenne saeclo!")
        self.assertEqual(verse.scansion, '  -  U -  U U-   U -  U   -  U ')
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'plūs unō maneāt perēnne saeclo!')
        # Note: that it would be preferrable to accent ūno as well
        verse = scanner.scan("plūs ūno maneat perenne saeclo!")
        self.assertEqual(verse.scansion, '  -  - -  U U-   U -  U   -  U ')
        self.assertTrue(verse.valid)
        self.assertEqual(verse.accented, 'plūs ūnō maneāt perēnne saeclo!')

        # if you give the scanner too little it will return invalid
        self.assertFalse(scanner.scan('pauca verba').valid)
        # same if too many syllables
        self.assertFalse(
            scanner.scan('o multa verba versum hexameterum non facit hodie! visne?').valid)

    def test_syllabifier(self):
        syllabifier = Syllabifier()
        # break a word into syllables
        self.assertEqual(syllabifier.syllabify("Bīthÿnus"), ['Bī', 'thÿ', 'nus'])
        # break a group of words into a group of syllables:
        self.assertEqual(syllabifier.syllabify("arbor pulcher ruptus"), [
            'ar', 'bor', 'pul', 'cher', 'ru', 'ptus'])
        # do not process character sets that have not been specified by the ScansionConstants class
        # that is injected into the constructor; a whole group is rejected when this occurs
        self.assertEqual(syllabifier.syllabify("Platonis Ψυχη"),['Platonis', 'Ψυχη'])
