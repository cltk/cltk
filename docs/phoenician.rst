Phoenician was a language originally spoken in the coastal (Mediterranean) region then called "Canaan". It is a part of the Canaanite subgroup of the Northwest Semitic languages. It was also spoken in the area of Phoenician colonization along the coasts of the southwestern Mediterranean Sea. Phoenician, together with Punic, is primarily known from approximately 10,000 surviving inscriptions, supplemented by occasional glosses in books written in other languages. The Phoenician alphabet is the oldest verified consonantal alphabet, or abjad. It has become conventional to refer to the script as "Proto-Canaanite" until the mid-11th century BCE, when it is first attested on inscribed bronze arrowheads, and as "Phoenician" only after 1050 BCE. The Phoenician phonetic alphabet is generally believed to be at least the partial ancestor of almost all modern alphabets. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Phoenician_language>`_)

Swadesh
=======
The corpus module has a class for generating a Swadesh list for Latin.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import swadesh_phn

   In [2]: print(swadesh_phn[:10])
   ['‘l', '‘ḥr', 'kl', 'mzbḥ', 'w', 'mšḥ', '‘ny', 'qrb?', 'zr’', 'ṣb’']

   In [3]: print(len(swadesh_phn))
   320
