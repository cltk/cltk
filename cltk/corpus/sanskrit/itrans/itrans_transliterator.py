__author__ = ["Nurendra Choudhary <nurendrachoudhary31@gmail.com>", "Anoop Kunchukuttan <anoop.kunchukuttan@gmail.com>"]
__license__ = "GPLv3"
""" Transliterate texts between unicode and standard transliteration schemes.

Transliterate texts between non-latin scripts and commonly-used latin
transliteration schemes. Uses standard Unicode character blocks -- 
e.g. DEVANAGARI U+0900 ... U+097F -- and transliteration schemes -- 
e.g. the IAST convention for transliteration of Sanskrit to latin-with-dots.

The following character blocks and transliteration schemes are included:

DEVANAGARI
    IAST
    ITRANS -- http://www.aczoom.com/itrans/#itransencoding (Sanskrit only)
    Harvard Kyoto
    
CYRILLIC
    ISO 9:1995 (Russian only)
    
New character blocks and transliteration schemes can be added by creating
new CharacterBlock and TransliterationScheme objects.

USAGE
--------
Transliterate a text:

>>> import transliterator
>>> transliterator.transliterate('yogazcittavRttinirodhaH', 'harvardkyoto',
...     'devanagari', {'outputASCIIEncoded' : True})
'&#x92f;&#x94b;&#x917;&#x936;&#x94d;&#x91a;&#x93f;&#x924;&#x94d;&#x924;&#x935;&#x943;&#x924;&#x94d;&#x924;&#x93f;&#x928;&#x93f;&#x930;&#x94b;&#x927;&#x903;'

Create a new CharacterBlock and TransliterationScheme:

>>> import transliterator
>>> cb = transliterator.CharacterBlock('NEWBLOCK', range(0x901, 0x9FF))
>>> scheme = transliterator.TransliterationScheme(cb.name, 'NEWSCHEME',
...                          {'ab': 0x901, 'cd': 0x902})
>>> transliterator.transliterate('abcd', scheme, cb, {'outputASCIIEncoded' : True})
'&#x901;&#x902;'

COPYRIGHT AND DISCLAIMER
------------------------------------
Transliterator is:

version 0.1 software  - use at your own risk.

The IAST, ITRANS and Harvard-Kyoto transliteration schemes have been
tested for classical Sanskrit, not for any other language.

The Cyrillic alphabet and ISO 9:1995 transliteration (for Russian only)
are included but have been even more lightly tested than Devanagari.

Copyright (c) 2005 by Alan Little

By obtaining, using, and/or copying this software and/or its
associated documentation, you agree that you have read, understood,
and will comply with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and
its associated documentation for any purpose and without fee is
hereby granted, provided that the above copyright notice appears in
all copies, and that both that copyright notice and this permission
notice appear in supporting documentation, and that the name of 
the author not be used in advertising or publicity pertaining to 
distribution of the software without specific, written prior permission.

THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.  
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR 
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION 
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
       
"""
""" TO DO

cyrillic: GOST & something ASCII-only & sensible
punctuation &/ numerals:
    HK
    check Itrans punctuation
 implicit conversion to unicode if no to format specified
 URLs for the input text
 
Bugs
is there a problem with implicit A before visarga?


"""
__version__ = '2.0'

import unicodedata
#from sets import Set
import sys

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


characterBlocks = {}
_names = {}

# handle unrecognised characters

UNRECOGNISED_FAIL = 0
UNRECOGNISED_ECHO = 1
UNRECOGNISED_SUBSTITUTE = 2

# default options

options = {}
def resetOptions():
    """ Reset options to their default values. """
    global options
    defaultOptions = {
        'inputEncoding' : 'utf-8',  # default input encoding for strings
        'outputEncoding' : 'utf-8', # default output encoding
        'substituteChar' : '?', # use to substitute unrecognised characters
        'handleUnrecognised' : UNRECOGNISED_FAIL,   # unrecognised characters:
                                                    # fail, echo or substitute
        'outputASCIIEncoded' : False,   # HTML-encoded ASCII output?                                                
    }
    options = defaultOptions.copy()
