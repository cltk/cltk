"""Install the Lapos POS tagger."""

import os
import subprocess
from sys import platform


from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.utils.importer import CorpusImportError
from cltk.utils.cltk_logger import logger


class Lapos:
    """Class for everything pertaining to installing Lapos."""

    def __init__(self, language):
        """Constructor."""
        self.language = language
        self.operating_system = self._what_os()
        self._is_cloned_get_make()  # get software if not present

    def _is_cloned_get_make(self):
        """Check if installed, if not, install it.
        TODO: This could be 3 functions.
        """
        # ! add check here for mac or unix
        if self.operating_system == 'mac':
            branch = 'apple'
        else:
            branch = 'master'
        fp = os.path.expanduser('~/cltk_data/multilingual/software/lapos/README.md')
        if os.path.isfile(fp):
            return True
        else:
            importer = CorpusImporter('multilingual')
            importer.import_corpus('lapos', branch=branch)
        if os.path.isfile(fp):
            print('Cloned Lapos successfully.')
            self.make()
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

    def tag_sentence(self, sentence):
        """Tag using Lapos model.

        TODO: Figure out how to pre-load model (loading is slow). Or force users to bulk-convert files or strings.
        """
        fp_lapos = os.path.expanduser('~/cltk_data/multilingual/software/lapos')
        fp_model = os.path.expanduser('~/cltk_data/{0}/model/{1}_models_cltk/taggers/pos'.format(self.language, self.language))  # rel from Lapos dir
        try:
            p_out = subprocess.check_output('cd {0} && echo "{1}" | ./lapos -t -m {2}'.format(fp_lapos, sentence, fp_model),
                                            shell=True,
                                            stderr=subprocess.STDOUT,
                                            universal_newlines=True)
        except subprocess.CalledProcessError as cp_err:
            logger.error('Lapos call failed. Check installation.')
            logger.error(sentence)
            print(cp_err)
            raise

        # Parse output from Lapos
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
    l = Lapos('latin')
    s = "Quis novus hic nostris successit sedibus hospes.".lower()
    print(l.tag_sentence(s))
