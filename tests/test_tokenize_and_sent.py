"""Test cltk.tokenize.

TODO: Mk different file for sentence tests.
"""

import unittest
from unittest.mock import patch

from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.data.fetch import FetchCorpus
from cltk.sentence.lat import LatinPunktSentenceTokenizer
from cltk.sentence.san import SanskritRegexSentenceTokenizer
from cltk.tokenizers.akk import AkkadianWordTokenizer
from cltk.tokenizers.arb import ArabicWordTokenizer
from cltk.tokenizers.enm import MiddleEnglishWordTokenizer
from cltk.tokenizers.fro import OldFrenchWordTokenizer
from cltk.tokenizers.gmh import MiddleHighGermanWordTokenizer
from cltk.tokenizers.lat.lat import LatinWordTokenizer
from cltk.tokenizers.lat.utils import LatinSentenceTokenizerTrainer
from cltk.tokenizers.line import LineTokenizer
from cltk.tokenizers.non import OldNorseWordTokenizer
from cltk.tokenizers.utils import SentenceTokenizerTrainer
from cltk.tokenizers.word import WordTokenizer


class TestSentenceTokenize(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    @classmethod
    def setUpClass(self):
        corpus_importer = FetchCorpus("grc")
        corpus_importer.import_corpus("grc_models_cltk")
        corpus_importer = FetchCorpus("lat")
        corpus_importer.import_corpus("lat_models_cltk")
        self.greek_text = """ὅλως δ’ ἀντεχόμενοί τινες, ὡς οἴονται, δικαίου τινός (ὁ γὰρ νόμος δίκαιόν τἰ τὴν κατὰ πόλεμον δουλείαν τιθέασι δικαίαν, ἅμα δ’ οὔ φασιν· τήν τε γὰρ ἀρχὴν ἐνδέχεται μὴ δικαίαν εἶναι τῶν πολέμων, καὶ τὸν ἀνάξιον δουλεύειν οὐδαμῶς ἂν φαίη τις δοῦλον εἶναι· εἰ δὲ μή, συμβήσεται τοὺς εὐγενεστάτους εἶναι δοκοῦντας δούλους εἶναι καὶ ἐκ δούλων, ἐὰν συμβῇ πραθῆναι ληφθέντας."""  # pylint: disable=line-too-long
        self.latin_text = "O di inmortales! ubinam gentium sumus? in qua urbe vivimus? quam rem publicam habemus? Hic, hic sunt in nostro numero, patres conscripti, in hoc orbis terrae sanctissimo gravissimoque consilio, qui de nostro omnium interitu, qui de huius urbis atque adeo de orbis terrarum exitio cogitent! Hos ego video consul et de re publica sententiam rogo et, quos ferro trucidari oportebat, eos nondum voce volnero! Fuisti igitur apud Laecam illa nocte, Catilina, distribuisti partes Italiae, statuisti, quo quemque proficisci placeret, delegisti, quos Romae relinqueres, quos tecum educeres, discripsisti urbis partes ad incendia, confirmasti te ipsum iam esse exiturum, dixisti paulum tibi esse etiam nunc morae, quod ego viverem."  # pylint: disable=line-too-long

    def test_sentence_tokenizer_latin_punkt(self):
        """Test tokenizing Latin sentences."""
        target = [
            "O di inmortales!",
            "ubinam gentium sumus?",
            "in qua urbe vivimus?",
            "quam rem publicam habemus?",
            "Hic, hic sunt in nostro numero, patres conscripti, in hoc orbis terrae sanctissimo gravissimoque consilio, qui de nostro omnium interitu, qui de huius urbis atque adeo de orbis terrarum exitio cogitent!",
            "Hos ego video consul et de re publica sententiam rogo et, quos ferro trucidari oportebat, eos nondum voce volnero!",
            "Fuisti igitur apud Laecam illa nocte, Catilina, distribuisti partes Italiae, statuisti, quo quemque proficisci placeret, delegisti, quos Romae relinqueres, quos tecum educeres, discripsisti urbis partes ad incendia, confirmasti te ipsum iam esse exiturum, dixisti paulum tibi esse etiam nunc morae, quod ego viverem.",
        ]  # pylint: disable=line-too-long
        tokenizer = LatinPunktSentenceTokenizer()
        tokenized_sentences = tokenizer.tokenize(self.latin_text)
        self.assertEqual(tokenized_sentences, target)

    def test_sentence_tokenizer_latin_punkt_strict(self):
        """Test tokenizing Latin sentences with stricter punctuation."""
        target = [
            "in principio creavit Deus caelum et terram;",
            "terra autem erat inanis et vacua et tenebrae super faciem abyssi et spiritus Dei ferebatur super aquas;",
            "dixitque Deus fiat lux et facta est lux;",
            "et vidit Deus lucem quod esset bona et divisit lucem ac tenebras.",
        ]  # pylint: disable=line-too-long
        tokenizer = LatinPunktSentenceTokenizer(strict=True)
        tokenized_sentences = tokenizer.tokenize(
            """in principio creavit Deus caelum et terram; terra autem erat inanis et vacua et tenebrae super faciem abyssi et spiritus Dei ferebatur super aquas; dixitque Deus fiat lux et facta est lux; et vidit Deus lucem quod esset bona et divisit lucem ac tenebras."""
        )
        self.assertEqual(tokenized_sentences, target)

    # TODO: KJ commented this out, re-enable
    # def test_sentence_tokenizer_latin_punkt_missing(self):
    #     """Test whether models are present"""
    #     with patch.object(LatinPunktSentenceTokenizer, 'models_path', ''):
    #         with self.assertRaises(FileNotFoundError):
    #             tokenizer = LatinPunktSentenceTokenizer()

    # # Simplify, just checking if/else really
    # def test_sentence_tokenizer_greek_regex_switch(self):
    #     """Test tokenizing Greek sentences with regex."""
    #     target = [
    #         'ὅλως δ’ ἀντεχόμενοί τινες, ὡς οἴονται, δικαίου τινός (ὁ γὰρ νόμος δίκαιόν τἰ τὴν κατὰ πόλεμον δουλείαν τιθέασι δικαίαν, ἅμα δ’ οὔ φασιν·',
    #         'τήν τε γὰρ ἀρχὴν ἐνδέχεται μὴ δικαίαν εἶναι τῶν πολέμων, καὶ τὸν ἀνάξιον δουλεύειν οὐδαμῶς ἂν φαίη τις δοῦλον εἶναι·',
    #         'εἰ δὲ μή, συμβήσεται τοὺς εὐγενεστάτους εἶναι δοκοῦντας δούλους εἶναι καὶ ἐκ δούλων, ἐὰν συμβῇ πραθῆναι ληφθέντας.']  # pylint: disable=line-too-long
    #     tokenizer = GreekSentenceTokenizer(tokenizer='regex')
    #     tokenized_sentences = tokenizer.tokenize(self.greek_text)
    #     self.assertEqual(tokenized_sentences, target)
    #
    # def test_sentence_tokenizer_greek_punkt_switch(self):
    #     """Test tokenizing Greek sentences with punkt."""
    #     target = [
    #         'ὅλως δ’ ἀντεχόμενοί τινες, ὡς οἴονται, δικαίου τινός (ὁ γὰρ νόμος δίκαιόν τἰ τὴν κατὰ πόλεμον δουλείαν τιθέασι δικαίαν, ἅμα δ’ οὔ φασιν· τήν τε γὰρ ἀρχὴν ἐνδέχεται μὴ δικαίαν εἶναι τῶν πολέμων, καὶ τὸν ἀνάξιον δουλεύειν οὐδαμῶς ἂν φαίη τις δοῦλον εἶναι· εἰ δὲ μή, συμβήσεται τοὺς εὐγενεστάτους εἶναι δοκοῦντας δούλους εἶναι καὶ ἐκ δούλων, ἐὰν συμβῇ πραθῆναι ληφθέντας.']  # pylint: disable=line-too-long
    #     tokenizer = GreekSentenceTokenizer(tokenizer='punkt')
    #     tokenized_sentences = tokenizer.tokenize(self.greek_text)
    #     self.assertEqual(tokenized_sentences, target)
    #
    # def test_sentence_tokenizer_greek_punkt_missing(self):
    #     """Test whether models are present for BackoffLatinLemmatizer"""
    #     with patch.object(GreekPunktSentenceTokenizer, 'models_path', ''):
    #         with self.assertRaises(FileNotFoundError):
    #             tokenizer = GreekPunktSentenceTokenizer()

    def test_sentence_tokenizer_sanskrit(self):
        """Test tokenizing Sanskrit sentences."""
        text = """श्री भगवानुवाच भूय एव महाबाहो श्रृणु मे परमं वचः। यत्तेऽहं प्रीयमाणाय वक्ष्यामि हितकाम्यया।।
न मे विदुः सुरगणाः प्रभवं न महर्षयः। अहमादिर्हि देवानां महर्षीणां च सर्वशः।।"""
        target = [
            "श्री भगवानुवाच भूय एव महाबाहो श्रृणु मे परमं वचः।",
            "यत्तेऽहं प्रीयमाणाय वक्ष्यामि हितकाम्यया।।",
            "न मे विदुः सुरगणाः प्रभवं न महर्षयः।",
            "अहमादिर्हि देवानां महर्षीणां च सर्वशः।।",
        ]
        tokenizer = SanskritRegexSentenceTokenizer()
        tokenized_sentences = tokenizer.tokenize(text)
        self.assertEqual(tokenized_sentences, target)


class TestWordTokenize(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    @classmethod
    def setUpClass(self):
        # corpus_importer = FetchCorpus('greek')
        # corpus_importer.import_corpus('greek_models_cltk')
        # corpus_importer = FetchCorpus('lat')
        # corpus_importer.import_corpus('latin_models_cltk')
        # self.greek_text = """ὅλως δ’ ἀντεχόμενοί τινες, ὡς οἴονται, δικαίου τινός (ὁ γὰρ νόμος δίκαιόν τἰ τὴν κατὰ πόλεμον δουλείαν τιθέασι δικαίαν, ἅμα δ’ οὔ φασιν· τήν τε γὰρ ἀρχὴν ἐνδέχεται μὴ δικαίαν εἶναι τῶν πολέμων, καὶ τὸν ἀνάξιον δουλεύειν οὐδαμῶς ἂν φαίη τις δοῦλον εἶναι· εἰ δὲ μή, συμβήσεται τοὺς εὐγενεστάτους εἶναι δοκοῦντας δούλους εἶναι καὶ ἐκ δούλων, ἐὰν συμβῇ πραθῆναι ληφθέντας."""  # pylint: disable=line-too-long
        # self.latin_text = "O di inmortales! ubinam gentium sumus? in qua urbe vivimus? quam rem publicam habemus? Hic, hic sunt in nostro numero, patres conscripti, in hoc orbis terrae sanctissimo gravissimoque consilio, qui de nostro omnium interitu, qui de huius urbis atque adeo de orbis terrarum exitio cogitent! Hos ego video consul et de re publica sententiam rogo et, quos ferro trucidari oportebat, eos nondum voce volnero! Fuisti igitur apud Laecam illa nocte, Catilina, distribuisti partes Italiae, statuisti, quo quemque proficisci placeret, delegisti, quos Romae relinqueres, quos tecum educeres, discripsisti urbis partes ad incendia, confirmasti te ipsum iam esse exiturum, dixisti paulum tibi esse etiam nunc morae, quod ego viverem."  # pylint: disable=line-too-long
        pass

    def test_greek_word_tokenizer(self):
        """Test Greek-specific word tokenizer."""
        word_tokenizer = TreebankWordTokenizer()

        # Test sources:
        # - Thuc. 1.1.1

        test = "Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων, ὡς ἐπολέμησαν πρὸς ἀλλήλους, ἀρξάμενος εὐθὺς καθισταμένου καὶ ἐλπίσας μέγαν τε ἔσεσθαι καὶ ἀξιολογώτατον τῶν προγεγενημένων, τεκμαιρόμενος ὅτι ἀκμάζοντές τε ᾖσαν ἐς αὐτὸν ἀμφότεροι παρασκευῇ τῇ πάσῃ καὶ τὸ ἄλλο Ἑλληνικὸν ὁρῶν ξυνιστάμενον πρὸς ἑκατέρους, τὸ μὲν εὐθύς, τὸ δὲ καὶ διανοούμενον."

        target = [
            "Θουκυδίδης",
            "Ἀθηναῖος",
            "ξυνέγραψε",
            "τὸν",
            "πόλεμον",
            "τῶν",
            "Πελοποννησίων",
            "καὶ",
            "Ἀθηναίων",
            ",",
            "ὡς",
            "ἐπολέμησαν",
            "πρὸς",
            "ἀλλήλους",
            ",",
            "ἀρξάμενος",
            "εὐθὺς",
            "καθισταμένου",
            "καὶ",
            "ἐλπίσας",
            "μέγαν",
            "τε",
            "ἔσεσθαι",
            "καὶ",
            "ἀξιολογώτατον",
            "τῶν",
            "προγεγενημένων",
            ",",
            "τεκμαιρόμενος",
            "ὅτι",
            "ἀκμάζοντές",
            "τε",
            "ᾖσαν",
            "ἐς",
            "αὐτὸν",
            "ἀμφότεροι",
            "παρασκευῇ",
            "τῇ",
            "πάσῃ",
            "καὶ",
            "τὸ",
            "ἄλλο",
            "Ἑλληνικὸν",
            "ὁρῶν",
            "ξυνιστάμενον",
            "πρὸς",
            "ἑκατέρους",
            ",",
            "τὸ",
            "μὲν",
            "εὐθύς",
            ",",
            "τὸ",
            "δὲ",
            "καὶ",
            "διανοούμενον",
            ".",
        ]

        result = word_tokenizer.tokenize(test)

        self.assertEqual(result, target)

    def test_latin_word_tokenizer(self):
        """Test Latin-specific word tokenizer."""
        word_tokenizer = LatinWordTokenizer()

        # Test sources:
        # - V. Aen. 1.1
        # - Prop. 2.5.1-2
        # - Ov. Am. 1.8.65-66
        # - Cic. Phillip. 13.14
        # - Plaut. Capt. 937
        # - Lucr. DRN. 5.1351-53
        # - Plaut. Bacch. 837-38
        # - Plaut. Amph. 823
        # - Caes. Bel. 6.29.2

        tests = [
            "Arma virumque cano, Troiae qui primus ab oris.",
            "Hoc verumst, tota te ferri, Cynthia, Roma, et non ignota vivere nequitia?",
            "Nec te decipiant veteres circum atria cerae. Tolle tuos tecum, pauper amator, avos!",
            "Neque enim, quod quisque potest, id ei licet, nec, si non obstatur, propterea etiam permittitur.",
            "Quid opust verbis? lingua nullast qua negem quidquid roges.",
            "Textile post ferrumst, quia ferro tela paratur, nec ratione alia possunt tam levia gigni insilia ac fusi, radii, scapique sonantes.",
            # pylint: disable=line-too-long
            "Dic sodes mihi, bellan videtur specie mulier?",
            "Cenavin ego heri in navi in portu Persico?",
            "quae ripas Ubiorum contingebat in longitudinem pedum ducentorum rescindit",
        ]

        results = []

        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)

        target = [
            [
                "Arma",
                "virum",
                "-que",
                "cano",
                ",",
                "Troiae",
                "qui",
                "primus",
                "ab",
                "oris",
                ".",
            ],
            [
                "Hoc",
                "verum",
                "est",
                ",",
                "tota",
                "te",
                "ferri",
                ",",
                "Cynthia",
                ",",
                "Roma",
                ",",
                "et",
                "non",
                "ignota",
                "vivere",
                "nequitia",
                "?",
            ],
            [
                "Nec",
                "te",
                "decipiant",
                "veteres",
                "circum",
                "atria",
                "cerae",
                ".",
                "Tolle",
                "tuos",
                "cum",
                "te",
                ",",
                "pauper",
                "amator",
                ",",
                "avos",
                "!",
            ],
            [
                "Neque",
                "enim",
                ",",
                "quod",
                "quisque",
                "potest",
                ",",
                "id",
                "ei",
                "licet",
                ",",
                "nec",
                ",",
                "si",
                "non",
                "obstatur",
                ",",
                "propterea",
                "etiam",
                "permittitur",
                ".",
            ],
            [
                "Quid",
                "opus",
                "est",
                "verbis",
                "?",
                "lingua",
                "nulla",
                "est",
                "qua",
                "negem",
                "quidquid",
                "roges",
                ".",
            ],
            [
                "Textile",
                "post",
                "ferrum",
                "est",
                ",",
                "quia",
                "ferro",
                "tela",
                "paratur",
                ",",
                "nec",
                "ratione",
                "alia",
                "possunt",
                "tam",
                "levia",
                "gigni",
                "insilia",
                "ac",
                "fusi",
                ",",
                "radii",
                ",",
                "scapi",
                "-que",
                "sonantes",
                ".",
            ],
            [
                "Dic",
                "si",
                "audes",
                "mihi",
                ",",
                "bella",
                "-ne",
                "videtur",
                "specie",
                "mulier",
                "?",
            ],
            [
                "Cenavi",
                "-ne",
                "ego",
                "heri",
                "in",
                "navi",
                "in",
                "portu",
                "Persico",
                "?",
            ],
            [
                "quae",
                "ripas",
                "Ubiorum",
                "contingebat",
                "in",
                "longitudinem",
                "pedum",
                "ducentorum",
                "rescindit",
            ],
        ]

        self.assertEqual(results, target)

    def test_tokenize_latin_words(self):
        word_tokenizer = LatinWordTokenizer()

        test = "Arma virumque cano, Troiae qui primus ab oris."
        tokens = word_tokenizer.tokenize(test)
        target = [
            "Arma",
            "virum",
            "-que",
            "cano",
            ",",
            "Troiae",
            "qui",
            "primus",
            "ab",
            "oris",
            ".",
        ]
        self.assertEqual(tokens, target)

        test = (
            "Hoc verumst, tota te ferri, Cynthia, Roma, et non ignota vivere nequitia?"
        )
        tokens = word_tokenizer.tokenize(test)
        target = [
            "Hoc",
            "verum",
            "est",
            ",",
            "tota",
            "te",
            "ferri",
            ",",
            "Cynthia",
            ",",
            "Roma",
            ",",
            "et",
            "non",
            "ignota",
            "vivere",
            "nequitia",
            "?",
        ]
        self.assertEqual(tokens, target)

        test = "Nec te decipiant veteres circum atria cerae. Tolle tuos tecum, pauper amator, avos!"
        tokens = word_tokenizer.tokenize(test)
        target = [
            "Nec",
            "te",
            "decipiant",
            "veteres",
            "circum",
            "atria",
            "cerae",
            ".",
            "Tolle",
            "tuos",
            "cum",
            "te",
            ",",
            "pauper",
            "amator",
            ",",
            "avos",
            "!",
        ]
        self.assertEqual(tokens, target)

        test = "Neque enim, quod quisque potest, id ei licet, nec, si non obstatur, propterea etiam permittitur."
        tokens = word_tokenizer.tokenize(test)
        target = [
            "Neque",
            "enim",
            ",",
            "quod",
            "quisque",
            "potest",
            ",",
            "id",
            "ei",
            "licet",
            ",",
            "nec",
            ",",
            "si",
            "non",
            "obstatur",
            ",",
            "propterea",
            "etiam",
            "permittitur",
            ".",
        ]
        self.assertEqual(tokens, target)

        test = "Quid opust verbis? lingua nullast qua negem quidquid roges."
        tokens = word_tokenizer.tokenize(test)
        target = [
            "Quid",
            "opus",
            "est",
            "verbis",
            "?",
            "lingua",
            "nulla",
            "est",
            "qua",
            "negem",
            "quidquid",
            "roges",
            ".",
        ]
        self.assertEqual(tokens, target)

        test = "Textile post ferrumst, quia ferro tela paratur, nec ratione alia possunt tam levia gigni insilia ac fusi, radii, scapique sonantes."
        tokens = word_tokenizer.tokenize(test)
        target = [
            "Textile",
            "post",
            "ferrum",
            "est",
            ",",
            "quia",
            "ferro",
            "tela",
            "paratur",
            ",",
            "nec",
            "ratione",
            "alia",
            "possunt",
            "tam",
            "levia",
            "gigni",
            "insilia",
            "ac",
            "fusi",
            ",",
            "radii",
            ",",
            "scapi",
            "-que",
            "sonantes",
            ".",
        ]
        self.assertEqual(tokens, target)

        test = "Cenavin ego heri in navi in portu Persico?"
        tokens = word_tokenizer.tokenize(test)
        target = [
            "Cenavi",
            "-ne",
            "ego",
            "heri",
            "in",
            "navi",
            "in",
            "portu",
            "Persico",
            "?",
        ]
        self.assertEqual(tokens, target)

        test = (
            "quae ripas Ubiorum contingebat in longitudinem pedum ducentorum rescindit"
        )
        tokens = word_tokenizer.tokenize(test)
        target = [
            "quae",
            "ripas",
            "Ubiorum",
            "contingebat",
            "in",
            "longitudinem",
            "pedum",
            "ducentorum",
            "rescindit",
        ]
        self.assertEqual(tokens, target)

    def test_tokenize_arabic_words(self):
        word_tokenizer = ArabicWordTokenizer()
        tests = [
            "اللُّغَةُ الْعَرَبِيَّةُ جَمِيلَةٌ.",
            "انما الْمُؤْمِنُونَ اخوه فاصلحوا بَيْنَ اخويكم",
            "الْعَجُزُ عَنِ الْإِدْرَاكِ إِدْرَاكٌ، وَالْبَحْثَ فِي ذاتِ اللَّه اشراك.",
            "اللَّهُمُّ اُسْتُرْ عُيُوبَنَا وَأَحْسَنَ خَوَاتِيمَنَا الْكَاتِبِ: نَبِيلُ جلهوم",
            "الرَّأْي قَبْلَ شَجَاعَة الشّجعَانِ",
            "فَأَنْزَلْنَا مِنْ السَّمَاء مَاء فَأَسْقَيْنَاكُمُوهُ",
            "سُئِلَ بَعْضُ الْكُتَّابِ عَنِ الْخَطّ، مَتَى يَسْتَحِقُّ أَنْ يُوصَفَ بِالْجَوْدَةِ ؟",
        ]

        results = []
        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)

        target = [
            ["اللُّغَةُ", "الْعَرَبِيَّةُ", "جَمِيلَةٌ", "."],
            ["انما", "الْمُؤْمِنُونَ", "اخوه", "فاصلحوا", "بَيْنَ", "اخويكم"],
            [
                "الْعَجُزُ",
                "عَنِ",
                "الْإِدْرَاكِ",
                "إِدْرَاكٌ",
                "،",
                "وَالْبَحْثَ",
                "فِي",
                "ذاتِ",
                "اللَّه",
                "اشراك",
                ".",
            ],  # pylint: disable=line-too-long
            [
                "اللَّهُمُّ",
                "اُسْتُرْ",
                "عُيُوبَنَا",
                "وَأَحْسَنَ",
                "خَوَاتِيمَنَا",
                "الْكَاتِبِ",
                ":",
                "نَبِيلُ",
                "جلهوم",
            ],  # pylint: disable=line-too-long
            ["الرَّأْي", "قَبْلَ", "شَجَاعَة", "الشّجعَانِ"],
            ["فَأَنْزَلْنَا", "مِنْ", "السَّمَاء", "مَاء", "فَأَسْقَيْنَاكُمُوهُ"],
            [
                "سُئِلَ",
                "بَعْضُ",
                "الْكُتَّابِ",
                "عَنِ",
                "الْخَطّ",
                "،",
                "مَتَى",
                "يَسْتَحِقُّ",
                "أَنْ",
                "يُوصَفَ",
                "بِالْجَوْدَةِ",
                "؟",
            ]
            # pylint: disable=line-too-long
        ]
        self.assertEqual(results, target)

    def test_word_tokenizer_old_french(self):
        word_tokenizer = OldFrenchWordTokenizer()

        tests = [
            "S'a table te veulz maintenir, Honnestement te dois tenir Et garder les enseignemens Dont cilz vers sont commancemens."
        ]  # pylint: disable=line-too-long

        results = []

        for test in tests:
            result = word_tokenizer.tokenize(test)
            results.append(result)

        target = [
            [
                "S'",
                "a",
                "table",
                "te",
                "veulz",
                "maintenir",
                ",",
                "Honnestement",
                "te",
                "dois",
                "tenir",
                "Et",
                "garder",
                "les",
                "enseignemens",
                "Dont",
                "cilz",
                "vers",
                "sont",
                "commancemens",
                ".",
            ]
        ]  # pylint: disable=line-too-long

        self.assertEqual(results, target)

    def test_old_norse_word_tokenizer(self):
        text = (
            "Gylfi konungr var maðr vitr ok fjölkunnigr. "
            "Hann undraðist þat mjök, er ásafólk var svá kunnigt, at allir hlutir gengu at vilja þeira."
        )
        target = [
            "Gylfi",
            "konungr",
            "var",
            "maðr",
            "vitr",
            "ok",
            "fjölkunnigr",
            ".",
            "Hann",
            "undraðist",
            "þat",
            "mjök",
            ",",
            "er",
            "ásafólk",
            "var",
            "svá",
            "kunnigt",
            ",",
            "at",
            "allir",
            "hlutir",
            "gengu",
            "at",
            "vilja",
            "þeira",
            ".",
        ]
        word_tokenizer = OldNorseWordTokenizer()
        result = word_tokenizer.tokenize(text)
        self.assertTrue(result == target)

    def test_middle_english_tokenizer(self):
        text = "    Fers am I ferd of oure fare;\n Fle we ful fast þer-fore. \n Can Y no cownsel bot care.\n\n"
        target = [
            "Fers",
            "am",
            "I",
            "ferd",
            "of",
            "oure",
            "fare",
            ";",
            "Fle",
            "we",
            "ful",
            "fast",
            "þer",
            "-",
            "fore",
            ".",
            "Can",
            "Y",
            "no",
            "cownsel",
            "bot",
            "care",
            ".",
        ]
        tokenizer = MiddleEnglishWordTokenizer()
        tokenized = tokenizer.tokenize(text)
        self.assertTrue(tokenized == target)

    def test_middle_high_german_tokenizer(self):
        text = "Gâwân het êre unde heil,\nieweders volleclîchen teil:\nnu nâht och sînes kampfes zît."
        target = [
            "Gâwân",
            "het",
            "êre",
            "unde",
            "heil",
            ",",
            "ieweders",
            "volleclîchen",
            "teil",
            ":",
            "nu",
            "nâht",
            "och",
            "sînes",
            "kampfes",
            "zît",
            ".",
        ]
        tokenizer = MiddleHighGermanWordTokenizer()
        tokenized_lines = tokenizer.tokenize(text)
        self.assertTrue(tokenized_lines == target)

    def test_akkadian_word_tokenizer(self):
        """
        Tests word_tokenizer.
        """
        tokenizer = AkkadianWordTokenizer()
        line = "u2-wa-a-ru at-ta e2-kal2-la-ka _e2_-ka wu-e-er"
        output = tokenizer.tokenize(line)
        goal = [
            ("u2-wa-a-ru", "akkadian"),
            ("at-ta", "akkadian"),
            ("e2-kal2-la-ka", "akkadian"),
            ("_e2_-ka", "sumerian"),
            ("wu-e-er", "akkadian"),
        ]
        self.assertEqual(output, goal)

    def test_akkadian_sign_tokenizer(self):
        """
        Tests sign_tokenizer.
        """
        tokenizer = AkkadianWordTokenizer()
        word = ("{gisz}isz-pur-ram", "akkadian")
        output = tokenizer.tokenize_sign(word)
        goal = [
            ("gisz", "determinative"),
            ("isz", "akkadian"),
            ("pur", "akkadian"),
            ("ram", "akkadian"),
        ]
        self.assertEqual(output, goal)

    # These are word tokenizers; the code that generates these results needs
    # to be moved to the appropriate word.py modules

    # def test_bengali_word_tokenizer(self):
    #     """Test tokenizing bengali sentences."""
    #     text = "দুর্ব্বাসার শাপে রাজা শকুন্তলাকে একেবারে ভুলে বেশ সুখে আছেন।"
    #     target = ['দুর্ব্বাসার', 'শাপে', 'রাজা', 'শকুন্তলাকে', 'একেবারে', 'ভুলে', 'বেশ', 'সুখে', 'আছেন', '।']
    #     tokenizer = TokenizeSentence('bengali')
    #     tokenized_sentences = tokenizer.tokenize(text)
    #     self.assertEqual(tokenized_sentences, target)
    #
    # def test_classical_hindi_word_tokenizer(self):
    #     """Test tokenizing classical_hindi sentences."""
    #     text = "जलर्  चिकित्सा से उन्हें कोई लाभ नहीं हुआ।"
    #     target = ['जलर्', 'चिकित्सा', 'से', 'उन्हें', 'कोई', 'लाभ', 'नहीं', 'हुआ', '।']
    #     tokenizer = TokenizeSentence('hindi')
    #     tokenized_sentences = tokenizer.tokenize(text)
    #     self.assertEqual(tokenized_sentences, target)
    #
    # def test_marathi_word_tokenizer(self):
    #     """Test tokenizing marathi sentences."""
    #     text = "अर्जुन उवाच । एवं सतत युक्ता ये भक्तास्त्वां पर्युपासते । ये चाप्यक्षरमव्यक्तं तेषां के योगवित्तमाः ॥"
    #     target = ['अर्जुन', 'उवाच', '।', 'एवं', 'सतत', 'युक्ता', 'ये', 'भक्तास्त्वां', 'पर्युपासते', '।', 'ये', 'चाप्यक्षरमव्यक्तं', 'तेषां', 'के', 'योगवित्तमाः', '॥']
    #     tokenizer = TokenizeSentence('marathi')
    #     tokenized_sentences = tokenizer.tokenize(text)
    #     self.assertEqual(tokenized_sentences, target)
    #

    #
    # def test_telugu_word_tokenizer(self):
    #     """Test tokenizing telugu sentences."""
    #     text = "తా. ఎక్కడెక్కడ బుట్టిన నదులును రత్నాకరుడను నాశతో సముద్రుని చేరువిధముగా నెన్నియిక్కట్టులకైన నోర్చి ప్రజలు దమంతట దామె ప్రియముం జూపుచు ధనికుని యింటికేతెంచుచుందురు."
    #     target = ['తా', '.', 'ఎక్కడెక్కడ', 'బుట్టిన', 'నదులును', 'రత్నాకరుడను', 'నాశతో', 'సముద్రుని', 'చేరువిధముగా', 'నెన్నియిక్కట్టులకైన', 'నోర్చి', 'ప్రజలు', 'దమంతట', 'దామె', 'ప్రియముం', 'జూపుచు', 'ధనికుని', 'యింటికేతెంచుచుందురు', '.']
    #     tokenizer = TokenizeSentence('telugu')
    #     tokenized_sentences = tokenizer.tokenize(text)
    #     self.assertEqual(tokenized_sentences, target)