resetOptions()


def _unrecognised(achr):
    """ Handle unrecognised characters. """
    if options['handleUnrecognised'] == UNRECOGNISED_ECHO:
        return achr
    elif options['handleUnrecognised'] == UNRECOGNISED_SUBSTITUTE:
        return options['substituteChar']
    else:
        raise KeyError(achr)

def py23char(x):
    return chr(x)
 
class TLCharacter (object):
    """ Class representing a Unicode character with its equivalents.
    
    Public attributes:
    unicodeHexValue -- the numeric value of the Unicode code point.
    unichr -- the character value of the Unicode code point.
    name -- the name of the Unicode code point.
    equivalents -- a dict containing the character's equivalents in 
                   various transliteration schemes, in the format:
                   {'Scheme A': 'A', 'Scheme B': 'aah', }
                   where keys are TransliterationScheme names,
                   values are transliterated equivalents of the 
                   character.
    
    """

    def __init__(self, unicodeHexValue, block):
        """ Set up a unicode character.
        
        Arguments:
        unicodeHexValue -- an integer that should correspond to a 
                           Unicode code point.
        block -- the CharacterBlock this character belongs to.
        
        Raises:
        ValueError -- if unicodeHexValue is not a valid code point.
        
        """
        if unicodeHexValue < 0 or unicodeHexValue > 0x10FFFF:
            raise ValueError("numeric value outside Unicode range")
        self.unicodeHexValue = unicodeHexValue
        """ Use name check to filter out unused characters.
              unicodedata.name() raises ValueError for these
        """
        self.unichr = py23char(self.unicodeHexValue)
        self.name = unicodedata.name(self.unichr)
        self.equivalents = {}
        self._block = block
        
    def addEquivalent(self, equivName, equivalent):
        """ Add an equivalent for the character.
        
        Arguments:
        equivName -- the name of a TransliterationScheme
        equivalent -- string/unicode equivalent in the named
                      TransliterationScheme for this code point.
        """
        self.equivalents[equivName] = equivalent
     
class CharacterBlock(dict):
    """ Dictionary-like representation of a set of unicode characters.
    
    For our purposes, a character block corresponds to an alphabet/script
    that we want to be able to transliterate to or from, e.g. Cyrillic,
    Devanagari.
    
    Keys are unicode characters.
    Values are TLCharacter instances.

    """
    
    def __init__(self, name, charRange, charClass=TLCharacter):
        """ Set up a character block corresponding to a range of code points.
       
        Keyword arguments:
        name -- a string containing the name of the character block.
                (should normally use a standard Unicode character block name)
        range -- a list of code points. Reserved code points are ignored.
        charClass -- the class to be used to create the characters.
                     Should be a subclass of TLCharacter.
        
        """
        
        """ Ensure that any character sequence dependencies will be ok.
        
        e.g. set up Devanagari standalone vowels before dependents.
        
        """
        charRange.sort()
        
        for c in charRange:
            try:
                tlchar = charClass(c, self)
                self[tlchar.unichr] = tlchar
            except ValueError: # Unicode reserved code points.
                # not an error
                pass
        self._longestEntry = 1
        self.name = name
        self.transliterationSchemes = {}
        self._register()

    def _register(self):
        characterBlocks[self.name] = self
        _names[self.name.upper()] = self
        
    def _transliterate (self, text, outFormat):
        """ Transliterate the text to the target transliteration scheme."""
        result = []
        for c in text:
            if c.isspace(): result.append(c)
            try: 
                result.append(self[c].equivalents[outFormat.name])
            except KeyError:
                result.append(_unrecognised(c))
        return result
        
    def _preprocess(self, text):
        """ Make our signature compatible with TransliterationScheme. """
        return text

    def _getNextChar(self, text, startPos):
        return text[startPos]

    
