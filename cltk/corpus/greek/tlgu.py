"""Wrapper for `tlgu` command line utility.

Original software at: ``http://tlgu.carmen.gr/``.

TODO: the arguments to ``convert_corpus()`` need some rationalization, and
``divide_works()`` should be incorporated into it.
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from cltk.utils.cltk_logger import logger
from cltk.corpus.utils.importer import CorpusImporter
import os
import subprocess


# this currently not in use
ARGS = {
    'book_breaks': '-b',
    'page_breaks': '-p',
    'latin_text': '-r',
    'level_1': '-v',
    'level_2': '-w',
    'level_3': '-x',
    'level_4': '-y',
    'level_5': '-z',
    'line_tab': '-B',
    'higher_levels': '-X',
    'lower_levels': '-Y',
    'no_spaces': '-N',  # break_lines
    'citation_debug': '-C',
    'code_debug': '-S',
    'verbose': '-V',
    'split_works': '-W'
}


class TLGU(object):
    """Check, install, and call TLGU."""
    def __init__(self, testing=False):
        """Check whether tlgu is installed, if not, import and install."""
        self.testing = testing
        self._check_import_source()
        self._check_install()

    @staticmethod
    def _check_import_source():
        """Check if tlgu imported, if not import it."""
        path_rel = '~/cltk_data/greek/software/greek_software_tlgu/tlgu.h'
        path = os.path.expanduser(path_rel)
        if not os.path.isfile(path):
            try:
                corpus_importer = CorpusImporter('greek')
                corpus_importer.import_corpus('tlgu')
            except Exception as exc:
                logger.error('Failed to import TLGU: %s', exc)
                raise

    def _check_install(self):
        """Check if tlgu installed, if not install it."""
        try:
            subprocess.check_output(['which', 'tlgu'])
        except Exception as exc:
            logger.info('TLGU not installed: %s', exc)
            logger.info('Installing TLGU.')
            if not subprocess.check_output(['which', 'gcc']):
                logger.error('GCC seems not to be installed.')
            else:
                tlgu_path_rel = '~/cltk_data/greek/software/greek_software_tlgu'
                tlgu_path = os.path.expanduser(tlgu_path_rel)
                if not self.testing:
                    print('Do you want to install TLGU? To continue, press Return. To exit, Control-C.')
                    input()
                else:
                    print('Automated or test build, skipping keyboard input confirmation for installation of TLGU.')
                try:
                    p_out = subprocess.call('cd {0} && make install'.format(tlgu_path), shell=True)
                    if p_out == 0:
                        logger.info('TLGU installed.')
                    else:
                        logger.error('TLGU install without sudo failed.')
                except Exception as exc:
                    logger.error('TLGU install failed: %s', exc)
                else:  # for Linux needing root access to '/usr/local/bin'
                    p_out = subprocess.call('cd {0} && sudo make install'.format(tlgu_path), shell=True)
                    if p_out == 0:
                        logger.info('TLGU installed.')
                    else:
                        logger.error('TLGU install with sudo failed.')

    def convert(self, input_path=None, output_path=None, markup=None,
                break_lines=False, divide_works=False, latin=False,
                extra_args=None):
        """
        :param input_path: TLG filepath to convert.
        :param output_path: filepath of new converted text.
        :param markup: Specificity of inline markup. Default None removes all
        numerical markup; 'full' gives most detailed, with reference numbers
        included before each text line.
        :param break_lines: No spaces; removes line ends and hyphens before an
         ID code; hyphens and spaces before page and column ends are retained.
        :param divide_works: Each work (book) is output as a separate file in
        the form output_file-xxx.txt; if an output file is not specified, this
         option has no effect.
        :param latin: Primarily Latin text (PHI). Some TLG texts, notably
        doccan1.txt and doccan2.txt are mostly roman texts lacking explicit
        language change codes. Setting this option will force a change to
        Latin text after each citation block is encountered.
        :param extra_args: Any other tlgu args to be passed, in list form and
        without dashes, e.g.: ['p', 'b', 'B'].
        """
        # setup file paths
        input_path = os.path.expanduser(input_path)
        output_path = os.path.expanduser(output_path)

        # check input path exists
        assert os.path.isfile(input_path), 'File {0} does not exist.'.format(input_path)

        # setup tlgu flags
        tlgu_options = []
        if markup == 'full':
            full_args = ['v', 'w', 'x', 'y', 'z']
            [tlgu_options.append(x) for x in full_args]  # pylint: disable=W0106
        if break_lines:
            tlgu_options.append('N')
        if divide_works:
            tlgu_options.append('W')
        if latin:
            tlgu_options.append('r')
        # setup extra args
        if extra_args is None:
            extra_args = []
        else:
            try:
                extra_args = list(extra_args)
            except Exception as exc:
                logger.error("Argument 'extra_args' must be a list: %s.", exc)
                raise
        tlgu_options = tlgu_options + extra_args
        # assemble all tlgu flags
        tlgu_options = list(set(tlgu_options))
        if tlgu_options:
            tlgu_flags = '-' + ' -'.join(tlgu_options)
        else:
            tlgu_flags = ''
        # make tlgu call
        tlgu_call = 'tlgu {0} {1} {2}'.format(tlgu_flags,
                                              input_path,
                                              output_path)
        logger.info(tlgu_call)
        try:
            p_out = subprocess.call(tlgu_call, shell=True)
            if p_out == 1:
                logger.error('Failed to convert %s to %s.',
                             input_path,
                             output_path)
        except Exception as exc:
            logger.error('Failed to convert %s to %s: %s',
                         input_path,
                         output_path,
                         exc)
            raise

    def convert_corpus(self, corpus, markup=None, break_lines=False, divide_works=False, latin=None, extra_args=None):  # pylint: disable=W0613
        """Look for imported TLG or PHI files and convert them all to
        ``~/cltk_data/greek/text/tlg/<plaintext>``.
        TODO: Should this and/or convert() be static?
        TODO: Add markup options to input.
        TODO: Do something with break_lines, divide_works, and extra_args or rm them
        """
        orig_path_rel = '~/cltk_data/originals'
        orig_path = os.path.expanduser(orig_path_rel)
        target_path_rel = '~/cltk_data'
        target_path = os.path.expanduser(target_path_rel)
        assert corpus in ['tlg', 'phi5', 'phi7'], "Corpus must be 'tlg', 'phi5', or 'phi7'"
        if corpus in ['tlg', 'phi5', 'phi7']:
            orig_path = os.path.join(orig_path, corpus)
            if corpus in ['tlg', 'phi7']:
                if 'phi7' and latin is True:
                    latin = True
                    target_path = os.path.join(target_path, 'latin', 'text', corpus)
                else:
                    latin = None
                    target_path = os.path.join(target_path, 'greek', 'text', corpus)
            else:
                target_path = os.path.join(target_path, 'latin', 'text', corpus)
                latin = True
        try:
            corpus_files = os.listdir(orig_path)
        except Exception as exception:
            logger.error("Failed to find TLG files: %s", exception)
            raise
        # make a list of files to be converted
        txts = []
        [txts.append(x) for x in corpus_files if x.endswith('TXT')]  # pylint: disable=W0106
        # loop through list and convert one at a time
        for txt in txts:
            orig_txt_path = os.path.join(orig_path, txt)
            if markup is None:
                target_txt_dir = os.path.join(target_path, 'plaintext')
            else:
                target_txt_dir = os.path.join(target_path, str(markup))
            if not os.path.isdir(target_txt_dir):
                os.makedirs(target_txt_dir)
            target_txt_path = os.path.join(target_txt_dir, txt)
            try:
                self.convert(orig_txt_path, target_txt_path, markup=None,
                             break_lines=False, divide_works=False, latin=latin,
                             extra_args=None)
            except Exception as exception:
                logger.error("Failed to convert file '%s' to '%s': %s", orig_txt_path, target_txt_path, exception)

    def divide_works(self, corpus):
        """Use the work-breaking option.
        TODO: Maybe incorporate this into ``convert_corpus()``
        TODO: Write test for this
        """
        if corpus == 'tlg':
            orig_dir_rel = '~/cltk_data/originals/tlg'
            works_dir_rel = '~/cltk_data/greek/text/tlg/individual_works'
            file_prefix = 'TLG'
            latin = False
        elif corpus == 'phi5':
            orig_dir_rel = '~/cltk_data/originals/phi5'
            works_dir_rel = '~/cltk_data/latin/text/phi5/individual_works'
            file_prefix = 'LAT'
            latin = True  # this is for the optional TLGU argument to convert()

        orig_dir = os.path.expanduser(orig_dir_rel)
        works_dir = os.path.expanduser(works_dir_rel)
        if not os.path.exists(works_dir):
            os.makedirs(works_dir)

        files = os.listdir(orig_dir)
        texts = [x for x in files if x.endswith('.TXT') and x.startswith(file_prefix)]

        for file in texts:
            orig_file_path = os.path.join(orig_dir, file)
            new_file_path = os.path.join(works_dir, file)

            try:
                self.convert(orig_file_path, new_file_path, divide_works=True, latin=latin)
                logger.info('Writing files at %s to %s.', orig_file_path, works_dir)
            except Exception as err:
                logger.error('Failed to convert files: %s.', err)
