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

    def markdown_single_text(self, catalog, cdli_number):
        """
        Prints single text in file in markdown.
       :param catalog: text ingested by cdli_corpus
       :param cdli_number: text you wish to print
       :return: output in filename.md
       """
        if cdli_number in catalog:
            pnum = catalog[cdli_number]['pnum']
            edition = catalog[cdli_number]['edition']
            metadata = '\n\t'.join(catalog[cdli_number]['metadata'])
            transliteration = '\n\t'.join(catalog[cdli_number]['transliteration'])
            normalization = '\n\t'.join(catalog[cdli_number]['normalization'])
            translation = '\n\t'.join(catalog[cdli_number]['translation'])
            m_d = """{edition}
{pnum}
---
### metadata
    {metadata}
### transliteration
    {trans}
### normalization
    {norm}
### translation
    {translation}  
""".format(pnum=pnum, edition=edition, metadata=metadata,
           trans=transliteration, norm=normalization,
           translation=translation)
            self.markdown_text = m_d  # pylint: disable=attribute-defined-outside-init

    def html_print_file(self, catalog, destination):
        """
        Prints text_file in html.
        :param catalog: text file you wish to pretty print
        :param destination: where you wish to save the HTML data
        :return: output in html_file.html.
        """
        with open(destination, mode='r+', encoding='utf8') as t_f:
            for text in catalog:
                pnum = catalog[text]['pnum']
                edition = catalog[text]['edition']
                metadata = '<br>\n'.join(catalog[text]['metadata'])
                transliteration = '<br>\n'.join(catalog[text]['transliteration'])
                normalization = '<br>\n'.join(catalog[text]['normalization'])
                translation = '<br>\n'.join(catalog[text]['translation'])
                self.html_file = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{edition}</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>{edition}<br>{pnum}</h2>
</th><th>
<h3>transliteration</h3>
</th><th>
<h3>normalization</h3>
</th><th>
<h3>translation</h3>
</tr><tr><td>
{metadata}</td><td>
<p>{trans}
</td><td>
<p>{norm}
</td><td>
<font size='2'>
{translation}
</font></td></tr>

</table>
<br>
</body>
</html>""".format(
    pnum=pnum, edition=edition, metadata=metadata,
    trans=transliteration, norm=normalization,
    translation=translation)
                t_f.write(self.html_file)

    def html_print_single_text(self, catalog, cdli_number, destination):
        """
        Prints text_file in html.
        :param catalog: CDLICorpus().catalog
        :param cdli_number: which text you want printed
        :param destination: where you wish to save the HTML data
        :return: output in html_file.html.
        """
        if cdli_number in catalog:
            pnum = catalog[cdli_number]['pnum']
            edition = catalog[cdli_number]['edition']
            metadata = '<br>\n'.join(catalog[cdli_number]['metadata'])
            transliteration = '<br>\n'.join(catalog[cdli_number]['transliteration'])
            normalization = '<br>\n'.join(catalog[cdli_number]['normalization'])
            translation = '<br>\n'.join(catalog[cdli_number]['translation'])
            self.html_single = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{edition}</title>
</head>
<body><table cellpadding="10"; border="1">
<tr><th>
<h2>{edition}<br>{pnum}</h2>
</th><th>
<h3>transliteration</h3>
</th><th>
<h3>normalization</h3>
</th><th>
<h3>translation</h3>
</tr><tr><td>
{metadata}</td><td>
<p>{trans}
</td><td>
<p>{norm}
</td><td>
<font size='2'>
{translation}
</font></td></tr>

</table>
<br>
</body>
</html>""".format(
    pnum=pnum, edition=edition, metadata=metadata,
    trans=transliteration, norm=normalization,
    translation=translation)
            with open(destination, mode='r+', encoding='utf8') as t_f:
                t_f.write(self.html_single)