class TransliterationScheme(dict):
    """ Dictionary-like representation of a transliteration scheme.
    
    e.g. the Harvard-Kyoto, IAST or ITRANS schemes for
    transliterating Devanagari to or from the latin alphabet.
    
    Keys are unicode strings representing the letter-equivalents used
    in the transliteration scheme.
    Values are TLCharacter instances.
    
    """

    def __init__(self, blockName, schemeName, data, swapTable=None):
        """ Set up a transliteration scheme.
        
        Keyword arguments:
        blockName -- a string containg the name of the character block this 
                     transliteration scheme is used for, 
                     e.g. 'CYRILLIC', 'DEVANAGARI'.
        schemeName -- the name of the transliteration scheme. 
                      Must be unique.
        data -- a dict containing the data for the transliteration scheme. 
                Keys are transliterated Unicode characters or strings.
                Values are integers corresponding to Unicode code points.
                For examples, see the data for the built-in transliteration
                schemes.
        swapTable -- a dict (default None) containing any non-standard
                     letter combinations used in the transliteration scheme
                     that we want to pre-process away before transliterating.
                     See the ITRANS data for examples.
        
        Raises:
        KeyError: unknown block name.
        TypeError: swapTable is not a dict
                
        """
        self.block = characterBlocks[blockName]
        self.name = schemeName
        for equiv, unicodeHexValue in data.items():
            self[equiv] = self.block[py23char(unicodeHexValue)]
            self[equiv].addEquivalent(self.name, equiv)
        self._longestEntry = max([len(e) for e in list(data.keys())])
        if self._longestEntry > 1:
            self._parseTree = {}
            self._parsedata = list(data.keys())
            self._parsedata.sort()
            self._setupParseTree(0, len(data) - 1, 0, self._parseTree)
        if swapTable is not None:
            if not isinstance(swapTable, dict): raise TypeError
        self.swapTable = swapTable
        self._register()

    def _register(self):
        self.block.transliterationSchemes[self.name] = self
        _names[self.name.upper()] = self
    
    def _setupParseTree(self, rowFrom, rowTo, colIndex, tree):
        """ Build the search tree for multi-character encodings.
        """
        if colIndex == self._longestEntry:
            return
        prevchar = None
        rowIndex = rowFrom
        while rowIndex <= rowTo:
            if colIndex < len(self._parsedata[rowIndex]):
                c = self._parsedata[rowIndex][colIndex]
                if c != prevchar:
                    tree[c] = {}
                    if  prevchar is not None:
                        self._setupParseTree(rowFrom, rowIndex - 1, colIndex + 1, tree[prevchar])
                    rowFrom = rowIndex
                    prevchar = c
                if rowIndex == rowTo:
                    self._setupParseTree(rowFrom, rowIndex, colIndex + 1, tree[prevchar])
            rowIndex = rowIndex + 1
                
    def __getNextChar(self, text, startPos, tree):
        i = startPos
        matched = text[i]
        if i < len(text) - 1:
            try:
                if text[i + 1] in tree[text[i]]:
                    matched = matched + self.__getNextChar(text, i + 1, tree[text[i]])
            except KeyError:
                # Ignore. The lookup for the equivalent character later on will handle it.
                pass
        return matched
    
    def _getNextChar(self, text, startPos):
        if self._longestEntry > 1 and not text[startPos].isspace():
            return self.__getNextChar(text, startPos, self._parseTree)
        else:
            return text[startPos]
            
    def _preprocess(self, text):
        if self.swapTable:
            for c in self.swapTable:
                if isinstance(text,bytes):
                	text = text.decode()
                text = text.replace(c, self.swapTable[c])
        return text
        
            
    def _transliterate (self, text, outFormat):
        """ Transliterate the text to Unicode."""
        result = []
        text = self._preprocess(text)
        i = 0
        while i < len(text):
            if text[i].isspace(): 
                result.append(text[i])
                i = i+1
            else: 
                chr = self._getNextChar(text, i)
                try:
                    result.append(self[chr].unichr)
                except KeyError:
                    result.append(_unrecognised(chr))
                i = i + len(chr)
        return result

    
