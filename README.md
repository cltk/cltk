The Classical Language Toolkit
==============================

[![PyPi downloads](http://img.shields.io/pypi/v/cltk.svg?style=flat)](https://pypi.python.org/pypi/cltk/) [![PyPI version](http://img.shields.io/pypi/dm/cltk.svg?style=flat)](https://pypi.python.org/pypi/cltk/)  [![Build Status](https://travis-ci.org/cltk/cltk.svg?branch=master)](https://travis-ci.org/cltk/cltk) [![Coverage Status](https://coveralls.io/repos/kylepjohnson/cltk/badge.svg?branch=master)](https://coveralls.io/r/kylepjohnson/cltk?branch=master) [![codecov.io](http://codecov.io/github/kylepjohnson/cltk/coverage.svg?branch=master)](http://codecov.io/github/kylepjohnson/cltk?branch=master) [![Dependency Status](https://gemnasium.com/kylepjohnson/cltk.svg)](https://gemnasium.com/kylepjohnson/cltk) [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.32167.svg)](http://dx.doi.org/10.5281/zenodo.32540)

[![Join the chat at https://gitter.im/kylepjohnson/cltk](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/kylepjohnson/cltk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


About
-----

The Classical Language Toolkit (CLTK) offers natural language processing support for Classical languages. In some areas, it extends the NLTK. The goals of the CLTK are to:

*   compile analysis-friendly corpora in a variety of Classical languages (currently available for Chinese, Coptic, Greek, Latin, Pali, and Tibetan);
*   gather, improve, and generate linguistic data required for NLP (Greek and Latin are in progress, with [more in the pipeline](https://github.com/kylepjohnson/cltk/wiki/List-of-Classical-languages));
*   develop a free and open platform for generating reproducible, scientific research that advances the study of the languages and literatures of the ancient world.


Installation
------------

See [installation instructions available in the docs](http://docs.cltk.org/en/latest/installation.html).


Documentation
-------------

The docs are at [docs.cltk.org](http://docs.cltk.org). More information is available on the CLTK's website, [cltk.org](http://cltk.org).


Corpora, training sets, models, etc.
------------------------------------

Corpora are kept in [the CLTK's GitHub user group](https://github.com/cltk). A language's trained models are found in, e.g., [`latin_models_cltk`](https://github.com/cltk/latin_models_cltk) and [`greek_models_cltk`](https://github.com/cltk/greek_models_cltk). The CLTK imports files and stores them locally to your computer at `~/cltk_data`.


Citation
--------

Each major release of the CLTK is given a [DOI](http://en.wikipedia.org/wiki/Digital_object_identifier), a type of unique identity for digital documents. This DOI ought to be included in your citation, as it will allow your readers to reproduce your scholarship should the CLTK's API or codebase change. To find the CLTK's current DOI, observe the blue `DOI` button in the repository's home on GitHub. To the end of your bibliographic entry, append `DOI ` plus the current identifier.

Therefore, please cite as follows: 
```
Kyle P. Johnson et al.. (2014-2015). CLTK: The Classical Language Toolkit. DOI 10.5281/zenodo.<current_release_id>
```

A style-neutral BibTeX entry would look like this:
```
@Misc{johnson2014,
author = {Kyle P. Johnson et al.},
title = {CLTK: The Classical Language Toolkit},
howpublished = {\url{https://github.com/cltk/cltk}},
note = {{DOI} 10.5281/zenodo.<current_release_id>},
year = {2014--2015},
}
```

You may also add version/release number, located in the `pypi` button at the project's GitHub repository homepage.


License
-------

The CLTK is Copyright (c) 2015 Kyle P. Johnson, under the MIT License. See 'LICENSE' for details.
