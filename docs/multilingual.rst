Multilingual
*************

Some functions in the CLTK are language independent.

Concordance
===========

.. note:: This is a new feature. Advice regarding readability is encouraged!

The ``philology`` module can produce a concordance. Currently there are two methods that write a concordance to file, one which takes one or more paths and another which takes a text string. Texts in Latin characters are alphabetized.

.. code-block:: python

   In [1]: from cltk.utils.philology import Philology

   In [2]: p = Philology()

   In [3]: iliad = '~/cltk_data/greek/text/tlg/individual_works/TLG0012.TXT-001.txt'

   In [4]: p.write_concordance_from_file(iliad, 'iliad')


This will print a traditional, human–readable, 120,000–line concordance at ``~/cltk_data/user_data/concordance_iliad.txt``.

Multiple files can be passed as a list into this method.

   In [5]: odyssey = '~/cltk_data/greek/text/tlg/individual_works/TLG0012.TXT-002.txt'

   In [6]: p.write_concordance_from_file([iliad, odyssey], 'homer')

This creates the file ``~/cltk_data/user_data/concordance_homer.txt``.

``write_concordance_from_string()`` takes a string and will build the concordance from it.


.. code-block:: python

   In [7]: from cltk.corpus.utils.formatter import phi5_plaintext_cleanup

   In [8]: import os

   In [9]: tibullus = os.path.expanduser('~/cltk_data/latin/text/phi5/plaintext/LAT0660.TXT')

   In [10]: with open(tibullus) as f:
   ....:     tib_read = f.read()

   In [10]: tib_clean = phi5_plaintext_cleanup(tib_read).lower()

   In [11]: p.write_concordance_from_string(tib_clean, 'tibullus')

The resulting concordance looks like:

.. code-block

   modulatus eburno felices cantus ore sonante dedit. sed postquam fuerant digiti cum voce locuti , edidit haec tristi dulcia verba modo : 'salve , cura
    caveto , neve cubet laxo pectus aperta sinu , neu te decipiat nutu , digitoque liquorem ne trahat et mensae ducat in orbe notas. exibit quam saepe ,
    acerbi : non ego sum tanti , ploret ut illa semel. nec lacrimis oculos digna est foedare loquaces : lena nocet nobis , ipsa puella bona est. lena ne
   eaera tamen.” “carmine formosae , pretio capiuntur avarae. gaudeat , ut digna est , versibus illa tuis. lutea sed niveum involvat membrana libellum ,
   umnus olympo mille habet ornatus , mille decenter habet. sola puellarum digna est , cui mollia caris vellera det sucis bis madefacta tyros , possidea
    velim , sed peccasse iuvat , voltus conponere famae taedet : cum digno digna fuisse ferar. invisus natalis adest , qui rure molesto et sine cerintho
   a phoebe superbe lyra. hoc sollemne sacrum multos consummet in annos : dignior est vestro nulla puella choro. parce meo iuveni , seu quis bona pascua
  a para. sic bene conpones : ullae non ille puellae servire aut cuiquam dignior illa viro. nec possit cupidos vigilans deprendere custos , fallendique




Corpora
=======

The CLTK uses languages in its organization of data, however some good corpora do not and cannot be easily broken apart. Furthermore, some, such as parallel text corpora, are inherently multilingual. Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``multilingual_``) to discover available multilingual corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('multilingual')

   In [3]: c.list_corpora
   Out[3]: ['multilingual_treebank_proiel']

