"""These stopwords are taken from 
- people.stanford.edu/widner/content/text-mining-middle-ages (slide 13)
- textifier.com/resources/common-english-words.txt
- en.wikipedia.org/wiki/Middle_English
- en.wiktionary.org/wiki/Category:Middle_English_prepositions
- en.wiktionary.org/wiki/Category:MIddle_English_determiners
- en.wiktionary.org/wiki/Category:MIddle_English_conjunctions"""

STOPS_LIST = ['ac',
			  'afore',
			  'ake',
			  'an',
			  'because',
			  'ek',
			  'fore',
			  'for',
			  'forthi',
			  'whan',
			  'whanne',
			  'whilis',
			  'if',
			  'yf',
			  'yif',
			  'yiff',
			  'yit',
			  'yet',
			  'and',
			  'or',
			  'any',
			  'but',
			  'a',
			  'y', 
			  'ne',
			  'no',
			  'not',
			  'nor',
			  'nat',
			  'however',
			  'o',
			  'than',
			  'n',
			  'nn',
			  'nnn',
			  'to',
			  'with',
			  'wyth',
			  'at',
			  'as',
			  'of',
			  'off',
			  'from',
			  'on',
			  'before',
			  'by',
			  'after',
			  'about',
			  'above',
			  'across',
			  'among',
			  'against',
			  'below',
			  'between',
			  'during',
			  'into',
			  'in',
			  'out',
			  'over',
			  'under',
			  'abord',
			  'aboven',
			  'afore',
			  'aftir',
			  'bi',
			  'bifor',
			  'bisyde',
			  'bitwixten',
			  'byfore',
			  'bytwene',
			  'down',
			  'doun',
			  'embe',
			  'fra',
			  'ine',
			  'mid',
			  'sanz',
			  'tyll',
			  'umbe',
			  'vnto',
			  'vpon',
			  'withouten',
			  'with',
			  'wth',
			  'wtout',
			  'can',
			  'cannot',
			  "can't",
			  't',
			  'could',
			  'did',
			  'do',
			  'does',
			  'wyl',
			  'will',
			  'would',
			  'haven',
			  'hast',
			  'haþ',
			  'havende',
			  'hadde',
			  'haddest',
			  'hadden',
			  'had',
			  "hadn't",
			  'has',
			  "hasn't",
			  'hasn',
			  'have',
			  "haven't",
			  'haven',
			  'having',
			  'be',
			  'ben',
			  'been',
			  'am',
			  'art',
			  'is',
			  'ys',
			  'aren',
			  'are',
			  "aren't",
			  'bende',
			  "isn't",
			  'isn',
			  'wæs',
			  'was', 
			  "wasn't",
			  'wasn',
			  'weren',
			  'were',
			  "weren't",
			  'þe',
			  'the',
			  'þat',
			  'þenne',
			  'þis',
			  'whiche',
			  'which',
			  'while',
			  'who',
			  'whom',
			  'what',
			  'when',
			  'where',
			  'why',
			  'that',
			  "that's",
			  's',
			  'there',
			  'ther',
			  'þer',
			  "there's",
			  'these',
			  'this',
			  'those',
			  'boþe',
			  'thilke',
			  'eiþer',
			  'either',
			  'neither',
			  'al',
			  'all',
			  'also',
			  'ane',
			  'ic',
			  'ich',
			  'i',
			  "i'd",
			  'd',
			  "i'll",
			  'll',
			  "i'm",
			  'm',
			  "i've",
			  've',
			  'me',
			  'mi',
			  'my',
			  'minen',
			  'min',
			  'mire',
			  'minre',
			  'myself',
			  'þu',
			  'þou',
			  'tu',
			  'þeou',
			  'thi',
			  'you',
			  'þe',
			  'þi',
			  'ti',
			  'þin',
			  'þyn',
			  'þeself',
			  "you'd",
			  "you'll",
			  "you're",
			  're',
			  "you've",
			  'your',
			  'yours',
			  'yourself',
			  'yourselves',
			  'thee',
			  'thy',
			  'thou',
			  'ye',
			  'thine',
			  'he',
			  "he'd",
			  "he'll",
			  "he's",
			  'she',
			  'sche',
			  "she'd",
			  "she'll",
			  "she's",
			  'her',
			  'heo',
			  'hie',
			  'hies',
			  'hire',
			  'hir',
			  'hers',
			  'hio',
			  'heore',
			  'herself',
			  'him',
			  'hine',
			  'hisse',
			  'hes',
			  'himself',
			  'his',
			  'hys',
			  'hym',
			  'hit',
			  'yt',
			  'it',
			  'its',
			  "it's",
			  'tis',
			  'twas',
			  'itself',
			  'þay',
			  'youre',
			  'hyr',
			  'hem',
			  'we',
			  "we'd",
			  "we'll",
			  "we're",
			  "we've",
			  'us',
			  'ous',
			  'our',
			  'ure',
			  'ures',
			  'urne',
			  'ours',
			  'oures',
			  'ourselves',
			  'their',
			  'theirs',
			  'them',
			  'themselves',
			  'thai',
			  'thei',
			  'they',
			  "they'd",
			  "they'll",
			  "they're",
			  "they've",
			  'whan',
	   		   "a", 
	      		  "about",
		         "above", 
		        
		         "across",
		         "after",
		         "afterwards",
		         "again",
		         "against", 
		          "all",
		         "almost", 
		         "alone",
		        "along",
		        "already",
		        "also",
		        "although",
		        "always",
		        "am",
		        "among",
		        "amongst",
		        "amoungst", 
		        "amount", 
		        "an", 
		        "and", 
		        "another", 
		        "any",
		        "anyhow",
		        "anyone",
		        "anything",
		        "anyway",
		        "anywhere", 
		        "are", 
		        "around", 
		        "as", 
		        "at", 
		        "back",
		        "be",
		        "became", 
		        "because",
		        "become",
		        "becomes", 
		        "becoming",
		        "been", 
		        "before", 
		        "beforehand",
		        "behind", 
		        "being",
		        "below", 
		        "beside", 
		        "besides", 
		        "between", 
		        "beyond", 
		        "bill", 
		        "both", 
		        "bottom",
		        "but", 
		        "by", 
		        "call",
		        "can", 
		        "cannot",
		        "cant", 
		        "co", 
		        "con",
		        "could", 
		        "couldnt", 
		        "cry",
		        "de", 
	                "describe",
	                "detail",
	      		"do", 
	      		"done",
	      		"down", 
	      		"due",
	      		"during",
	      		"each",
	      		"eg",
	      		"eight", 
	                "either",
	      		"eleven",
	      		"else",
	      		"elsewhere",
	      		"empty",
	      		"enough",
	      		"etc",
	      		"even",
	      		"ever", 
	                "every",
	      		"everyone",
	      		"everything",
	      		"everywhere",
	      		"except",
	      		"few",
	      		"fifteen",
	      		"fify",
	                "fill",
	      		"find",
	      		"fire", 
	      		"first",
	      		"five", 
	                "for",
	      		"former",
	      		"formerly",
	      		"forty",
	      		"found",
	      		"four",
	      		"from",
	      		"front", 
	                "full",
	      		"further", 
	      		"get",
	      		"give",
	      		"go",
	      		"had",
	      		"has",
	      		"hasnt",
	      		"have",
	      		"he",
	      		"hence",
	                "her",
	      		"here",
	      		"hereafter", 
	      		"hereby",
	      		"herein", 
	      		"hereupon",
	      		"hers", 
	      		"herself", 
	      		"him", 
	                "himself",
	      		"his",
	      		"how",
	      		"however", 
	      		"hundred",
	      		"ie", "if",
	      		"in",
	      		"inc",
	      		"indeed",
	      		"interest",
	                "into", 
	      		"is",
	      		"it",
	      		"its", 
	      		"itself",
	      		"keep",
	      		"last",
	      		"latter",
	      		"latterly", 
	      		"least",
	      		"less",
	      		"ltd", 
	                "made", 
	      		"many", 
	      		"may",
	      		"me", 
	      		"meanwhile", 
	      		"might", 
	      		"mill", 
	      		"mine",
	      		"more",
	      		"moreover",
	      		"most",
	      		"mostly", 
	                "move",
	      		"much",
	      		"must", 
	      		"my", 
	      		"myself",
	      		"name",
	      		"namely", 
	      		"neither",
	      		"never",
	      		"nevertheless", 
	      		"next", 
	      		"nine", 
	                "no", 
	      		"nobody",
	      		"none",
	      		"noone",
	      		"nor",
	      		"not",
	      		"nothing",
	      		"now",
	      		"nowhere", 
	      		"of",
	      		"off",
	      		"often",
	      		"on",
	      		"once", 
	                "one",
	      		"only",
	      		"onto",
	      		"or",
	      		"other",
	      		"others",
	      		"otherwise",
	      		"our",
	      		"ours",
	      		"ourselves",
	      		"out",
	      		"over",
	      		"own",
	                "part", 
	      		"per", 
		      "perhaps",
		      "please", 
		      "put", 
		      "rather",
		      "re",
		      "same", 

		      "see", 
		      "seem",
		      "seemed", 
		      "seeming",
		      "seems",

		      "serious",
		      "several",
		      "she",
		      "should", 
		      "show",
		      "side", 
		      "since", 
		      "sincere",
		      "six", 
		      "sixty", 
		      "so", 
		      "some", 
		      "somehow",

		      "someone", 
		      "something",
		      "sometime",
		      "sometimes", 
		      "somewhere", 
		      "still", 
		      "such", 
		      "system", 
		      "take",
		      "ten", 

		      "than", 
		      "that", 
		      "the",
		      "their",
		      "them", 
		      "themselves",
		      "then", 
		      "thence", 
		      "there",
		      "thereafter", 
		      "thereby",

		      "therefore", 
		      "therein",
		      "thereupon",
		      "these",
		      "they", 
		      "thickv", 
		      "thin",
		      "third", 
		      "this", 
		      "those", 
		      "though",

		      "three", 
		      "through", 
		      "throughout",
		      "thru",
		      "thus", 
		      "to", 
		      "together",
		      "too", 
		      "top", 
		      "toward",

		      "towards", 
		      "twelve",

		      "twenty",
		      "two", 
		      "un", 
		      "under",
		      "until",
		      "up", 
		      "upon", 
		      "us",
		      "very", 
		      "via",
		      "was", 
		      "we", 
		      "well", 
		      "were",
		      "what",

		      "whatever", 
		      "when",
		      "whence",
		      "whenever", 
		      "where", 
		      "whereafter", 
		      "whereas",
		      "whereby", 
		      "wherein", 
		      "whereupon", 

		      "wherever",

		      "whether",
		      "which",
		      "while", 
		      "whither", 
		      "who",
		      "whoever", 
		      "whole",
		      "whom", 
		      "whose", 
		      "why",
		      "will", 
		       "with"
		      ,
		      "within", 
		      "without",
		      "would",
		      "yet", 
		      "you",
		      "your", 
		      "yours", 
		      "yourself", 
		      "yourselves", 
		      "the"]

