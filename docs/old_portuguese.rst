Old Portuguese
**************

Galician-Portuguese, also known as Old Portuguese or Medieval Galician, was a West Iberian Romance language spoken in the Middle Ages, in the northwest area of the Iberian Peninsula. Alternatively, it can be considered a historical period of the Galician and Portuguese languages. The language was used for literary purposes from the final years of the 12th century to roughly the middle of the 14th century in what are now Spain and Portugal and was, almost without exception, the only language used for the composition of lyric poetry. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Galician-Portuguese>`_)

Swadesh
=======
The corpus module has a class for generating a Swadesh list for Old Portuguese.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('pt_old')

   In [3]: swadesh.words()[:10]
   Out[3]: ['eu', 'tu', 'ele', 'nos', 'vos', 'eles', 'esto, aquesto', 'aquelo', 'aqui', 'ali']
