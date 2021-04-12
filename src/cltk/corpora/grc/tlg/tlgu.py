"""Wrapper for `tlgu` command line utility.

Original software at: ``http://tlgu.carmen.gr/``.

TLGU software written by Dimitri Marinakis and available at
`<http://tlgu.carmen.gr/>`_ under GPLv2 license.

TODO: the arguments to ``convert_corpus()`` need some rationalization, and
``divide_works()`` should be incorporated into it.

"""

__author__ = [
    "Kyle P. Johnson <kyle@kyle-p-johnson.com>",
    "Stephen Margheim <stephen.margheim@gmail.com>",
]
__license__ = "MIT License. See LICENSE."

import os
import subprocess

from cltk.core.cltk_logger import logger
from cltk.core.exceptions import CLTKException
from cltk.data.fetch import FetchCorpus
from cltk.utils.file_operations import make_cltk_path
from cltk.utils.utils import query_yes_no

# this currently not in use
ARGS = {
    "book_breaks": "-b",
    "page_breaks": "-p",
    "lat_text": "-r",
    "level_1": "-v",
    "level_2": "-w",
    "level_3": "-x",
    "level_4": "-y",
    "level_5": "-z",
    "line_tab": "-B",
    "higher_levels": "-X",
    "lower_levels": "-Y",
    "no_spaces": "-N",  # rm_newlines
    "citation_debug": "-C",
    "code_debug": "-S",
    "verbose": "-V",
    "split_works": "-W",
}