def transliterate(text, inFormat, outFormat, requestOptions={}):
    """ Transliterate a text.
    
    Keyword arguments:
    text -- a unicode string containing the text to be transliterated
    inFormat -- the "from" CharacterBlock or TransliterationScheme, or its name
    outFormat -- the target CharacterBlock or TransliterationScheme, or its name
    requestOptions -- optional dict containing option settings that override the
                      defaults for this request.
    
    Returns a unicode object containing the text transliterated into the
    target character set.
    
    Raises:
    ValueError -- unrecognised input or output format.
    KeyError -- a character in text is not a member of inFormat, or has no
    corresponding character defined in outFormat.
    
    """
    def asciiEncode(chr):
        value = ord(chr)
        if value > 255:
            return '&#x%x;' % (value)
        return chr
      
    try:
        options.update(requestOptions)
    
        """ Ensure we have the correct encoding for input text. """
        if isinstance(text, str):
            try:
                text = text.decode(options['inputEncoding'])
            except:
            	pass

        """ Look up input & output format names. """
        def findFormat(fmt):
            if isinstance(fmt, basestring):
                try:
                    fmt = _names[fmt.upper()]
                except KeyError:
                    raise ValueError('unrecognised format ' + fmt)
            return fmt
        inFormat = findFormat(inFormat)
        outFormat = findFormat(outFormat)
        
        """ Perform sanity checks. """
    
        if not isinstance(text, basestring): 
                raise TypeError("The text must be a string or a unicode object")
        
        def getBlock(format):
            if isinstance(format, CharacterBlock):
                return format
            else:
                return format.block
        inBlock = getBlock(inFormat)
        outBlock = getBlock(outFormat)
        if not inBlock is outBlock:
            raise ValueError("incompatible input and output formats")
            
        if inFormat is outFormat:
            # They're trying to trick us. Just do a quick sanity check & bounce it back.
            if inFormat._longestEntry == 1:
                [inFormat[c] for c in set(text) if not c.isspace()] 
                # -> KeyError for extraneous chars.
                return text
            
        """ At last we're happy. Do it. """
            
        result = inFormat._transliterate(text, outFormat)
        if options['outputASCIIEncoded']:
            result = [asciiEncode(c) for c in result]
        return u''.join(result).encode(options['outputEncoding'])
    finally:
        resetOptions()
    
            
""" DEVANAGARI PROCESSING

    Specialised classes & functions to handle Devanagari.
    
"""


