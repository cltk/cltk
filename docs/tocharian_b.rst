Tocharian B
***********

Tocharian, also spelled Tokharian (/təˈkɛəriən/ or /təˈkɑːriən/), is an extinct branch of the Indo-European language family. It is known from manuscripts dating from the 6th to the 8th century AD, which were found in oasis cities on the northern edge of the Tarim Basin (now part of Xinjiang in northwest China). The discovery of these languages in the early 20th century contradicted the formerly prevalent idea of an east–west division of Indo-European language family on the centum–satem isogloss, and contributed to re-invigorate study of the family. Identifying the authors with the Tokharoi people of ancient Bactria (Tokharistan), early authors called these languages "Tocharian". Although this identification is now generally considered mistaken, the name has stuck.

The documents record two closely related languages, called Tocharian A ("East Tocharian", Agnean or Turfanian) and Tocharian B ("West Tocharian" or Kuchean). The subject matter of the texts suggests that Tocharian A was more archaic and used as a Buddhist liturgical language, while Tocharian B was more actively spoken in the entire area from Turfan in the east to Tumshuq in the west
(Source: `Wikipedia <https://en.wikipedia.org/wiki/Tocharian_languages>`_)

Swadesh
=======
The corpus module has a class for generating a Swadesh list for Tocharian B.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('txb')

   In [3]: swadesh.words()[:10]
   Out[3]: ['ñäś', 'tuwe', 'su', 'wes', 'yes', 'cey', 'se', 'su, samp', 'tane', 'tane, omp']