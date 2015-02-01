"""Config for PyPI."""

from collections import OrderedDict
import importlib.machinery
from setuptools import find_packages
from setuptools import setup
import os
from pprint import pprint


def build_contribs_file():
    """Recursively scan ``cltk`` dir for ``.py`` files and read
    ``__author__``, then build a dictionary index of
    'author': [files contributed to], and write it to file.
    """
    py_files_list = []
    for dir_path, dir_names, files in os.walk('cltk'):  # pylint: disable=W0612
        for name in files:
            if name.lower().endswith('.py') and not name.lower().startswith('__init__'):
                py_files_list.append(os.path.join(dir_path, name))

    file_author = {}
    # get all authors in each file
    for py_file in py_files_list:
        loader = importlib.machinery.SourceFileLoader('__author__', py_file)
        mod = loader.load_module()
        mod_path = mod.__file__

        # check if author value is a string, turn to list
        if type(mod.__author__) is str:
            authors = [mod.__author__]
        elif type(mod.__author__) is list:
            authors = mod.__author__
        else:
            print('ERROR bad __author__ type: ', mod.__author__, type(mod.__author__))

        # get all authors
        for author in authors:
            if author not in file_author:
                file_author[author] = [mod_path]
            else:
                file_author[author].append(mod_path)

    # order dict by contrib's first name
    file_author_ordered = OrderedDict(sorted(file_author.items()))

    with open('contributors.txt', 'w') as contrib_f:
        pprint(file_author_ordered, contrib_f)

setup(
    author='Kyle P. Johnson',
    author_email='kyle@kyle-p-johnson.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
    description='NLP support for Classical languages.',
    install_requires=['nltk',
                      'requests',
                      'requests-toolbelt',
                      'numpy',
                      'cltk'],
    keywords=['nlp', 'nltk', 'greek', 'latin'],
    license='MIT',
    long_description="The Classical Language Toolkit (CLTK) is a framework for natural language processing for Classical languages.",  # pylint: disable=C0301
    name='cltk',
    packages=find_packages(),
    url='https://github.com/kylepjohnson/cltk',
    version='0.0.1.3',
    zip_safe=True,
    test_suite='cltk.tests.test_cltk',
)

#build_contribs_file()
