"""Install the Lapos POS tagger."""

import os
import subprocess
from subprocess import Popen, PIPE
from sys import platform


from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.utils.importer import CorpusImportError
from cltk.utils.cltk_logger import logger


class Lapos:
    """Class for everything pertaining to installing Lapos."""

    def __init__(self):
        """Constructor."""
        self.operating_system = self._what_os()
        self._is_cloned_get()  # get software if not present
        self.commands = {'evaluate': 'lapos-evaluate',
                         'train': 'lapos-learn',
                         'tag': 'lapos'}

    def _is_cloned_get(self):
        """Check if installed, if not, install it.
        TODO: This could be 2 functions.
        """
        # ! add check here for mac or unix
        if self.operating_system == 'mac':
            branch = 'clang'
        else:
            branch = 'master'
        fp = os.path.expanduser('~/cltk_data/multilingual/software/lapos/README.md')
        if os.path.isfile(fp):
            return True
        else:
            importer = CorpusImporter('multilingual')
            importer.import_corpus('lapos', branch=branch)
        if os.path.isfile(fp):
            print('Cloned Lapos OK.')
            return True
        else:
            logger.error("Something went wrong with importing the Lapos tagger on the '{}' branch.".format(branch))
            raise CorpusImportError

    def _what_os(self):
        """Get operating system."""
        if platform == "linux" or platform == "linux2":
            _platform = 'linux'
        elif platform == "darwin":
            _platform = 'mac'
        elif platform == "win32":
            _platform = 'windows'
        logger.info("Detected '{}' operating system.".format(_platform))

        return _platform

    def make(self):
        """Build program."""
        fp = os.path.expanduser('~/cltk_data/multilingual/software/lapos')
        p_out = subprocess.call('cd {} && make'.format(fp), shell=True, stdout=subprocess.DEVNULL)

        if p_out == 0:
            print('Lapos built successfully.')
            logger.info('Lapos build successfully.')
        else:
            print('Lapos did not build successfully.')
            logger.error('Lapos did not build successfully.')

    def train(self):
        """Train new Lapos model."""
        fp = os.path.expanduser('~/cltk_data/multilingual/software/lapos')

        p_out = subprocess.call('cd {} && ./lapos-learn -m . samples/train.pos '.format(fp),
                                shell=True,
                                stdout=subprocess.DEVNULL)

        if p_out == 0:
            print('Lapos built successfully.')
            logger.info('Lapos built model successfully.')
        else:
            print('Lapos did not build successfully.')
            logger.error('Lapos did not build model successfully.')

    def tag_file_example(self):
        """Tag using Lapos model."""
        fp = os.path.expanduser('~/cltk_data/multilingual/software/lapos')
        try:
            p_out = subprocess.check_output('cd {} && ./lapos -m . < samples/test.txt'.format(fp),
                                            shell=True,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=True)
        except subprocess.CalledProcessError as cp_err:
            logger.error('Lapos call failed.')
            print(cp_err)
            raise

        # Parse output from Laops
        # TODO: Make this cleaner/faster
        output_list = p_out.split('\n')
        output_list_filtered = [l for l in output_list if not l.startswith('loading the models')]
        output_list_filtered = [l for l in output_list_filtered if not l == 'done']
        output_list_filtered = [l for l in output_list_filtered if l]


        tagged_sentences = []
        for line in output_list_filtered:
            word_tags = line.split(' ')
            tagged_sentence = []
            for word_tag in word_tags:
                word, tag = word_tag.split('/')
                word_tag_tuple = (word, tag)
                tagged_sentence.append(word_tag_tuple)

            tagged_sentences.append(tagged_sentence)

        return tagged_sentences

    def tag_sentence(self, sentence):
        """Tag using Lapos model."""
        fp = os.path.expanduser('~/cltk_data/multilingual/software/lapos')
        try:
            p_out = subprocess.check_output('cd {0} && echo {1}| ./lapos -t -m .'.format(fp, sentence),
                                            shell=True,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=True)
        except subprocess.CalledProcessError as cp_err:
            logger.error('Lapos call failed.')
            print(cp_err)
            raise

        # Parse output from Laops
        # TODO: Make this cleaner/faster
        output_list = p_out.split('\n')
        output_list_filtered = [l for l in output_list if not l.startswith('loading the models')]
        output_list_filtered = [l for l in output_list_filtered if not l == 'done']
        output_list_filtered = [l for l in output_list_filtered if l]

        for line in output_list_filtered:
            word_tags = line.split(' ')
            tagged_sentence = []
            for word_tag in word_tags:
                word, tag = word_tag.split('/')
                word_tag_tuple = (word, tag)
                tagged_sentence.append(word_tag_tuple)

            return tagged_sentence


if __name__ == '__main__':
    l = Lapos()
    print(l.tag_sentence('The involvement of ion channels in B and T lymphocyte activation'))