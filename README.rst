|circleci| |pypi| |twitter| |discord|


.. |circleci| image:: https://circleci.com/gh/cltk/cltk/tree/master.svg?style=svg
   :target: https://circleci.com/gh/cltk/cltk/tree/master

.. |rtd| image:: https://img.shields.io/readthedocs/cltk
   :target: http://docs.cltk.org/

.. |codecov| image:: https://codecov.io/gh/cltk/cltk/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/cltk/cltk

.. |pypi| image:: https://img.shields.io/pypi/v/cltk
   :target: https://pypi.org/project/cltk/

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3445585.svg
   :target: https://doi.org/10.5281/zenodo.3445585

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/cltk/tutorials/master

.. |twitter| image:: https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2FCLTKorg&label=Follow%20%40CLTKorg
   :target: https://twitter.com/CLTKorg
   
.. |discord| image:: https://img.shields.io/discord/974033391542480936
   :target: https://discord.gg/ATUDJQX7cg
 
The Classical Language Toolkit (CLTK) is a Python library offering natural language processing (NLP) for pre-modern languages.


Installation
============

For the CLTK's latest version:

.. code-block:: bash

   $ pip install cltk

For more information, see `Installation docs <https://docs.cltk.org/en/latest/installation.html>`_ or, to install from source, `Development <https://docs.cltk.org/en/latest/development.html>`_.

Pre-1.0 software remains available on the `branch v0.1.x <https://github.com/cltk/cltk/tree/v0.1.x>`_ and docs at `<https://legacy.cltk.org>`_. Install it with ``pip install "cltk<1.0"``.


Documentation
=============

Documentation at `<https://docs.cltk.org>`_.


Citation
========

When using the CLTK, please cite `the following publication <https://aclanthology.org/2021.acl-demo.3>`_, including the DOI:

   Johnson, Kyle P., Patrick J. Burns, John Stewart, Todd Cook, Clément Besnier, and William J. B.  Mattingly. "The Classical Language Toolkit: An NLP Framework for Pre-Modern Languages." In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations*, pp. 20-29. 2021. 10.18653/v1/2021.acl-demo.3


The complete BibTeX entry:

.. code-block:: bibtex

   @inproceedings{johnson-etal-2021-classical,
       title = "The {C}lassical {L}anguage {T}oolkit: {A}n {NLP} Framework for Pre-Modern Languages",
       author = "Johnson, Kyle P.  and
         Burns, Patrick J.  and
         Stewart, John  and
         Cook, Todd  and
         Besnier, Cl{\'e}ment  and
         Mattingly, William J. B.",
       booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
       month = aug,
       year = "2021",
       address = "Online",
       publisher = "Association for Computational Linguistics",
       url = "https://aclanthology.org/2021.acl-demo.3",
       doi = "10.18653/v1/2021.acl-demo.3",
       pages = "20--29",
       abstract = "This paper announces version 1.0 of the Classical Language Toolkit (CLTK), an NLP framework for pre-modern languages. The vast majority of NLP, its algorithms and software, is created with assumptions particular to living languages, thus neglecting certain important characteristics of largely non-spoken historical languages. Further, scholars of pre-modern languages often have different goals than those of living-language researchers. To fill this void, the CLTK adapts ideas from several leading NLP frameworks to create a novel software architecture that satisfies the unique needs of pre-modern languages and their researchers. Its centerpiece is a modular processing pipeline that balances the competing demands of algorithmic diversity with pre-configured defaults. The CLTK currently provides pipelines, including models, for almost 20 languages.",
   }


License
=======

.. |year| date:: %Y

Copyright (c) 2014-|year| Kyle P. Johnson under the `MIT License <https://github.com/cltk/cltk/blob/master/LICENSE>`_.
