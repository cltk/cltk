# The Classical Language Toolkit

[![PyPi downloads](http://img.shields.io/pypi/v/cltk.svg?style=flat)](https://pypi.python.org/pypi/cltk/) [![PyPI version](http://img.shields.io/pypi/dm/cltk.svg?style=flat)](https://pypi.python.org/pypi/cltk/) [![Dependency Status](https://gemnasium.com/kylepjohnson/cltk.svg)](https://gemnasium.com/kylepjohnson/cltk) [![Documentation Status](https://readthedocs.org/projects/cltk/badge/?version=latest)](http://docs.cltk.org/en/latest/?badge=latest)

[![Build Status](https://travis-ci.org/cltk/cltk.svg?branch=master)](https://travis-ci.org/cltk/cltk) [![Coverage Status](https://coveralls.io/repos/kylepjohnson/cltk/badge.svg?branch=master)](https://coveralls.io/r/kylepjohnson/cltk?branch=master) [![codecov.io](http://codecov.io/github/cltk/cltk/coverage.svg?branch=master)](http://codecov.io/github/cltk/cltk?branch=master) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/ac803b087b1543e190dc31224dd7f4bf/badge.svg)](https://www.quantifiedcode.com/app/project/ac803b087b1543e190dc31224dd7f4bf) 

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.44555.svg)](http://dx.doi.org/10.5281/zenodo.44555)

<a href="https://zenhub.io"><img src="https://raw.githubusercontent.com/ZenHubIO/support/master/zenhub-badge.png"></a>

[![Join the chat at https://gitter.im/cltk/cltk](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cltk/cltk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## About

The Classical Language Toolkit (CLTK) offers natural language processing support for Classical languages. In some areas, it extends the NLTK. The goals of the CLTK are to:

*   compile analysis-friendly corpora in a variety of Classical languages (currently available for Chinese, Coptic, Greek, Latin, Pali, and Tibetan);
*   gather, improve, and generate linguistic data required for NLP (Greek and Latin are in progress, with [more in the pipeline](https://github.com/cltk/cltk/wiki/List-of-Classical-languages));
*   develop a free and open platform for generating reproducible, scientific research that advances the study of the languages and literatures of the ancient world.


## Documentation

The docs are at [docs.cltk.org](http://docs.cltk.org).


### Installation

``` bash
$ pip install cltk
```

See docs for [complete installation instructions](http://docs.cltk.org/en/latest/installation.html).

The [CLTK organization curates corpora](https://github.com/cltk) which can download directly or, better, [imported by the toolkit](http://docs.cltk.org/en/latest/importing_corpora.html).


## Contributing

See the [Quickstart for contributors](https://github.com/cltk/cltk/wiki/Quickstart-for-contributors) for an overview of the process. If you're looking to start with a small contribution, see the [Issue tracker for "easy" jobs](https://github.com/cltk/cltk/issues?q=is%3Aopen+is%3Aissue+label%3Aeasy) needing to be done. Bigger projects may be found at [Project ideas](https://github.com/cltk/cltk/wiki/Project-ideas) page. Of course, new ideas are always welcome.


## Citation

Each major release of the CLTK is given a [DOI](http://en.wikipedia.org/wiki/Digital_object_identifier), a type of unique identity for digital documents. This DOI ought to be included in your citation, as it will allow researcher to reproduce your results should the CLTK's API or codebase change. To find the CLTK's current DOI, observe the blue `DOI` button in the repository's home on GitHub. To the end of your bibliographic entry, append `DOI ` plus the current identifier. You may also add version/release number, located in the `pypi` button at the project's GitHub repository homepage.

Thus, please cite core software as something like:
```
Kyle P. Johnson et al.. (2014-2016). CLTK: The Classical Language Toolkit. DOI 10.5281/zenodo.<current_release_id>
```

A style-neutral BibTeX entry would look like this:
```
@Misc{johnson2014,
author = {Kyle P. Johnson et al.},
title = {CLTK: The Classical Language Toolkit},
howpublished = {\url{https://github.com/cltk/cltk}},
note = {{DOI} 10.5281/zenodo.<current_release_id>},
year = {2014--2016},
}
```

[Many contributors](https://github.com/cltk/cltk/blob/master/contributors.md) have made substantial contributions to the CLTK. For scholarship about particular code, it might be proper to cite these individuals as authors of the work under discussion.


## License

The CLTK is Copyright (c) 2016 Kyle P. Johnson, under the MIT License. See '[LICENSE](https://github.com/cltk/cltk/blob/master/LICENSE)' for details.
