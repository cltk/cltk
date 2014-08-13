"""Config for PyPI"""

from setuptools import find_packages
from setuptools import setup

setup(
    author='Kyle P. Johnson',
    author_email='kyle@kyle-p-johnson.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Greek',
        'Natural Language :: Latin',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
    description=('NLP support for Ancient Greek and Latin'),
    keywords=['nlp', 'ancient greek', 'latin', 'tlg', 'phi', 'literature'],
    license='MIT',
    long_description="""The Classical Language Toolkit (CLTK) is a \
suite of tools assisting natural language processing for the Ancient Greek \
and Latin languages. It is developed in Python 3.4.""",
    name='cltk',
    packages=find_packages(),
    url='https://github.com/kylepjohnson/cltk',
    version='0.0.0.21',
    zip_safe=True,
    test_suite = 'cltk.tests.test_cltk',
)