class DevanagariCharacter (TLCharacter):
    """ Special processing for Devanagari characters. 
    """
    
    """
        Devanaagarii characters need to know if they are vowels or not.
        Unicode Data doesn't help with this - category 'Mn' is not unique to dependent vowels
        - so need to hard code the ranges
    """
    _vowelOffset = 0x93E - 0x906
    _depVowelRange = list(range(0x93E, 0x94D)) + [0x962,0x963]
    _vowelRange = list(range(0x904, 0x915)) + [0x960,0x961]
    _VIRAMA = py23char(0x94D)
    _LETTER_A = py23char(0x905)
    """ Unicode calls agravaha a letter. Not for our purposes:
        we need to not treat it as one for handling virama & implicit 'a'
    """
    _AGRAVAHA = 0x93D
    _OM = 0x950
    
    def __init__(self, unicodeHexValue, block):
        """ Create an object representing a Devanagari character.
        
        Extends TLCharacter.__init__ to distinguish Devanagari standalone
        vowels, dependent vowels and consonants.
        
        Raises 
        ValueError -- for characters in the Devanagari dependent vowel range.
                      We want these as variants of the corresponding standalone 
                      vowels, not as separate characters.
        
        """
        TLCharacter.__init__(self, unicodeHexValue, block)

        self.isVowel = False
        if unicodeHexValue in DevanagariCharacter._vowelRange:
            self.isVowel = True

        self._dependentVowel = None
        if unicodeHexValue==0x960: 
            ## dependency vowel sign for vocalic RR is set only when processing the vowel, since the maatra precedes the vowel in the Unicode chart
            self._setDependentVowel(0x944)

        if unicodeHexValue in DevanagariCharacter._depVowelRange:
            vowel=None
            if  unicodeHexValue == 0x962: 
                vowel=block[py23char(0x90C)]
            elif  unicodeHexValue == 0x963: 
                vowel=block[py23char(0x961)]
            elif unicodeHexValue == 0x944:
                ## dependency vowel sign for vocalic RR is set only when processing the vowel, since the maatra precedes the vowel in the Unicode chart
                ## That step's cpde is above, with documentation 
                pass 
            else:                 
                vowel=block[py23char(unicodeHexValue - DevanagariCharacter._vowelOffset)]
            if vowel is not None:                 
                # The check condition is for 0x944, processing deferred for later
                vowel._setDependentVowel(unicodeHexValue)
            raise ValueError # don't create dependent vowels as separate instances
            
        #TLCharacter.__init__(self, unicodeHexValue, block)

        self.isConsonant = False
        if self.isVowel == False \
        and self.unichr.isalpha() \
        and self.unicodeHexValue not in (DevanagariCharacter._AGRAVAHA,
                                                           DevanagariCharacter._OM):
            self.isConsonant = True

    def _setDependentVowel(self, unicodeHexValue):
        if unicodeHexValue is not None:
            if not self.isVowel: raise ValueError
            self._dependentVowel = py23char(unicodeHexValue)
            self._block[py23char(unicodeHexValue)] = self
            
class _Devanagari(object):
    """ Holder class for the Devanagari transliteration algorithm. """
    
    def _transliterate(self, text, outFormat):
        """ Transliterate a devanagari text into the target format.
        
        Transliterating a character to or from Devanagari is not a simple 
        lookup: it depends on the preceding and following characters.
        """
        def getResult(): 
            if curMatch.isspace():
                result.append(curMatch)
                return
            if prevMatch in self:
                prev = self[prevMatch]
            else:
                prev = None
            if nextMatch in self:
                next = self[nextMatch]
            else:
                next = None
            try:
                equiv = outFormat._equivalent(self[curMatch], 
                                                            prev, #self.get(prevMatch, None), 
                                                            next, #self.get(nextMatch, None),
                                                            self._implicitA)
            except KeyError:
                equiv = _unrecognised(curMatch)
            for e in equiv:
                result.append(e)
                
        def incr(c):
            if self._longestEntry == 1:
                return 1
            return len(c)
            
            
        result = []
        try:
            text = text.decode()
        except:
        	pass
        text = self._preprocess(text)
        i = 0
        prevMatch = None
        nextMatch = None
        curMatch = self._getNextChar(text, i)
        i = i + len(curMatch)
        while i < len(text):
            nextMatch = self._getNextChar(text, i)
            getResult()
            i = i + len(nextMatch)
            prevMatch = curMatch
            curMatch = nextMatch
            nextMatch = None
        getResult() 
        return result


class DevanagariCharacterBlock(CharacterBlock, _Devanagari):
    """ Class representing the Devanagari Unicode character block.
    
    """
    
    def __init__(self, name, charRange):
        """ Set up the Devanagari character block.
        
        Extends CharacterBlock.__init__ by specifiying that the characters
        created should be instances of DevanagariCharacter.
        
        """
        CharacterBlock.__init__(self, name, charRange, DevanagariCharacter)
        self._implicitA = True # generate implicit As when transliterating 
                                # *FROM* this scheme
        
    def _transliterate(self, text, outFormat):
        """ Need to specify which superclass _transliterate() to call. """
        return _Devanagari._transliterate(self, text, outFormat)
    
    def _equivalent(self, char, prev, next, implicitA):
        """ Transliterate a Latin character equivalent to Devanagari.
        
        Add VIRAMA for ligatures.
        Convert standalone to dependent vowels.
        
        """
        result = []
        if char.isVowel == False:
            result.append(char.unichr)
            if char.isConsonant \
            and ((next is not None and next.isConsonant) \
            or next is None): 
                result.append(DevanagariCharacter._VIRAMA)
        else:
            if prev is None or prev.isConsonant == False:
                result.append(char.unichr)
            else:
                if char._dependentVowel is not None:
                    result.append(char._dependentVowel)
        return result

        
