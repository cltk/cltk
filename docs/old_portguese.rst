Old Portuguese
***********

Galician-Portuguese (Galician: galego-portugués or galaico-portugués, Portuguese: galego-português or galaico-português), also known as Old Portuguese or Medieval Galician, was a West Iberian Romance language spoken in the Middle Ages, in the northwest area of the Iberian Peninsula. Alternatively, it can be considered a historical period of the Galician and Portuguese languages.
(Source: `Wikipedia <https://en.wikipedia.org/wiki/Galician-Portuguese>`_)

Swadesh
=======
The corpus module has a class for generating a Swadesh list for Old Portuguese.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('pt_old')

   In [3]: swadesh.words()[:10]
   Out[3]: ['eu', 'tu', 'ele', 'nos', 'vos', 'eles', 'esto, aquesto', 'aquelo', 'aqui', 'ali']