class TLGU:
    """Check, install, and call TLGU."""

    def __init__(self, interactive=True):
        """Check whether tlgu is installed, if not, import and install."""
        self.interactive = interactive
        self._check_and_download_tlgu_source()
        self._check_install()

    def _check_and_download_tlgu_source(self):
        """Check if tlgu downloaded, if not download it."""
        path = make_cltk_path("grc/software/grc_software_tlgu/tlgu.h")
        if not os.path.isfile(path):
            dl_msg = f"This part of the CLTK depends upon TLGU, software written by Dimitri Marinakis `<http://tlgu.carmen.gr/>`_."
            print(dl_msg)
            repo_url = "https://github.com/cltk/grc_software_tlgu.git"
            dl_dir = os.path.split(path)[0]
            dl_question = (
                f"Do you want to download TLGU from '{repo_url}' to '{dl_dir}'?"
            )
            if self.interactive:
                do_download = query_yes_no(question=dl_question)
            else:
                do_download = True
            if do_download:
                fetch_corpus = FetchCorpus(language="grc")
                fetch_corpus.import_corpus(corpus_name="grc_software_tlgu")
            else:
                raise CLTKException(f"TLGU software required for this class to work.")

    def _check_install(self):
        """Check if tlgu installed, if not install it."""
        try:
            subprocess.check_output(["which", "tlgu"])
        except subprocess.SubprocessError as sub_err:
            print("TLGU not installed.")
            logger.info("TLGU not installed: %s", sub_err)
            logger.info("Installing TLGU.")
            if not subprocess.check_output(["which", "gcc"]):
                logger.error("GCC seems not to be installed.")
            else:
                tlgu_path = make_cltk_path("grc/software/grc_software_tlgu")
                if self.interactive:
                    install_question = "Do you want to install TLGU?"
                    do_install = query_yes_no(question=install_question)
                    if not do_install:
                        raise CLTKException(
                            "TLGU installation required for this class to work."
                        )
                else:
                    print("Non-interactive installation. Continuing ...")
                command = "cd {0} && make install".format(tlgu_path)
                print(f"Going to run command: ``{command}``")
                try:
                    p_out = subprocess.call(command, shell=True)
                except subprocess.SubprocessError as sub_err:
                    print(
                        "Error executing installation. Going to check output of ``subprocess.call()`` ..."
                    )
                    raise CLTKException(sub_err)
                if p_out == 0:
                    msg = "TLGU installed."
                    print(msg)
                    logger.info(msg)
                    return True
                else:
                    msg = "TLGU install without sudo failed. Going to try again with sudo (usually required for Linux) ..."
                    print(msg)
                    logger.error(msg)
                command = "cd {0} && sudo make install".format(tlgu_path)
                if self.interactive:
                    install_question = "Do you want to install TLGU? with sudo?"
                    do_install = query_yes_no(question=install_question)
                    if not do_install:
                        raise CLTKException(
                            "TLGU installation required for this class to work."
                        )
                    p_out = subprocess.call(command, shell=True)
                else:
                    print("Going to run command:", command)
                    p_out = subprocess.call(command, shell=True)
                if p_out == 0:
                    msg = "TLGU installed."
                    print(msg)
                    logger.info(msg)
                else:
                    msg = "TLGU install with sudo failed."
                    print(msg)
                    logger.error(msg)
                    raise CLTKException(
                        "TLGU installation required for this class to work."
                    )

    @staticmethod
    def convert(
        input_path=None,
        output_path=None,
        markup=None,
        rm_newlines=False,
        divide_works=False,
        lat=False,
        extra_args=None,
    ):
        """
        Do conversion.

        :param input_path: TLG filepath to convert.
        :param output_path: filepath of new converted text.
        :param markup: Specificity of inline markup. Default None removes all numerical markup; 'full' gives most detailed, with reference numbers included before each text line.
        :param rm_newlines: No spaces; removes line ends and hyphens before an ID code; hyphens and spaces before page and column ends are retained.
        :param divide_works: Each work (book) is output as a separate file in the form output_file-xxx.txt; if an output file is not specified, this option has no effect.
        :param lat: Primarily Latin text (PHI). Some TLG texts, notably doccan1.txt and doccan2.txt are mostly roman texts lacking explicit language change codes. Setting this option will force a change to Latin text after each citation block is encountered.
        :param extra_args: Any other tlgu args to be passed, in list form and without dashes, e.g.: ['p', 'b', 'B'].

        """
        # setup file paths
        input_path = os.path.expanduser(input_path)
        output_path = os.path.expanduser(output_path)

        # check input path exists
        assert os.path.isfile(input_path), "File {0} does not exist.".format(input_path)

        # setup tlgu flags
        tlgu_options = []
        if markup == "full":
            full_args = ["v", "w", "x", "y", "z"]
            [tlgu_options.append(x) for x in full_args]  # pylint: disable=W0106
        if rm_newlines:
            tlgu_options.append("N")
        if divide_works:
            tlgu_options.append("W")
        if lat:
            tlgu_options.append("r")
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
            tlgu_flags = "-" + " -".join(tlgu_options)
        else:
            tlgu_flags = ""
        # make tlgu call
        tlgu_call = "tlgu {0} {1} {2}".format(tlgu_flags, input_path, output_path)
        logger.info(tlgu_call)
        try:
            p_out = subprocess.call(tlgu_call, shell=True)
            if p_out == 1:
                logger.error("Failed to convert %s to %s.", input_path, output_path)
        except Exception as exc:
            logger.error("Failed to convert %s to %s: %s", input_path, output_path, exc)
            raise

    def convert_corpus(self, corpus, markup=None, lat=None):  # pylint: disable=W0613
        """Look for imported TLG or PHI files and convert them all to
        ``~/cltk_data/grc/text/tlg/<plaintext>``.
        TODO: Add markup options to input.
        TODO: Add rm_newlines, divide_works, and extra_args
        """
        orig_path = make_cltk_path("originals")
        target_path = make_cltk_path()
        assert corpus in [
            "tlg",
            "phi5",
            "phi7",
        ], "Corpus must be 'tlg', 'phi5', or 'phi7'"
        if corpus in ["tlg", "phi5", "phi7"]:
            orig_path = os.path.join(orig_path, corpus)
            if corpus in ["tlg", "phi7"]:
                if "phi7" and lat is True:
                    lat = True
                    target_path = os.path.join(target_path, "lat", "text", corpus)
                else:
                    lat = None
                    target_path = os.path.join(target_path, "grc", "text", corpus)
            else:
                target_path = os.path.join(target_path, "lat", "text", corpus)
                lat = True
        try:
            corpus_files = os.listdir(orig_path)
        except Exception as exception:
            logger.error("Failed to find TLG files: %s", exception)
            raise
        # make a list of files to be converted
        txts = [x for x in corpus_files if x.endswith("TXT")]
        # loop through list and convert one at a time
        for txt in txts:
            orig_txt_path = os.path.join(orig_path, txt)
            if markup is None:
                target_txt_dir = os.path.join(target_path, "plaintext")
            else:
                target_txt_dir = os.path.join(target_path, str(markup))
            if not os.path.isdir(target_txt_dir):
                os.makedirs(target_txt_dir)
            target_txt_path = os.path.join(target_txt_dir, txt)
            try:
                self.convert(
                    orig_txt_path,
                    target_txt_path,
                    markup=False,
                    rm_newlines=False,
                    divide_works=False,
                    lat=lat,
                    extra_args=None,
                )
            except Exception as exception:
                logger.error(
                    "Failed to convert file '%s' to '%s': %s",
                    orig_txt_path,
                    target_txt_path,
                    exception,
                )

    def divide_works(self, corpus):
        """Use the work-breaking option.
        TODO: Maybe incorporate this into ``convert_corpus()``
        TODO: Write test for this

        """
        if corpus == "tlg":
            orig_dir = make_cltk_path("originals/tlg")
            works_dir = make_cltk_path("grc/text/tlg/individual_works")
            file_prefix = "TLG"
            lat = False
        elif corpus == "phi5":
            orig_dir = make_cltk_path("originals/phi5")
            works_dir = make_cltk_path("lat/text/phi5/individual_works")
            file_prefix = "LAT"
            lat = True  # this is for the optional TLGU argument to convert()
        elif corpus == "phi7":
            raise CLTKException("``phi7`` cannot be divided into individual works.")
        else:
            raise CLTKException(f"Invalid corpus '{corpus}'. This should never happen.")

        if not os.path.exists(works_dir):
            os.makedirs(works_dir)

        files = os.listdir(orig_dir)
        texts = [x for x in files if x.endswith(".TXT") and x.startswith(file_prefix)]

        for file in texts:
            orig_file_path = os.path.join(orig_dir, file)
            new_file_path = os.path.join(works_dir, file)

            try:
                self.convert(orig_file_path, new_file_path, divide_works=True, lat=lat)
                logger.info("Writing files at %s to %s.", orig_file_path, works_dir)
            except Exception as err:
                logger.error("Failed to convert files: %s.", err)


# assemble_tlg_author_filepaths
