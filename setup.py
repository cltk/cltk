"""Config for PyPI."""

import os

from setuptools import find_packages
from setuptools import setup


setup(
    author='Kyle P. Johnson',
    author_email='kyle@kyle-p-johnson.com',
    classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: English',
        'Natural Language :: Greek',
        'Natural Language :: Latin',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
    ],
    description='NLP for the ancient world',
    install_requires=['fuzzywuzzy',
                      'gitpython',
                      'nltk',
                      'python-Levenshtein',
                      'pyuca',
                      'pyyaml',
                      'regex',
                      'whoosh'],
    keywords=['nlp', 'nltk', 'greek', 'latin', 'chinese', 'sanskrit', 'pali', 'tibetan'],
    license='MIT',
    long_description='The Classical Language Toolkit (CLTK) is a framework for natural language processing for Classical languages.',  # pylint: disable=C0301,
    name='cltk',
    packages=find_packages(),
    url='https://github.com/cltk/cltk',
    version='0.1.46',
    zip_safe=True,
    test_suite='cltk.tests.test_cltk',
)