class TestLineTokenize(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    def test_line_tokenizer(self):
        """Test LineTokenizer"""
        text = """49. Miraris verbis nudis me scribere versus?\nHoc brevitas fecit, sensus coniungere binos."""
        target = [
            "49. Miraris verbis nudis me scribere versus?",
            "Hoc brevitas fecit, sensus coniungere binos.",
        ]
        tokenizer = LineTokenizer("lat")
        tokenized_lines = tokenizer.tokenize(text)
        self.assertTrue(tokenized_lines == target)

    def test_line_tokenizer_include_blanks(self):
        """Test LineTokenizer"""
        text = """48. Cum tibi contigerit studio cognoscere multa,\nFac discas multa, vita nil discere velle.\n\n49. Miraris verbis nudis me scribere versus?\nHoc brevitas fecit, sensus coniungere binos."""  # pylint: disable=line-too-long
        target = [
            "48. Cum tibi contigerit studio cognoscere multa,",
            "Fac discas multa, vita nil discere velle.",
            "",
            "49. Miraris verbis nudis me scribere versus?",
            "Hoc brevitas fecit, sensus coniungere binos.",
        ]  # pylint: disable=line-too-long
        tokenizer = LineTokenizer("lat")
        tokenized_lines = tokenizer.tokenize(text, include_blanks=True)
        self.assertTrue(tokenized_lines == target)

    def test_french_line_tokenizer(self):
        """Test LineTokenizer"""
        text = """Ki de bone matire traite,\nmult li peise, se bien n’est faite.\nOëz, seignur, que dit Marie,\nki en sun tens pas ne s’oblie. """  # pylint: disable=line-too-long
        target = [
            "Ki de bone matire traite,",
            "mult li peise, se bien n’est faite.",
            "Oëz, seignur, que dit Marie,",
            "ki en sun tens pas ne s’oblie. ",
        ]  # pylint: disable=line-too-long
        tokenizer = LineTokenizer("french")
        tokenized_lines = tokenizer.tokenize(text)
        self.assertTrue(tokenized_lines == target)

    def test_french_line_tokenizer_include_blanks(self):
        """Test LineTokenizer"""
        text = """Ki de bone matire traite,\nmult li peise, se bien n’est faite.\nOëz, seignur, que dit Marie,\nki en sun tens pas ne s’oblie.\n\nLes contes que jo sai verais,\ndunt li Bretun unt fait les lais,\nvos conterai assez briefment."""  # pylint: disable=line-too-long
        target = [
            "Ki de bone matire traite,",
            "mult li peise, se bien n’est faite.",
            "Oëz, seignur, que dit Marie,",
            "ki en sun tens pas ne s’oblie.",
            "",
            "Les contes que jo sai verais,",
            "dunt li Bretun unt fait les lais,",
            "vos conterai assez briefment.",
        ]  # pylint: disable=line-too-long
        tokenizer = LineTokenizer("french")
        tokenized_lines = tokenizer.tokenize(text, include_blanks=True)
        self.assertTrue(tokenized_lines == target)


class TestSentenceTokenizeUtils(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""

    @classmethod
    def setUpClass(self):
        self.latin_text = "O di inmortales! ubinam gentium sumus? in qua urbe vivimus? quam rem publicam habemus? Hic, hic sunt in nostro numero, patres conscripti, in hoc orbis terrae sanctissimo gravissimoque consilio, qui de nostro omnium interitu, qui de huius urbis atque adeo de orbis terrarum exitio cogitent! Hos ego video consul et de re publica sententiam rogo et, quos ferro trucidari oportebat, eos nondum voce volnero! Fuisti igitur apud Laecam illa nocte, Catilina, distribuisti partes Italiae, statuisti, quo quemque proficisci placeret, delegisti, quos Romae relinqueres, quos tecum educeres, discripsisti urbis partes ad incendia, confirmasti te ipsum iam esse exiturum, dixisti paulum tibi esse etiam nunc morae, quod ego viverem."  # pylint: disable=line-too-long

    def test_sentence_tokenizer_utils(self):
        """Test sentence tokenization trainer"""
        trainer = SentenceTokenizerTrainer("lat")
        self.assertIsInstance(
            trainer.train_sentence_tokenizer(self.latin_text), PunktSentenceTokenizer
        )

    def test_sentence_tokenizer_utils_with_punctuation(self):
        """Test sentence tokenization trainer"""
        trainer = SentenceTokenizerTrainer("lat", punctuation=[".", "?", "!"])
        self.assertIsInstance(
            trainer.train_sentence_tokenizer(self.latin_text), PunktSentenceTokenizer
        )

    def test_sentence_tokenizer_utils_with_abbreviations(self):
        """Test sentence tokenization trainer"""
        trainer = SentenceTokenizerTrainer("lat", abbreviations=["Kal."])
        self.assertIsInstance(
            trainer.train_sentence_tokenizer(self.latin_text), PunktSentenceTokenizer
        )

    def test_sentence_tokenizer_utils_with_strict(self):
        """Test sentence tokenization trainer"""
        trainer = SentenceTokenizerTrainer(
            "lat", strict=True, punctuation=[".", "?", "!"], strict_punctuation=[","]
        )
        self.assertIsInstance(
            trainer.train_sentence_tokenizer(self.latin_text), PunktSentenceTokenizer
        )

    def test_sentence_tokenizer_trainer_pickle(self):
        with patch.object(
            SentenceTokenizerTrainer, "pickle_sentence_tokenizer"
        ) as mock:
            trainer = SentenceTokenizerTrainer("lat")
            trainer.pickle_sentence_tokenizer("mock.p", trainer)
        mock.assert_called_once_with("mock.p", trainer)

    def test_sentence_tokenizer_utils_latin(self):
        """Test sentence tokenization trainer"""
        trainer = LatinSentenceTokenizerTrainer()
        self.assertIsInstance(
            trainer.train_sentence_tokenizer(self.latin_text), PunktSentenceTokenizer
        )


if __name__ == "__main__":
    unittest.main()
