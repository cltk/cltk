"""
This module is for printing texts in Markdown or HTML.
"""

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class PrettyPrint(object):
    """
    Prints texts in markdown or in HTML.
    """
    def __init__(self):
        """
        Empty.
        """

    def markdown_single_text(self, ingest_text, cdli_number):
        """
        Prints single text in file in markdown.
       :param ingest_text: text ingested by cdli_corpus
       :param cdli_number: text you wish to print
       :return: output in filename.md
       """
        for text in ingest_text:
            cdli = text['cdli number'][0]
            if cdli_number in cdli:
                edition = text['text edition'][0]
                metadata = '\n \t'.join(text['metadata'][0]).rstrip()
                transliteration = '\n \t'.join(text['transliteration'][0]).rstrip()
                m_d = """{edition}
---
### metadata
    {metadata}
### transliteration
    {transliteration}  
""".format(edition=edition, metadata=metadata, transliteration=transliteration)
                self.markdown_text = m_d

    def html_print_file(self, ingested_file, destination):
        """
        Prints text_file in html.
        :param ingested_file: text file you wish to pretty print
        :param destination: where you wish to save the HTML data
        :return: output in html_file.html.
        """
        with open(destination, mode='r+', encoding='utf8') as t_f:
            for text in ingested_file:
                edition = text['text edition'][0]
                metadata = '<br> \n'.join(text['metadata'][0])
                transliteration = '<br> \n'.join(text['transliteration'][0])
                self.html_file = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{edition}</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>{edition}</h2>
</th><th>
<h3>metadata</h3>
</th><th>
<h3>transliteration</h3>
</th></tr><tr><td></td><td>
<font size='2'>
    {metadata}     
</font></td><td>
<p>{trans}
</td></tr></table>
<br>
</body>
</html>""".format(edition=edition, metadata=metadata, trans=transliteration)
                t_f.write(self.html_file)

    def html_print_single_text(self, ingested_file, cdli_number, destination):
        """
        Prints text_file in html.
        :param ingested_file: CDLICorpus().texts after ingestion
        :param cdli_number: which text you want printed
        :param destination: where you wish to save the HTML data
        :return: output in html_file.html.
        """
        for text in ingested_file:
            cdli = text['cdli number'][0]
            if cdli_number in cdli:
                edition = text['text edition'][0]
                metadata = '<br> \n'.join(text['metadata'][0]).rstrip()
                transliteration = '<br> \n'.join(text
                                               ['transliteration'][0]).rstrip()
                with open(destination, mode='r+', encoding='utf8') as t_f:
                    self.html_single = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{edition}</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>{edition}</h2>
</th><th>
<h3>metadata</h3>
</th><th>
<h3>transliteration</h3>
</th></tr><tr><td></td><td>
<font size='2'>
    {metadata}     
</font></td><td>
<p>{trans}
</td></tr></table>
<br>
</body>
</html>""".format(edition=edition, metadata=metadata, trans=transliteration)
                    t_f.write(self.html_single)
