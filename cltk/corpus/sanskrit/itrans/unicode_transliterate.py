__author__ = ["Nurendra Choudhary <nurendrachoudhary31@gmail.com>", "Anoop Kunchukuttan <anoop.kunchukuttan@gmail.com>"]
__license__ = "GPLv3"
# Indic NLP Library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Indic NLP Library is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
# 
#        You should have received a copy of the GNU General Public License
#        along with Indic NLP Library.  If not, see <http://www.gnu.org/licenses/>.
#

#Program for text written in one Indic script to another based on Unicode mappings. 
#

import sys, codecs, itertools, re

import cltk.corpus.sanskrit.itrans.langinfo as langinfo 
import cltk.corpus.sanskrit.itrans.itrans_transliterator as itrans_transliterator
from cltk.corpus.sanskrit.itrans.sinhala_transliterator import SinhalaDevanagariTransliterator  as sdt
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


def py23char(x):
    return chr(x)

class UnicodeIndicTransliterator(object):
    """
    Base class for rule-based transliteration among Indian languages. 

    Script pair specific transliterators should derive from this class and override the transliterate() method. 
    They can call the super class 'transliterate()' method to avail of the common transliteration
    """

    @staticmethod
    def _correct_tamil_mapping(offset): 
        # handle missing unaspirated and voiced plosives in Tamil script 
        # replace by unvoiced, unaspirated plosives

        # for first 4 consonant rows of varnamala
        # exception: ja has a mapping in Tamil  
        if offset>=0x15 and offset<=0x28 and \
                offset!=0x1c and \
                not ( (offset-0x15)%5==0 or (offset-0x15)%5==4 )  :
            subst_char=(offset-0x15)/5
            offset=0x15+5*subst_char

        # for 5th consonant row of varnamala                         
        if offset in [ 0x2b, 0x2c, 0x2d]:
            offset=0x2a

        # 'sh' becomes 'Sh'
        if offset==0x36:
            offset=0x37

        return offset             

    @staticmethod
    def transliterate(text,lang1_code,lang2_code):
        """
        convert the source language script (lang1) to target language script (lang2)

        text: text to transliterate
        lang1_code: language 1 code 
        lang1_code: language 2 code 
        """
        if (lang1_code in langinfo.SCRIPT_RANGES) and (lang2_code in langinfo.SCRIPT_RANGES):
            
            # if Sinhala is source, do a mapping to Devanagari first 
            if lang1_code=='si': 
                text=sdt.sinhala_to_devanagari(text)
                lang1_code='hi'

            # if Sinhala is target, make Devanagiri the intermediate target
            org_lang2_code=''
            if lang2_code=='si': 
                lang2_code='hi'
                org_lang2_code='si'

            trans_lit_text=[]
            for c in text: 
                newc=c
                offset=ord(c)-langinfo.SCRIPT_RANGES[lang1_code][0]
                if offset >=langinfo.COORDINATED_RANGE_START_INCLUSIVE and offset <= langinfo.COORDINATED_RANGE_END_INCLUSIVE:
                    if lang2_code=='ta': 
                        # tamil exceptions 
                        offset=UnicodeIndicTransliterator._correct_tamil_mapping(offset)
                    newc=py23char(langinfo.SCRIPT_RANGES[lang2_code][0]+offset)

                trans_lit_text.append(newc)        

            # if Sinhala is source, do a mapping to Devanagari first 
            if org_lang2_code=='si': 
                return sdt.devanagari_to_sinhala(''.join(trans_lit_text))

            return (''.join(trans_lit_text))
        else:
            return text

class ItransTransliterator(object):
    """
    Transliterator between Indian scripts and ITRANS
    """

    @staticmethod
    def to_itrans(text,lang_code):
        if lang_code in langinfo.SCRIPT_RANGES:
            if lang_code=='ml': 
                # Change from chillus characters to corresponding consonant+halant
                text=text.replace(u'\u0d7a',u'\u0d23\u0d4d')
                text=text.replace(u'\u0d7b',u'\u0d28\u0d4d')
                text=text.replace(u'\u0d7c',u'\u0d30\u0d4d')
                text=text.replace(u'\u0d7d',u'\u0d32\u0d4d')
                text=text.replace(u'\u0d7e',u'\u0d33\u0d4d')
                text=text.replace(u'\u0d7f',u'\u0d15\u0d4d')

            devnag=UnicodeIndicTransliterator.transliterate(text,lang_code,'hi')
            
            itrans=itrans_transliterator.transliterate(devnag.encode('utf-8'), 'devanagari','itrans',
                                 {'outputASCIIEncoded' : False, 'handleUnrecognised': itrans_transliterator.UNRECOGNISED_ECHO})
            return itrans.decode('utf-8') 
        else:
            return text

    @staticmethod
    def from_itrans(text,lang_code):
        if lang_code in langinfo.SCRIPT_RANGES: 
            devnag_text=itrans_transliterator.transliterate(text.encode('utf-8'), 'itrans', 'devanagari',
                                 {'outputASCIIEncoded' : False, 'handleUnrecognised': itrans_transliterator.UNRECOGNISED_ECHO})

            lang_text=UnicodeIndicTransliterator.transliterate(devnag_text.decode('utf-8'),'hi',lang_code)
            
            return lang_text
        else:
            return text

