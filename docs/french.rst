French
******

Old French (franceis, françois, romanz; Modern French ancien français) was the language spoken in Northern France from the 8th century to the 14th century. In the 14th century, these dialects came to be collectively known as the langue d'oïl, contrasting with the langue d'oc or Occitan language in the south of France. The mid-14th century is taken as the transitional period to Middle French, the language of the French Renaissance, specifically based on the dialect of the Île-de-France region. The place and area where Old French was spoken natively roughly extended to the historical Kingdom of France and its vassals, but the influence of Old French was much wider, as it was carried to England, Sicily and the Crusader states as the language of a feudal elite and of commerce.

(Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_French>`_)

LEMMATIZER
==================
The lemmatizer takes as its input a list of tokens, previously tokenized and made lower-case.
.. It first seeks a match between each token and a list of potential lemmas taken from Godefroy (1901)’s Lexique, the Tobler-Lommatszch, and the DECT. If a match is not found, the lemmatizer then seeks a match between the forms different lemmas have been known to take and the token (this at present only applies to lemmas from A-D and W-Z). If no match is returned at this stage, a set of rules is applied to the token. These rules are similar to those applied by the stemmer but aim to bring forms in line with lemmas rather than truncating them. Finally, if no match is found between the modified token and the list of lemmas, a result of ‘None’ is returned.

.. References:
..  Godefroy. 1901. Lexique de l'Ancien Français. Paris & Leipzig : Welter.
..  Tobler, Adolf and Erhard Lommatzsch. 1915. Altfranzösisches Wörterbuch. Adolf Toblers nachgelassene Materialen, bearbeitet und herausgegeben von Erhard Lommatzsch, wietergeführt von Hans Helmut Christmann. Stuttgart: Franz Steiner Verlag.
..  DÉCT : Dictionnaire Électronique de Chrétien de Troyes, http://www.atilf.fr/dect, LFA/Université d'Ottawa - ATILF/CNRS & Université de Lorraine. 2014.


.. code-block:: python

    In [1]: from cltk.tokenize.word import WordTokenizer

    In [2]: from cltk.lemmatize.french.lemma import LemmaReplacer

    In [3]: text = "Li rois pense que par folie, Sire Tristran, vos aie amé ; Mais Dé plevis ma loiauté, Qui sor mon cors mete flaele, S’onques fors cil qui m’ot pucele Out m’amistié encor nul jor !"

    In [4]: text = str.lower(text)

    In [5]: tokenizer = WordTokenizer('french')

    In [6]: lemmatizer = LemmaReplacer()

    In [7]: tokens = tokenizer.tokenize(text)

    In [8]: lemmatizer.lemmatize(tokens)
    Out [8]: [('li', 'li'), ('rois', 'rois'), ('pense', 'pense'), ('que', 'que'), ('par', 'par'), ('folie', 'folie'), (',', ['PUNK']), ('sire', 'sire'), ('tristran', 'None'), (',', ['PUNK']), ('vos', 'vos'), ('aie', ['avoir']), ('amé', 'amer'), (';', ['PUNK']), ('mais', 'mais'), ('dé', 'dé'), ('plevis', 'plevir'), ('ma', 'ma'), ('loiauté', 'loiauté'), (',', ['PUNK']), ('qui', 'qui'), ('sor', 'sor'), ('mon', 'mon'), ('cors', 'cors'), ('mete', 'mete'), ('flaele', 'flaele'), (',', ['PUNK']), ("s'", "s'"), ('onques', 'onques'), ('fors', 'fors'), ('cil', 'cil'), ('qui', 'qui'), ("m'", "m'"), ('ot', 'ot'), ('pucele', 'pucele'), ('out', ['avoir']), ("m'", "m'"), ('amistié', 'amistié'), ('encor', 'encor'), ('nul', 'nul'), ('jor', 'jor'), ('!', ['PUNK'])]


LINE TOKENIZATION:
==================
The line tokenizer takes a string as its input and returns a list of strings.

.. code-block:: python

    In [1]: from cltk.tokenize.line import LineTokenizer

    In [2]: tokenizer = LineTokenizer('french')

    In [3]: untokenized_text = """Ki de bone matire traite,\nmult li peise, se bien n’est faite.\nOëz, seignur, que dit Marie,\nki en sun tens pas ne s’oblie."""

    In [4]: tokenizer.tokenize(untokenized_text)
    Out [4]: ['Ki de bone matire traite,', 'mult li peise, se bien n’est faite.','Oëz, seignur, que dit Marie,', 'ki en sun tens pas ne s’oblie. ']


NAMED ENTITY RECOGNITION
========================
The named entity recognizer for French takes as its input a string and returns a list of tuples. It tags named entities from a list, and also displays the category to which this named entity belongs.

Categories are modeled on those found in (`Moisan, 1986 <https://books.google.fr/books/about/Répertoire_des_noms_propres_de_personne.html?id=C9ng9q6pQHwC&redir_esc=y>`_) and include:

- Locations “LOC” (e.g. Girunde)
- Nationalities/places of origin “NAT” (e.g. Grius)
- Individuals:
  - animals “ANI” (i.e. horses, e.g. Veillantif, cows, e.g. Blerain, dogs, e.g. Husdent)
  - authors “AUT” (e.g. Marie, Chrestïen)
  - nobility “CHI” (e.g. Rolland, Artus). n.b. Characters such as Turpin are counted as nobility rather than religious figures.
  - characters from classical sources “CLAS” (e.g. Echo)
  - feasts “F” (e.g. Pentecost)
  - religious things “REL” (i.e. saints, e.g. St Alexis, and deities, e.g. Deus, and Old Testament people, e.g. Adam)
  - swords “SW” (e.g. Hautecler)
  - commoners “VIL” (e.g Pathelin)

.. code-block:: python

    In [1]: from cltk.tag.ner import NamedEntityReplacer

    In [2]: text_str = """Berte fu mere Charlemaine, qui pukis tint France et tot le Maine."""

    In [3]: ner_replacer = NamedEntityReplacer()

    In [4]: ner_replacer.tag_ner_fr(text_str)
    Out [4]: [[('Berte', 'entity', 'CHI')], ('fu',), ('mere',), [('Charlemaine', 'entity', 'CHI')], (',',), ('qui',), ('pukis',), ('tint',), [('France', 'entity', 'LOC')], ('et',), ('tot',), ('le',), [('Maine', 'entity', 'LOC')], ('.',)]

.. Reference: Moisan, A. 1986. Répertoire des noms propres de personnes et de lieux cités dans les Chansons de Geste françaises et les œuvres étrangères dérivées. Publications romanes et françaises CLXXIII. Geneva: Droz.


NORMALIZER
==================
The normalizer aims to maximally reduce the variation between the orthography of texts written in the `Anglo-Norman dialect <https://en.wikipedia.org/wiki/Anglo-Norman_language>`_ to bring it in line with “orthographe commune”.
It is heavily inspired by Pope (1956). It takes a string as its input. Spelling variation is not consistent enough to ensure the highest accuracy; the normalizer should therefore be used as a last resort.

.. code-block:: python

    In [1]: from cltk.corpus.utils.formatter import normalize_fr

    In [2]: text = "viw"

    In [3]: normalize_fr(text)
    Out [3]: ['vieux']

.. Reference: Pope, M.K. 1956. From Latin to Modern French with Especial Consideration of Anglo-Norman. Manchester: MUP.


STEMMER
==================
The stemmer strips morphological endings from an input string.
.. Morphological endings are taken from Brunot & Bruneau (1949) and include both nominal and verbal inflexion. A list of exceptions can be found at cltk.stem.french.exceptions.

.. code-block:: python

    In [1]: from cltk.stem.french.stem import stem

    In [2]: text = "ja departissent a itant quant par la vile vint errant tut a cheval une pucele en tut le siecle n’ot si bele un blanc palefrei chevalchot"

    In [3]: stem(text)
    Out [3]: "j depart a it quant par la vil v err tut a cheval un pucel en tut le siecl n' o si bel un blanc palefre chevalcho"

.. Reference: Brunot, F. & Bruneau, C. 1949. Précis de grammaire historique de la langue française. Paris: Masson & Cie.


STOPWORD FILTERING
==================
The stopword filterer removes the function words from a string of OF or MF text. The list includes function words from the most common 100 words in the corpus, as well as all conjugated forms of auxiliaries estre and avoir.

.. code-block:: python

    In [1]: from cltk.stop.french.stops import STOPS_LIST as FRENCH_STOPS

    In [2]: from cltk.tokenize.word import WordTokenizer

    In [3]: tokenizer = WordTokenizer('french')

    In [4]: text = "En pensé ai e en talant que d’ Yonec vus die avant dunt il fu nez, e de sun pere cum il vint primes a sa mere ."

    In [5]: text = text.lower()

    In [6]: tokens = tokenizer.tokenize(text)

    In [7]: no_stops = [w for w in tokens if w not in FRENCH_STOPS]

    In [8]: no_stops
    Out [8]: ['pensé', 'talant', 'yonec', 'die', 'avant', 'dunt', 'nez', ',', 'pere', 'cum', 'primes', 'mere', '.']



WORD TOKENIZATION
==================
.. code-block:: python

    In [1]: from cltk.tokenize.word import WordTokenizer

    In [2]: word_tokenizer = WordTokenizer('french')

    In [3]: text = "S'a table te veulz maintenir, Honnestement te dois tenir Et garder les enseignemens Dont cilz vers sont commancemens."

    In [4]: word_tokenizer.tokenize(text)
    Out [4]: ["S'", 'a', 'table', 'te', 'veulz', 'maintenir', ',', 'Honnestement', 'te', 'dois', 'tenir', 'Et', 'garder', 'les', 'enseignemens', 'Dont', 'cilz', 'vers', 'sont', 'commancemens', '.']


Apostrophes are considered part of the first word of the two they separate. Apostrophes are also normalized from “’” to “'“.


Swadesh
=======

.. code-block:: python

 In [1]: from cltk.corpus.swadesh import Swadesh
 
 In [2]: swadesh = Swadesh('fr_old')
 
 In [3]: swadesh.words()[:10]
 Out[3]: ['jo, jou, je, ge', 'tu', 'il', 'nos, nous', 'vos, vous', 'il, eles', 'cist, cest, cestui', 'ci', 'la']
