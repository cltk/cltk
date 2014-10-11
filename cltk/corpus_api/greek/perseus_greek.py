# encoding: utf-8
"""Perseus Greek texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import re
import bs4
from cltk.corpus import RemoteCorpus, TEIDoc
from cltk import soup_utils
from cltk.corpora.classical_greek.beta_to_unicode import Replacer


class PerseusGreek(RemoteCorpus):
    def __init__(self):
        self.name = 'perseus_greek'
        self.tar_url = ('https://raw.githubusercontent.com/kylepjohnson/'
                        'corpus_perseus_greek/master/perseus_greek.tar.gz')
        RemoteCorpus.__init__(self, self.name, self.tar_url)

    def retrieve(self):
        self.get_tar()


class PerseusGreekDoc(TEIDoc):

    def __init__(self, path):
        self.path = path
        TEIDoc.__init__(self, self.path)
        self.beta_replacer = Replacer()

    def main(self):
        # Get structure of entire XML tree
        content = self.soup.find('text')
        tree_structure = content.prettify()
        # Check for sub-texts
        texts = content.find_all('text')
        if texts == []:
            texts = content
        self.logger.info('Texts: ' + str(len(texts)))
        # Iterate over all (sub-)texts
        for text in texts:
            # If not BeautifulSoup tag, ignore
            if not text.name:
                continue

            # Get title of (sub-)text, prepare final MD text list
            md_text = [self.get_title(text)]

            # Find all text structure tags
            struct_tags = text.find_all('div1')
            self.logger.info('Structs: ' + str(len(struct_tags)))

            # Iterate over structure tags
            for s in struct_tags:
                # Determine where tag fits in tree's nested structure
                tag_level = self._tag_level(s, tree_structure)

                # Generate title for tag
                header = self._attrs_to_title(s, tag_level)
                if 'head' in soup_utils.tags(s):
                    head = s.head.text.replace('\n', ' ')
                    header = ' '.join([header, ':', head])

                # Check if tag + string or standalone tag
                if soup_utils.strings(s) == []:
                    if isinstance(s.next_sibling, bs4.element.NavigableString):
                        t = '\n'.join([header, s.next_sibling.replace('\t', '')])
                        md_text.append(t)
                    else:
                        #print(s.attrs)
                        #print(type(s.next_sibling))
                        pass
                else:
                    t = '\n'.join([header, s.text.replace('\t', '')])
                    md_text.append(t)

        #self.beta_replacer.beta_code()

        with open('/Users/smargh/Code/cltk/new.txt', 'w', encoding='utf-8') as f:
            data = '\n'.join(md_text)
            f.write(data)

    ## ------------------------------------------------------------------------

    def has_struct(self, tag):
        """BeautifulSoup ``find`` function.
        Checks if `tag` contains any attributes matching `structs` values.
        Since BeautifulSoup ``find`` functions can only have one argument,
        ``has_struct`` must access the `structs` var outside of its scope.
        """
        check = (ref for ref in self.struct_tags
                 for attr in list(tag.attrs.values())
                 if attr in ref)
        return next(check, False)

    def get_title(self, text_tag):
        # Get title from tag's `<head>` node
        if text_tag.find('head'):
            # Try to prepend head's parent node attribute data
            if text_tag.find('head').parent.attrs != {}:
                par_tag = text_tag.find('head').parent
                par_title = self._attrs_to_title(par_tag, 1)
                title_list = [par_title, '::']
            else:
                title_list = ['#']
            title_list.append(text_tag.find('head').text)
            text_title = ' '.join(title_list)
        else:
            # Get title from tag's attributes
            if text_tag.attrs != {}:
                text_title = self._attrs_to_title(text_tag, 1)
            # Get title from tag's first structure node
            else:
                tag = text_tag.find(self.has_struct)
                text_title = self._attrs_to_title(tag, 1)
        return text_title.replace('\t', '').replace('\n', ' ')

    def _attrs_to_title(self, tag, tag_level):
        tag_vals = sorted(list(tag.attrs.values()), reverse=True)
        header_level = '#' * tag_level
        tag_vals.insert(0, header_level)
        return ' '.join(tag_vals).upper()

    def _tag_level(self, tag, tree_structure):
        # Initialize default indent level (to become MD header level)
        indent_level = 2
        # Get contents of first XML tag
        first_tag = re.match('<[^>]+?>', str(tag)).group()
        # Create `re` search for tree node of tag
        first_tag_re = re.compile('^(\s*?)' + first_tag, re.M)
        # Search for tag in tree
        x = re.search(first_tag_re, tree_structure)
        # Extract indent level
        indent_level = len(x.group(1)) if x else indent_level
        return indent_level
