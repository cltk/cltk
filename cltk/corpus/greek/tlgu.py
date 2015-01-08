"""Wrapper for `tlgu` command line utility

TODO: Fully implement this.
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.utils.cltk_logger import logger
from cltk.corpus.utils.importer import CorpusImporter
import os
import subprocess
import sys

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
    def __init__(self):
        """Check whether tlgu is installed, if not, import and install."""
        self._check_import_source()
        self._check_install()

    @staticmethod
    def _check_import_source():
        """Check if tlgu imported, if not import it."""
        path_rel = '~/cltk_data/greek/software/tlgu/tlgu.h'
        path = os.path.expanduser(path_rel)
        if not os.path.isfile(path):
            try:
                corpus_importer = CorpusImporter('greek')
                corpus_importer.import_corpus('tlgu')
            except Exception as exc:
                logger.error('Failed to import TLGU: %s' % exc)
                sys.exit(1)

    @staticmethod
    def _check_install():
        """Check if tlgu installed, if not install it."""
        try:
            subprocess.check_output(['which', 'tlgu'])
        except Exception as exc:
            logger.info('TLGU not installed: %s' % exc)
            logger.info('Installing TLGU.')
            if not subprocess.check_output(['which', 'gcc']):
                logger.error('GCC seems not to be installed.')
            else:
                tlgu_path_rel = '~/cltk_data/greek/software/tlgu'
                tlgu_path = os.path.expanduser(tlgu_path_rel)
                try:
                    p_out = subprocess.call('cd %s && make install' %
                                            tlgu_path, shell=True)
                    if p_out == 0:
                        logger.info('TLGU installed.')
                    else:
                        logger.error('TLGU install without sudo failed.')
                except Exception as exc:
                    logger.error('TLGU install failed: %s' % exc)
                else:  # for Linux needing root access to '/usr/local/bin'
                    p_out = subprocess.call('cd %s && sudo make install' %
                                            tlgu_path, shell=True)
                    if p_out == 0:
                        logger.info('TLGU installed.')
                    else:
                        logger.error('TLGU install with sudo failed.')
                        sys.exit(1)

    #@staticmethod
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
        # setup tlgu flags
        tlgu_options = []
        if markup == 'full':
            full_args = ['v', 'w', 'x', 'y', 'z']
            [tlgu_options.append(x) for x in full_args]
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
                logger.error("Argument 'extra_args' must be a list: %s" % exc)
                sys.exit(1)
        tlgu_options = tlgu_options + extra_args
        # assemble all tlgu flags
        tlgu_options = list(set(tlgu_options))
        if tlgu_options:
            tlgu_flags = '-' + ' -'.join(tlgu_options)
        else:
            tlgu_flags = ''
        # make tlgu call
        tlgu_call = 'tlgu %s %s %s' % (tlgu_flags, input_path, output_path)
        logger.info(tlgu_call)
        try:
            p_out = subprocess.call(tlgu_call, shell=True)
            if p_out == 1:
                logger.error('Failed to convert %s to %s.' % (input_path, output_path))
                sys.exit(1)
        except Exception as exc:
            logger.error('Failed to convert %s to %s: %s' % (input_path, output_path, exc))
            sys.exit(1)

    #@staticmethod
    def convert_corpus(self, corpus, markup=None, break_lines=False, divide_works=False, latin=None, extra_args=None):
        """Look for imported TLG or PHI files and convert them all to
        ``~/cltk_data/greek/text/tlg/<plaintext>``.
        TODO: Should this and/or convert() be static?
        TODO: Add markup options to input.
        """
        orig_path_rel = '~/cltk_data/originals'
        orig_path = os.path.expanduser(orig_path_rel)
        target_path_rel = '~/cltk_data'
        target_path = os.path.expanduser(target_path_rel)
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
        else:
            logger.error("Corpus variable must be: 'tlg', 'phi5', or 'phi7'.")
            sys.exit(0)
        try:
            corpus_files = os.listdir(orig_path)
        except Exception as exception:
            logger.error("Failed to find an TLG files: %s" % exception)
            sys.exit(1)
        # make a list of files to be converted
        txts = []
        [txts.append(x) for x in corpus_files if x.endswith('TXT')]
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
                logger.error("Failed to convert file '%s' to '%s': %s" % (orig_txt_path, target_txt_path, exception))
