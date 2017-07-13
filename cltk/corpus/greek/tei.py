"""Work with TEI XML files."""

import glob
import os


bs4_installed = True
try:
    from bs4 import BeautifulSoup
except ImportError:
    bs4_installed = False

from cltk.utils.cltk_logger import logger


def onekgreek_tei_xml_to_text():
    """Find TEI XML dir of TEI XML for the First 1k Years of Greek corpus."""
    if not bs4_installed:
        logger.error('Install `bs4` and `lxml` to parse these TEI files.')
        raise ImportError
    xml_dir = os.path.expanduser('~/cltk_data/greek/text/greek_text_first1kgreek/data/*/*/*.xml')
    xml_paths = glob.glob(xml_dir)
    if not len(xml_paths):
        logger.error('1K Greek corpus not installed. Use CorpusInstaller to get `First1KGreek`.')
        raise FileNotFoundError
    xml_paths = [path for path in xml_paths if '__cts__' not in path]

    # new dir
    new_dir = os.path.expanduser('~/cltk_data/greek/text/greek_text_first1kgreek_plaintext/')
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)

    for xml_path in xml_paths:
        _, xml_name = os.path.split(xml_path)
        xml_name = xml_name.rstrip('.xml')
        xml_name += '.txt'
        with open(xml_path) as file_open:
            soup = BeautifulSoup(file_open, 'lxml')
        body = soup.body
        text = body.get_text()
        new_plaintext_path = os.path.join(new_dir, xml_name)
        with open(new_plaintext_path, 'w') as file_open:
            file_open.write(text)


if __name__ == '__main__':
    text = onekgreek_tei_xml_to_text()
    print(text)
