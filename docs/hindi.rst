Hindi
********

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub repository <https://github.com/cltk>`_ (anything beginning with ``hindi_``) to discover available Hindi corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('hindi')

   In [3]: c.list_corpora
   Out[3]: 
           ['hindi_text_ltrc']


Tokenizer
=========

This tool can break a sentence into its constituent words. It simply splits the text into tokens using PunktLanguageVars.

.. code-block:: python

   In [1]: from cltk.tokenize.word import WordTokenizer as wt

   In [2]: import os

   In [3]: root = os.path.expanduser('~')

   In [4]: hindi_corpus = os.path.join(root,'cltk_data/hindi/text/hindi_text_ltrc')

   In [5]: hindi_text_path = os.path.join(hindi_corpus, 'miscellaneous/gandhi/main.txt')

   In [6]: hindi_text = open(hindi_text_path,'r').read()

   In [7]: hindi_text_tokenize = wt('hindi').tokenize(hindi_text)

   In [8]: hindi_text_tokenize[0:10]

   In [9]: print (hindi_text_tokenize[0:100])
   ['10्र', 'प्रति', 'ा', 'वापस', 'नहीं', 'ली', 'जातीएक', 'बार', 'कस्तुरबा', 'गांधी', 'बहुत', 'बीमार', 'हो', 'गईं।', 'जलर्', 'चिकित्सा', 'से', 'उन्हें', 'कोई', 'लाभ', 'नहीं', 'हुआ।', 'दूसरे', 'उपचार', 'किये', 'गये।', 'उनमे', 'भी', 'सफलता', 'नहीं', 'मिली।', 'अंत', 'में', 'गांधीजी', 'ने', 'उन्हें', 'नमक', 'और', 'दाल', 'छोडने', 'की', 'सलाह', 'दी।', 'परन्तु', 'इसके', 'लिए', 'बा', 'तैयार', 'नहीं', 'हुईं।', 'गांधीजी', 'ने', 'बहुत', 'समझाया', '', '.', 'पोथियों', 'से', 'प्रमाण', 'पढकर', 'सुनाये', '', '.', 'लेकर', 'सब', 'व्यर्थ।बा', 'बोलीं', '', '.', '"', 'कोई', 'आपसे', 'कहे', 'कि', 'दाल', 'और', 'नमक', 'छोड', 'दो', 'तो', 'आप', 'भी', 'नहीं', 'छोडेंगे।', '"', 'गांधीजी', 'ने', 'तुरन्त', 'प्रसÙ', 'होकर', 'कहा', '', '.', '"', 'तुम', 'गलत', 'समझ', 'रही', 'हो।', 'मुझे']



Another tool to tokenize the text into tokens but the difference is in the above, word followed by period are considered as a single token where as here words are seperate from punctuations.

.. code-block:: python

   In [10]: from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex as i_word
   
   In [11]: hindi_text_tokenize = i_word(hindi_text)

   In [12]: print(hindi_text_tokenize[0:100])
   ['10्र', 'प्रति', 'ा', 'वापस', 'नहीं', 'ली', 'जातीएक', 'बार', 'कस्तुरबा', 'गांधी', 'बहुत', 'बीमार', 'हो', 'गईं', '।', 'जलर्', 'चिकित्सा', 'से', 'उन्हें', 'कोई', 'लाभ', 'नहीं', 'हुआ', '।', 'दूसरे', 'उपचार', 'किये', 'गये', '।', 'उनमे', 'भी', 'सफलता', 'नहीं', 'मिली', '।', 'अंत', 'में', 'गांधीजी', 'ने', 'उन्हें', 'नमक', 'और', 'दाल', 'छोडने', 'की', 'सलाह', 'दी', '।', 'परन्तु', 'इसके', 'लिए', 'बा', 'तैयार', 'नहीं', 'हुईं', '।', 'गांधीजी', 'ने', 'बहुत', 'समझाया', '.', 'पोथियों', 'से', 'प्रमाण', 'पढकर', 'सुनाये', '.', 'लेकर', 'सब', 'व्यर्थ', '।', 'बा', 'बोलीं', '.', '"', 'कोई', 'आपसे', 'कहे', 'कि', 'दाल', 'और', 'नमक', 'छोड', 'दो', 'तो', 'आप', 'भी', 'नहीं', 'छोडेंगे', '।', '"', 'गांधीजी', 'ने', 'तुरन्त', 'प्रसÙ', 'होकर', 'कहा', '.', '"', 'तुम']

