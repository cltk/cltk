"""Config for PyPI."""

from setuptools import find_packages
from setuptools import setup

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
    version='0.0.1.6',
    zip_safe=True,
    test_suite='cltk.tests.test_cltk',
)