class DevanagariTransliterationScheme(TransliterationScheme, _Devanagari):
    """ Class representing a Devanagari transliteration scheme. """

    def __init__(self, blockName, schemeName, data, swapTable=None):
        """ Set up a Devanagari transliteration scheme.
        
        Extends TransliterationScheme.__init__
        
        """
        TransliterationScheme.__init__\
                (self, blockName, schemeName, data, swapTable)
        self._implicitA = False # generate implicit As when transliterating 
                                # *FROM* this scheme

    def _transliterate(self, text, outFormat):
        """ Need to specify which superclass _transliterate() to call. """
        return _Devanagari._transliterate(self, text, outFormat)

    def _equivalent(self, char, prev, next, implicitA):
        """ Transliterate a Devanagari character to Latin.
        
        Add implicit As unless overridden by VIRAMA.
        
        """
        result = []
        if char.unichr != DevanagariCharacter._VIRAMA:
            result.append(char.equivalents[self.name])
        """ Append implicit A to consonants if the next character isn't a vowel. """
        if implicitA and char.isConsonant \
        and ((next is not None \
        and next.unichr != DevanagariCharacter._VIRAMA \
        and not next.isVowel) \
        or next is None):
            result.append(characterBlocks['DEVANAGARI']\
                   [DevanagariCharacter._LETTER_A].equivalents[self.name])
        return result
  

""" DEVANAGARI DATA

set up the Devanagari character set with three commonly used transliteration 
schemes:
ITRANS
Harvard Kyoto
IAST

"""

DevanagariCharacterBlock('DEVANAGARI', list(range(0x900, 0x97F)))

HARVARDKYOTO = { \
    'M': 0x902,
    'H': 0x903,
    'a': 0x905,
    'A': 0x906,
    'i': 0x907,
    'I': 0x908,
    'u': 0x909,
    'U': 0x90A,
    'R': 0x90B,
    'lR': 0x90C,
    'e': 0x90F,
    'ai': 0x910,
    'o': 0x913,
    'au': 0x914,
    'k': 0x915,
    'kh': 0x916,
    'g': 0x917,
    'gh': 0x918,
    'G': 0x919,
    'c': 0x91A,
    'ch': 0x91B,
    'j': 0x91C,
    'jh': 0x91D,
    'J': 0x91E,
    'T': 0x91F,
    'Th': 0x920,
    'D': 0x921,
    'Dh': 0x922,
    'N': 0x923,
    't': 0x924,
    'th': 0x925,
    'd': 0x926,
    'dh': 0x927,
    'n': 0x928,
    'p': 0x92A,
    'ph': 0x92B,
    'b': 0x92C,
    'bh': 0x92D,
    'm': 0x92E,
    'y': 0x92F,
    'r': 0x930,
    'l': 0x932,
    'v': 0x935,
    'z': 0x936,
    'S': 0x937,
    's': 0x938,
    'h': 0x939,
    "'": 0x93D,
    'oM': 0x950,
     }
DevanagariTransliterationScheme('DEVANAGARI','HARVARDKYOTO', HARVARDKYOTO)
     
