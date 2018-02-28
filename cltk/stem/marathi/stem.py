import re
from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex as i_word

def stem(text):
	text=text.lower()
	stemmed_text=''
	tokenized_text=i_word(text)
	for word in tokenized_text:
		word = matchremove_verb_endings(word)
		stemmed_text += word + ' '
	return stemmed_text



def matchremove_verb_endings(word):
	verb_endings=["त",  "तो" ,  "ते", "तोस", "तेस", "तात", "ईन", "ऊ", "शील", "आल" , "एल", "तील",
				 "लो", "ले", "लास", "लीस", "लात", "ला", "ली", "ले", "ल्या", 	
				"ताना", "णार", "णारा", "णारी", "णारे", "णाऱ्या", "लेला", "लेली"
				, "लेले", "लेल्या", "का", "को" ]
	for ending in verb_endings:
		if word ==ending:
			word=word
		break
		if word.endswith(ending):
			word = re.sub(r'{0}$'.format(ending), '', word)
		break
		return word









