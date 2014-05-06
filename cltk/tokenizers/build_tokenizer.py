In [1]: import nltk

In [2]: language_punkt_vars = nltk.tokenize.punkt.PunktLanguageVars

In [3]: language_punkt_vars.sent_end_chars=('.', '?', ';', ':')

In [4]: with open('sents_cael.txt') as f:
    train_data = f.read()

In [6]: trainer = nltk.tokenize.punkt.PunktTrainer(train_data, language_punkt_vars)
  Abbreviation: [5.0545] c
  Abbreviation: [0.3420] sex
  Abbreviation: [50.5447] m
  Abbreviation: [15.1634] q
  Abbreviation: [17.6906] l
  Abbreviation: [0.9297] cn
  Abbreviation: [10.1089] p
  Rare Abbrev: putaverunt.
  Sent Starter: [42.0636] 'sed'
  Sent Starter: [48.3138] 'nam'

In [7]: params = trainer.get_params()

In [8]: sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(params)

In [11]: with open('phil1.txt') as f:
   ....:     to_be_tokenized = f.read()
   ....:     

for sentence in sbd.sentences_from_text(to_be_tokenized, realign_boundaries=True):
    print(sentence)
    print('---')