ITRANS = { \
    'R': 0x931,  # added by anoop # extension 
    'M': 0x902,
    '.n': 0x902,
    '.m': 0x902,
    'H': 0x903,
    'a': 0x905,
    'A': 0x906,
    'aa': 0x906,
    'i': 0x907,
    'I': 0x908,
    'ii': 0x908,
    'u': 0x909,
    'U': 0x90A,
    'uu': 0x90A,
    'RRi': 0x90B,
    'R^i': 0x90B,
    'RRI': 0x960, # added by Anoop # extension 
    'R^I': 0x960,# added by Anoop # extension 
    'LLi': 0x90C,
    'L^i': 0x90C,
    'LLI': 0x961,# added by Anoop # extension 
    'L^I': 0x961,# added by Anoop # extension 
    '.e': 0x90E,   # added by Anoop # extension 
    'e': 0x90F,
    'ai': 0x910,
    '.o': 0x912,   # added by Anoop # extension 
    'o': 0x913,
    'au': 0x914,
    'k': 0x915,
    'kh': 0x916,
    'g': 0x917,
    'gh': 0x918,
    '~N': 0x919,
    'c': 0x91A,
    'ch': 0x91A,
    'Ch': 0x91B,
    'j': 0x91C,
    'jh': 0x91D,
    '~n': 0x91E,
    'T': 0x91F,
    'Th': 0x920,
    'D': 0x921,
    'Dh': 0x922,
    'N': 0x923,
    't': 0x924,
    'z': 0x936,
    'th': 0x925,
    'd': 0x926,
    'dh': 0x927,
    'n': 0x928,
    'p': 0x92A,
    'ph': 0x92B,
    'b': 0x92C,
    'bh': 0x92D,
    'm': 0x92E,
    'y': 0x92F,
    'r': 0x930,
    'l': 0x932,
    'L': 0x933, # added by anoop
    'ld': 0x933, # added by anoop
    'zh': 0x934, # added by anoop # extension
    'v': 0x935,
    'w': 0x935,
    'sh': 0x936,
    'Sh': 0x937,
    's': 0x938,
    'h': 0x939,
    ".a": 0x93D, # avagraha
    'OM': 0x950,
    'AUM': 0x950,
    '.': 0x0964,
    '..': 0x0965,
    '0': 0x0966,
    '1': 0x0967,
    '2': 0x0968,
    '3': 0x0969,
    '4': 0x096A,
    '5': 0x096B,
    '6': 0x096C,
    '7': 0x096D,
    '8': 0x096E,
    '9': 0x096F,
    # non-standard/obsolete iTrans variants still used in texts from
    # http://sanskrit.gde.to/
    '.h': 0x903,
    'N^': 0x919,
    'shh': 0x937,
    'JN': 0x91E,
     }
     
""" ITrans uses some characters only in common ligatures.

The easiest way to deal with these is to replace them with their
"normal consonant" equivalents before we try to transliterate.

(This assumes we are mainly transliterating iTrans inbound, and that 
the normal consonants are acceptable outbound. ITrans is not a good
choice for outbound anyway because it has so many ambiguities)

"""
_swapTable = {'GY': 'j~n', 'dny': 'j~n', 'x': 'kSh',
                    }

DevanagariTransliterationScheme('DEVANAGARI', 'ITRANS', ITRANS, _swapTable)

