Akkadian
********

Akkadian is an extinct East Semitic language (part of the greater Afroasiatic language family) that was spoken in ancient Mesopotamia. \
The earliest attested Semitic language, it used the cuneiform writing system, which was originally used to write the unrelated Ancient \
Sumerian, a language isolate. From the second half of the third millennium BC (ca. 2500 BC), texts fully written in Akkadian begin to \
appear. Hundreds of thousands of texts and text fragments have been excavated to date, covering a vast textual tradition of \
mythological narrative, legal texts, scientific works, correspondence, political and military events, and many other examples. \
By the second millennium BC, two variant forms of the language were in use in Assyria and Babylonia, known as Assyrian and \
Babylonian respectively. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Akkadian>`_)

Workflow Sample Model
=====================
A sample workflow model of utilizing the tools in Akkadian is shown below. In this example, we are taking a text file \
downloaded from CDLI, importing it, and have it be read and ingested. From here, we will look at the table of contents, \
select a text, convert the text into Unicode and PrettyPrint its result.

**note:** this workflow model uses a set of test documents, available to be downloaded here:

https://github.com/cltk/cltk/tree/master/cltk/tests/test_akkadian

When you have downloaded these files, utilize its file location within os.path.join(), *e.g.: os.path.join('downloads', \
'single_text.txt')*. **This tutorial assumes that you are using a fork of CLTK.**

.. code-block:: python

   In[1]: from cltk.corpus.akkadian.file_importer import FileImport

   In[2]: from cltk.corpus.akkadian.cdli_corpus import CDLICorpus

   In[3]: from cltk.corpus.akkadian.pretty_print import PrettyPrint

   In[4]: from cltk.corpus.akkadian.tokenizer import Tokenizer

   In[5]: from cltk.tokenize.word import WordTokenizer

   In[6]: from cltk.stem.akkadian.atf_converter import ATFConverter

   In[7]: import os

   # import a text and read it
   In[8]: fi = FileImport(os.path.join('test_akkadian', 'single_text.txt'))

   In[9]: fi.read_file()

   # output = fi.raw_file or fi.file_lines; for folder catalog = fi.file_catalog()
   # ingest your file lines
   In[10]: cc = CDLICorpus()

   In[11]: cc.parse_file(fi.file_lines)

   # this creates disparate sections of the text ingested (edition, metadata, etc)
   In[12]: transliteration = [cc.catalog[text]['transliteration'] for text in cc.catalog]

   # access the data through cc.texts (e.g. above) or initial prints (e.g. below):
   # look through the file's contents
   In[13]: print(cc.toc())
   Out[13]: ['Pnum: P254202, Edition: ARM 01, 001, length: 23 line(s)']

   # select a text through edition or cdli number (there's also .print_metadata):
   In[14]: selected_text = cc.catalog['P254202']['transliteration']

   # otherwise use the above 'transliteration'; same thing:
   In[15]: print(selected_text)
   Out[15]: ['a-na ia-ah-du-li-[im]', 'qi2-bi2-[ma]', 'um-ma a-bi-sa-mar#-[ma]', 'sa-li-ma-am e-pu-[usz]',
             'asz-szum mu-sze-zi-ba-am# [la i-szu]', '[sa]-li#-ma-am sza e-[pu-szu]', '[u2-ul] e-pu-usz sa#-[li-mu-um]',
             '[u2-ul] sa-[li-mu-um-ma]', 'isz#-tu mu#-[sze-zi-ba-am la i-szu]', 'a-la-nu-ia sza la is,-s,a-ab#-[tu]',
             'i-na-an-na is,-s,a-ab-[tu]', 'i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]',
             'ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]', 'u3 ia-am-ha-ad[{ki}]', 'a-la-nu an-nu-tum u2-ul ih-li-qu2#',
             'i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma', 'ih-ta-al-qu2',
             'u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#', 'u3 na-pa-asz2-ti u2-ba-li-it,', 'pi2-qa-at ha-s,e-ra#-at',
             'asz-szum a-la-nu-ka', 'u3 ma-ru-ka sza-al#-[mu]', '[a-na na-pa]-asz2#-ti-ia i-tu-ur']

   In[16]: print(transliteration[0])
   Out[16]: ['a-na ia-ah-du-li-[im]', 'qi2-bi2-[ma]', 'um-ma a-bi-sa-mar#-[ma]', 'sa-li-ma-am e-pu-[usz]',
             'asz-szum mu-sze-zi-ba-am# [la i-szu]', '[sa]-li#-ma-am sza e-[pu-szu]', '[u2-ul] e-pu-usz sa#-[li-mu-um]',
             '[u2-ul] sa-[li-mu-um-ma]', 'isz#-tu mu#-[sze-zi-ba-am la i-szu]', 'a-la-nu-ia sza la is,-s,a-ab#-[tu]',
             'i-na-an-na is,-s,a-ab-[tu]', 'i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]',
             'ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]', 'u3 ia-am-ha-ad[{ki}]', 'a-la-nu an-nu-tum u2-ul ih-li-qu2#',
             'i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma', 'ih-ta-al-qu2',
             'u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#', 'u3 na-pa-asz2-ti u2-ba-li-it,', 'pi2-qa-at ha-s,e-ra#-at',
             'asz-szum a-la-nu-ka', 'u3 ma-ru-ka sza-al#-[mu]', '[a-na na-pa]-asz2#-ti-ia i-tu-ur']

   # tokenize by word or sign
   In[17]: atf = ATFConverter()

   In[18]: tk = Tokenizer()

   In[19]: wtk = WordTokenizer('akkadian')

   In[18]: lines = [tk.string_tokenizer(text, include_blanks=False)
                    for text in atf.process(selected_text)]

   In[20]: words = [wtk.tokenize(line[0]) for line in lines]

   # taking off first four lines to focus on the text with [4:]
   In[21]: print(lines)
   In[21]: [['a-na ia-ah-du-li-im'], ['qi2-bi2-ma'], ['um-ma a-bi-sa-mar-ma'], ['sa-li-ma-am e-pu-usz'],
            ['asz-szum mu-sze-zi-ba-am la i-szu'], ['sa-li-ma-am sza e-pu-szu'], ['u2-ul e-pu-usz sa-li-mu-um'],
            ['u2-ul sa-li-mu-um-ma'], ['isz-tu mu-sze-zi-ba-am la i-szu'], ['a-la-nu-ia sza la is,-s,a-ab-tu'],
            ['i-na-an-na is,-s,a-ab-tu'], ['i-na ne2-kur-ti _lu2_ ha-szi-im{ki}'],
            ['ur-si-im{ki} _lu2_ ka-ar-ka-mi-is{ki}'], ['u3 ia-am-ha-ad{ki}'], ['a-la-nu an-nu-tum u2-ul ih-li-qu2'],
            ['i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur-ma'], ['ih-ta-al-qu2'],
            ['u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib'], ['u3 na-pa-asz2-ti u2-ba-li-it,'],
            ['pi2-qa-at ha-s,e-ra-at'], ['asz-szum a-la-nu-ka'], ['u3 ma-ru-ka sza-al-mu'],
            ['a-na na-pa-asz2-ti-ia i-tu-ur']]

   In[22]: print(words)
   In[22]: [[('a-na', 'akkadian'), ('ia-ah-du-li-im', 'akkadian')], [('qi2-bi2-ma', 'akkadian')],
            [('um-ma', 'akkadian'), ('a-bi-sa-mar-ma', 'akkadian')], [('sa-li-ma-am', 'akkadian'),
             ('e-pu-usz', 'akkadian')],
             [('asz-szum', 'akkadian'), ('mu-sze-zi-ba-am', 'akkadian'), ('la', 'akkadian'), ('i-szu', 'akkadian')],
            [('sa-li-ma-am', 'akkadian'), ('sza', 'akkadian'), ('e-pu-szu', 'akkadian')],
            [('u2-ul', 'akkadian'), ('e-pu-usz', 'akkadian'), ('sa-li-mu-um', 'akkadian')],
            [('u2-ul', 'akkadian'), ('sa-li-mu-um-ma', 'akkadian')],
            [('isz-tu', 'akkadian'), ('mu-sze-zi-ba-am', 'akkadian'), ('la', 'akkadian'), ('i-szu', 'akkadian')],
            [('a-la-nu-ia', 'akkadian'), ('sza', 'akkadian'), ('la', 'akkadian'), ('is,-s,a-ab-tu', 'akkadian')],
            [('i-na-an-na', 'akkadian'), ('is,-s,a-ab-tu', 'akkadian')],
            [('i-na', 'akkadian'), ('ne2-kur-ti', 'akkadian'), ('_lu2_', 'sumerian'), ('ha-szi-im{ki}', 'akkadian')],
            [('ur-si-im{ki}', 'akkadian'), ('_lu2_', 'sumerian'), ('ka-ar-ka-mi-is{ki}', 'akkadian')],
            [('u3', 'akkadian'), ('ia-am-ha-ad{ki}', 'akkadian')],
            [('a-la-nu', 'akkadian'), ('an-nu-tum', 'akkadian'), ('u2-ul', 'akkadian'), ('ih-li-qu2', 'akkadian')],
            [('i-na', 'akkadian'), ('ne2-kur-ti', 'akkadian'), ('{disz}sa-am-si-{d}iszkur-ma', 'akkadian')],
            [('ih-ta-al-qu2', 'akkadian')],
            [('u3', 'akkadian'), ('a-la-nu', 'akkadian'), ('sza', 'akkadian'), ('ki-ma', 'akkadian'),
             ('u2-hu-ru', 'akkadian'), ('u2-sze-zi-ib', 'akkadian')],
            [('u3', 'akkadian'), ('na-pa-asz2-ti', 'akkadian'), ('u2-ba-li-it,', 'akkadian')],
            [('pi2-qa-at', 'akkadian'), ('ha-s,e-ra-at', 'akkadian')],
            [('asz-szum', 'akkadian'), ('a-la-nu-ka', 'akkadian')],
            [('u3', 'akkadian'), ('ma-ru-ka', 'akkadian'), ('sza-al-mu', 'akkadian')],
            [('a-na', 'akkadian'), ('na-pa-asz2-ti-ia', 'akkadian'), ('i-tu-ur', 'akkadian')]]

   In[23]: for signs in words:
   In[24]:     sign = [tk.sign_tokenizer(x) for x in signs]
   # Note: Not printing 'signs' due to length. Try it!

   # Pretty printing:
   In[25]: pp = PrettyPrint()

   In[26]: destination = os.path.join('test_akkadian', 'html_single_text.html')

   In[27]: pp.html_print_single_text(cc.catalog, '&P254202', destination)

Read File
=========

Reads a `.txt` file and saves to memory the text in `.raw_file` and `.file_lines`.
These two instance attributes are used for the ATFConverter.

.. code-block:: python

   In[1]: import os

   In[2]: from cltk.corpus.akkadian.file_importer import FileImport

   In[3]: text_location = os.path.join('test_akkadian', 'single_text.txt')

   In[4]: text = FileImport(text_location)

   In[5]: text.read_file()

To access the text file, use `.raw_file` or `.file_lines`.
`.raw_file` is the file in its entirety, `.file_lines` splits the text using `.splitlines`.

File Catalog
============

This function looks at the folder storing a file and outputs its contents.

.. code-block:: python

   In[1]: import os

   In[2]: from cltk.corpus.akkadian.file_importer import FileImport

   In[3]: text_location = os.path.join('test_akkadian', 'single_text.txt')

   In[4]: folder = FileImport(text_location)

   In[5]: folder.file_catalog()

   Out[5]: ['html_file.html', 'html_single_text.html', 'single_text.txt',
            'test_akkadian.py', 'two_text_abnormalities.txt']

Parse File
==========

This method captures information in a text file and formats it in a clear, and disparate, manner for every text found.
It saves to memory dictionaries that split up texts by text edition, cdli number, metadata, and various text,
all of which are callable.

.. code-block:: python

   In[1]: Import os

   In[2]: from cltk.corpus.akkadian.cdli_corpus import CDLICorpus

   In[3]: cdli = CDLICorpus()

   In[4]: f_i = FileImport(os.path.join('test_akkadian', 'single_text.txt'))

   In[5]: f_i.read_file()

   In[6]: cdli.parse_file(f_i.file_lines)

To access the text, use `.catalog`.

.. code-block:: python

   In[7]: print(cc.catalog)
   Out[7]: {'P254202': {'metadata': ['Primary publication: ARM 01, 001', 'Author(s): Dossin, Georges',
                                     'Publication date: 1946',
                                     'Secondary publication(s): Durand, Jean-Marie, LAPO 16, 0305',
                                     'Collection: National Museum of Syria, Damascus, Syria',
                                     'Museum no.: NMSD —', 'Accession no.:', 'Provenience: Mari (mod. Tell Hariri)',
                                     'Excavation no.:', 'Period: Old Babylonian (ca. 1900-1600 BC)',
                                     'Dates referenced:', 'Object type: tablet', 'Remarks:', 'Material: clay',
                                     'Language: Akkadian', 'Genre: Letter', 'Sub-genre:', 'CDLI comments:',
                                     'Catalogue source: 20050104 cdliadmin', 'ATF source: cdlistaff',
                                     'Translation: Durand, Jean-Marie (fr); Guerra, Dylan M. (en)',
                                     'UCLA Library ARK: 21198/zz001rsp8x', 'Composite no.:', 'Seal no.:',
                                     'CDLI no.: P254202'],
                             'pnum': 'P254202',
                          'edition': 'ARM 01, 001',
                        'raw_text': ['@obverse', '1. a-na ia-ah-du-li-[im]', '2. qi2-bi2-[ma]',
                                     '3. um-ma a-bi-sa-mar#-[ma]', '4. sa-li-ma-am e-pu-[usz]',
                                     '5. asz-szum mu-sze-zi-ba-am# [la i-szu]', '6. [sa]-li#-ma-am sza e-[pu-szu]',
                                     '7. [u2-ul] e-pu-usz sa#-[li-mu-um]', '8. [u2-ul] sa-[li-mu-um-ma]',
                                     '$ rest broken', '@reverse', '$ beginning broken',
                                     "1'. isz#-tu mu#-[sze-zi-ba-am la i-szu]",
                                     "2'. a-la-nu-ia sza la is,-s,a-ab#-[tu]", "3'. i-na-an-na is,-s,a-ab-[tu]",
                                     "4'. i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]",
                                     "5'. ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]", "6'. u3 ia-am-ha-ad[{ki}]",
                                     "7'. a-la-nu an-nu-tum u2-ul ih-li-qu2#",
                                     "8'. i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma", "9'. ih-ta-al-qu2",
                                     "10'. u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#",
                                     "11'. u3 na-pa-asz2-ti u2-ba-li-it,", "12'. pi2-qa-at ha-s,e-ra#-at",
                                     "13'. asz-szum a-la-nu-ka", "14'. u3 ma-ru-ka sza-al#-[mu]",
                                     "15'. [a-na na-pa]-asz2#-ti-ia i-tu-ur"],
                 'transliteration': ['a-na ia-ah-du-li-[im]', 'qi2-bi2-[ma]', 'um-ma a-bi-sa-mar#-[ma]',
                                     'sa-li-ma-am e-pu-[usz]', 'asz-szum mu-sze-zi-ba-am# [la i-szu]',
                                     '[sa]-li#-ma-am sza e-[pu-szu]', '[u2-ul] e-pu-usz sa#-[li-mu-um]',
                                     '[u2-ul] sa-[li-mu-um-ma]', 'isz#-tu mu#-[sze-zi-ba-am la i-szu]',
                                     'a-la-nu-ia sza la is,-s,a-ab#-[tu]', 'i-na-an-na is,-s,a-ab-[tu]',
                                     'i-na ne2-kur-ti _lu2_ ha-szi-[im{ki}]',
                                     'ur-si-im{ki} _lu2_ ka-ar-ka#-[mi-is{ki}]', 'u3 ia-am-ha-ad[{ki}]',
                                     'a-la-nu an-nu-tum u2-ul ih-li-qu2#',
                                     'i-na ne2-kur-ti {disz}sa-am-si-{d}iszkur#-ma', 'ih-ta-al-qu2',
                                     'u3 a-la-nu sza ki-ma u2-hu-ru u2-sze-zi-ib#', 'u3 na-pa-asz2-ti u2-ba-li-it,',
                                     'pi2-qa-at ha-s,e-ra#-at', 'asz-szum a-la-nu-ka', 'u3 ma-ru-ka sza-al#-[mu]',
                                     '[a-na na-pa]-asz2#-ti-ia i-tu-ur'],
                   'normalization': [],
                     'translation': []}}

Table of Contents
=================

Prints a table of contents from which one can identify the edition and cdli number for printing purposes.

.. code-block:: python

   In[1]: Import os

   In[2]: from cltk.corpus.akkadian.cdli_corpus import CDLICorpus

   In[3]: cdli = CDLICorpus()

   In[4]: path = FileImport(os.path.join('test_akkadian', 'single_text.txt'))

   In[5]: f_i = FileImport(path)

   In[6]: f_i.read_file()

   In[6]: cdli.toc()
   Out[6]: ['Pnum: P254202, Edition: ARM 01, 001, length: 23 line(s)']

List Pnums
==========

Prints cdli numbers from which one can identify the edition and cdli number for printing purposes.

.. code-block:: python

   In[1]: Import os

   In[2]: from cltk.corpus.akkadian.cdli_corpus import CDLICorpus

   In[3]: cdli = CDLICorpus()

   In[4]: path = FileImport(os.path.join('test_akkadian', 'single_text.txt'))

   In[5]: f_i = FileImport(path)

   In[6]: f_i.read_file()

   In[6]: cdli.list_pnums()
   Out[6]: ['P254202']

List Editions
=============

Prints editions from which one can identify the edition and cdli number for printing purposes.

.. code-block:: python

   In[1]: Import os

   In[2]: from cltk.corpus.akkadian.cdli_corpus import CDLICorpus

   In[3]: cdli = CDLICorpus()

   In[4]: path = FileImport(os.path.join('test_akkadian', 'single_text.txt'))

   In[5]: f_i = FileImport(path)

   In[6]: f_i.read_file()

   In[6]: cdli.list_editions()
   Out[6]: ['ARM 01, 001']

Print Catalog
=============

Prints cdli_corpus.catalog with bite-sized information, rather than text entirety.

.. code-block:: python

   In[1]: Import os

   In[2]: from cltk.corpus.akkadian.cdli_corpus import CDLICorpus

   In[3]: cdli = CDLICorpus()

   In[4]: path = FileImport(os.path.join('test_akkadian', 'single_text.txt'))

   In[5]: f_i = FileImport(path)

   In[6]: f_i.read_file()

   In[6]: cdli.print_catalog()
   Out[6]: Pnum: P254202
           Edition: ARM 01, 001
           Metadata: True
           Transliteration: True
           Normalization: False
           Translation: False

Tokenization
============

The Akkadian tokenizer reads ATF material and converts the data into readable, mutable tokens.
There is an option whether or not to `preserve damage` in the text.

The ATFConverter depends upon the word and sign tokenizer outputs.

**String Tokenization:**

This function is based off CLTK's line tokenizer. Use this for strings (e.g. copy-and-pasinge lines from a document) rather than .txt files.

.. code-block:: python

   In[1]: from cltk.akkadian.Tokenizer import  Tokenizer

   In[2]: line_tokenizer = Tokenizer(preserve_damage=False)

   In[3]: text = '20. u2-sza-bi-la-kum\n1. a-na ia-as2-ma-ah-{d}iszkur#\n' \
               '2. qi2-bi2-ma\n3. um-ma {d}utu-szi-{d}iszkur\n' \
               '4. a-bu-ka-a-ma\n5. t,up-pa-[ka] sza#-[tu]-sza-bi-lam esz-me' \
               '\n' '6. asz-szum t,e4#-em# {d}utu-illat-su2\n'\
               '7. u3 ia#-szu-ub-dingir sza a-na la i-[zu]-zi-im\n'

   In[4]: line_tokenizer.string_token(text)
   Out[4]: ['20. u2-sza-bi-la-kum',
            '1. a-na ia-as2-ma-ah-{d}iszkur',
            '2. qi2-bi2-ma',
            '3. um-ma {d}utu-szi-{d}iszkur',
            '4. a-bu-ka-a-ma',
            '5. t,up-pa-ka sza-tu-sza-bi-lam esz-me',
            '6. asz-szum t,e4-em {d}utu-illat-su2',
            '7. u3 ia-szu-ub-dingir sza a-na la i-zu-zi-im']

**Line Tokenization:**

Line Tokenization is for any text, from `FileImport.raw_text` to `.CDLICorpus.texts`.

.. code-block:: python

   In[1]: import os

   In[2]: from cltk.akkadian.tokenizer import  Tokenizer

   In[3]: line_tokenizer = Tokenizer(preserve_damage=False)

   In[4]: text = os.path.join('test_akkadian', 'single_text.txt')

   In[5]: line_tokenizer.line_token(text[1:8])
   Out[5]: ['a-na ia-ah-du-li-[im]',
            'qi2-bi2-[ma]',
            'um-ma a-bi-sa-mar#-[ma]',
            'sa-li-ma-am e-pu-[usz]',
            'asz-szum mu-sze-zi-ba-am# [la i-szu]',
            '[sa]-li#-ma-am sza e-[pu-szu]',
            '[u2-ul] e-pu-usz sa#-[li-mu-um]',
            '[u2-ul] sa-[li-mu-um-ma]']

**Word Tokenization:**

Word tokenization operates on a single line of text, returns all words in the line as a tuple in a list.

.. code-block:: python

   In[1]: import os

   In[2]: from cltk.tokenize.word import  WordTokenizer

   In[3]: word_tokenizer = WordTokenizer('akkadian')

   In[4]: line = 'u2-wa-a-ru at-ta e2-kal2-la-ka _e2_-ka wu-e-er'

   In[5]: output = word_tokenizer.tokenize(line)
   Out[5]: [('u2-wa-a-ru', 'akkadian'), ('at-ta', 'akkadian'),
            ('e2-kal2-la-ka', 'akkadian'), ('_e2_-ka', 'sumerian'),
            ('wu-e-er', 'akkadian')]

**Sign Tokenization:**

Sign Tokenization takes a tuple (word, language) and splits the word up into individual sign tuples (sign, language) in a list.

.. code-block:: python

   In[1]: import os

   In[2]: from cltk.tokenize.word import  WordTokenizer

   In[3]: word_tokenizer = WordTokenizer('akkadian')

   In[4]: word = ("{gisz}isz-pur-ram", "akkadian")

   In[5]: word_tokenizer.tokenize_sign(word)
   Out[5]: [("gisz", "determinative"), ("isz", "akkadian"),
            ("pur", "akkadian"), ("ram", "akkadian")]

Unicode Conversion
==================

From a list of tokens, this module will return the list converted from CDLI standards to print publication standards.
`two_three` is a function allows the user to turn on and off accent marking for signs (`a₂` versus `á`).

.. code-block:: python

   In[1]: from cltk.stem.akkadian.atf_converter import ATFConverter

   In[2]: atf = ATFConverter(two_three=False)

   In[2]: test = ['as,', 'S,ATU', 'tet,', 'T,et', 'sza', 'ASZ', "a", "a2", "a3", "be2", "bad3", "buru14"]

   In[4]: atf.process(test)

   Out[4]: ['aṣ', 'ṢATU', 'teṭ', 'Ṭet', 'ša', 'AŠ', "a", "á", "à", "bé", "bàd", "buru₁₄"]

Pretty Printing
===============

Pretty Print allows an individual to take a `.txt` file and populate it into an html file.

.. code-block:: python

   In[1]: import os

   In[2]: from cltk.corpus.akkadian.pretty_print import  PrettyPrint

   In[3]: origin = os.path.join('test_akkadian', 'single_text.txt')

   In[4]: destination = os.path.join('..', 'Akkadian_test_text', 'html_single_text.html')

   In[5]: f_i = FileImport(path)
        f_i.read_file()
        origin = f_i.raw_file
        p_p = PrettyPrint()
        p_p.html_print(origin, destination)
        f_o = FileImport(destination)
        f_o.read_file()
        output = f_o.raw_file

Syllabifier
===========

Syllabify Akkadian words.

.. code-block:: python

   In [1]: from cltk.stem.akkadian.syllabifier import Syllabifier

   In [2]: word = "epištašu"

   In [3]: syll = Syllabifier()

   In [4]: syll.syllabify(word)
   ['e', 'piš', 'ta', 'šu']

Stress
======

This function identifies the stress on an Akkadian word.

.. code-block:: python

   In[2]: from cltk.phonology.akkadian.stress import StressFinder

   In[3]: stresser = StressFinder()

   In[4]: word = "šarrātim"

   In[5]: stresser.find_stress(word)

   Out[5]: ['šar', '[rā]', 'tim']

Decliner
========

This method outputs a list of tuples the first element being a declined noun, the second a dictionary containing its attributes.

.. code-block:: python

   In[2]: from cltk.stem.akkadian.declension import NaiveDecliner

   In[3]: word = 'ilum'

   In[4]: decliner = NaiveDecliner()

   In[5]: decliner.decline_noun(word, 'm')

   Out[5]:
   [('ilam', {'case': 'accusative', 'number': 'singular'}),
    ('ilim', {'case': 'genitive', 'number': 'singular'}),
    ('ilum', {'case': 'nominative', 'number': 'singular'}),
    ('ilīn', {'case': 'oblique', 'number': 'dual'}),
    ('ilān', {'case': 'nominative', 'number': 'dual'}),
    ('ilī', {'case': 'oblique', 'number': 'plural'}),
    ('ilū', {'case': 'nominative', 'number': 'plural'})]

Stems and Bound Forms
=====================

These two methods reduce a noun to its stem or bound form.

.. code-block:: python

   In[2]: from cltk.stem.akkadian.stem import Stemmer

   In[3]: stemmer = Stemmer()

   In[4]: word = "ilātim"

   In[5]: stemmer.get_stem(word, 'f')

   Out[5]: 'ilt'

.. code-block:: python

   In[2]: from cltk.stem.akkadian.bound_form import BoundForm

   In[3]: bound_former = BoundForm()

   In[4]: word = "kalbim"

   In[5]: bound_former.get_bound_form(word, 'm')

   Out[5]: 'kalab'

Consonant and Vowel patterns
============================

It's useful to be able to parse Akkadian words as sequences of consonants and vowels.

.. code-block:: python

   In[2]: from cltk.stem.akkadian.cv_pattern import CVPattern

   In[3]: cv_patterner = CVPattern()

   In[4]: word = "iparras"

   In[5]: cv_patterner.get_cv_pattern(word)

   Out[5]:
   [('V', 1, 'i'),
    ('C', 1, 'p'),
    ('V', 2, 'a'),
    ('C', 2, 'r'),
    ('C', 2, 'r'),
    ('V', 2, 'a'),
    ('C', 3, 's')]

   In[6]: cv_patterner.get_cv_pattern(word, pprint=True)

   Out[6]: 'V₁C₁V₂C₂C₂V₂C₃'

Stopword Filtering
==================

To use the CLTK's built-in stopwords list for Akkadian:

.. code-block:: python

    In[2]: from nltk.tokenize.punkt import PunktLanguageVars

    In[3]: from cltk.stop.akkadian.stops import STOP_LIST

    In[4]: sentence = "šumma awīlum ina dīnim ana šībūt sarrātim ūṣiamma awat iqbû la uktīn šumma dīnum šû dīn napištim awīlum šû iddâk"

    In[5]: p = PunktLanguageVars()

    In[6]: tokens = p.word_tokenize(sentence.lower())

    In[7]: [w for w in tokens if not w in STOP_LIST]
    Out[7]:
    ['awīlum',
     'dīnim',
     'šībūt',
     'sarrātim',
     'ūṣiamma',
     'awat',
     'iqbû',
     'uktīn',
     'dīnum',
     'dīn',
     'napištim',
     'awīlum',
     'iddâk']