IAST = { \
    py23char(0x1E43): 0x902,
    py23char(0x1E25): 0x903,
    'a': 0x905,
    py23char(0x101): 0x906,
    'i': 0x907,
    py23char(0x12B): 0x908,
    'u': 0x909,
    py23char(0x16B): 0x90A,
    py23char(0x1E5B): 0x90B,
    py23char(0x1E37): 0x90C,
    'e': 0x90F,
    'ai': 0x910,
    'o': 0x913,
    'au': 0x914,
    'k': 0x915,
    'kh': 0x916,
    'g': 0x917,
    'gh': 0x918,
    py23char(0x1E45): 0x919,
    'c': 0x91A,
    'ch': 0x91B,
    'j': 0x91C,
    'jh': 0x91D,
    py23char(0xF1): 0x91E,
    py23char(0x1E6D): 0x91F,
    py23char(0x1E6D) +'h': 0x920,
    py23char(0x1E0D): 0x921,
    py23char(0x1E0D) + 'h': 0x922,
    py23char(0x1E47): 0x923,
    't': 0x924,
    'th': 0x925,
    'd': 0x926,
    'dh': 0x927,
    'n': 0x928,
    'p': 0x92A,
    'ph': 0x92B,
    'b': 0x92C,
    'bh': 0x92D,
    'm': 0x92E,
    'y': 0x92F,
    'r': 0x930,
    'l': 0x932,
    'v': 0x935,
    py23char(0x15B): 0x936,
    py23char(0x1E63): 0x937,
    's': 0x938,
    'h': 0x939,
    "'": 0x93D, # avagraha
    'O' + py23char(0x1E43): 0x950,
    '.': 0x0964,
    '..': 0x0965,
    '0': 0x0966,
    '1': 0x0967,
    '2': 0x0968,
    '3': 0x0969,
    '4': 0x096A,
    '5': 0x096B,
    '6': 0x096C,
    '7': 0x096D,
    '8': 0x096E,
    '9': 0x096F,
     }

DevanagariTransliterationScheme('DEVANAGARI', 'IAST', IAST)


""" CYRILLIC DATA

set up Cyrillic and the ISO 9:1995 (Russian) transliteration scheme.
    
The Cyrillic unicode range contains about 4x what contemporary Russian
uses - other languages & history wacky stuff. Set the full range up in case
anybody ever has occasion to use it.

"""

CharacterBlock('CYRILLIC', list(range(0x400, 0x510)))

_ISO9RUS = {\
	py23char(0x0CB): 0x401, # IO
	'A': 0x410,
	'B': 0x411,
	'V': 0x412,
	'G': 0x413,
	'D': 0x414,
	'E': 0x415,
	py23char(0x17D): 0x416, # ZHE
	'Z': 0x417,
	'I': 0x418,
	'J': 0x419,
	'K': 0x41a,
	'L': 0x41b,
	'M': 0x41c,
	'N': 0x41d,
	'O': 0x41e,
	'P': 0x41f,
	'R': 0x420,
	'S': 0x421,
	'T': 0x422,
	'U': 0x423,
	'F': 0x424,
	'H': 0x425,
	'C': 0x426, # TS
	py23char(0x10C): 0x427, # CH
	py23char(0x160): 0x428, # SH
	py23char(0x15C): 0x429, # SHCH
	py23char(0x2BA): 0x42a, # hard
	'Y': 0x42b,
	py23char(0x2B9): 0x42c, # soft
	py23char(0x0C8): 0x42d, # YE
	py23char(0x0DB): 0x42e, # YU
	py23char(0x0C2): 0x42f, # YA
	'a': 0x430,
	'b': 0x431,
	'v': 0x432,
	'g': 0x433,
	'd': 0x434,
	'e': 0x435,
	py23char(0x17E): 0x436, # zhe
	'z': 0x437,
	'i': 0x438,
	'j': 0x439,
	'k': 0x43a,
	'l': 0x43b,
	'm': 0x43c,
	'n': 0x43d,
	'o': 0x43e,
	'p': 0x43f,
	'r': 0x440,
	's': 0x441,
	't': 0x442,
	'u': 0x443,
	'f': 0x444,
	'h': 0x445,
	'c': 0x446, # ts
	py23char(0x10D): 0x447, # ch
	py23char(0x161): 0x448, # sh
	py23char(0x15D): 0x449, # shch
	# py23char(0x2BA): 0x44a, # hard - same upper & lowercase
	'y': 0x44b,
	# py23char(0x2B9): 0x44c, # soft - same upper & lowercase
	py23char(0xE8): 0x44d, # ye
	py23char(0x0FB): 0x44e, #yu
	py23char(0x0E2): 0x44f, # ya
	py23char(0x0EB): 0x451, #  io
    }

TransliterationScheme('CYRILLIC', 'ISO9RUS', _ISO9RUS)

