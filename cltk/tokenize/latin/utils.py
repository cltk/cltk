if __name__ == "__main__":
    
    # http://nlpforhackers.io/splitting-text-into-sentences/
    
#    from nltk.corpus import gutenberg
# 
#    print(dir(gutenberg))
#    print(gutenberg.fileids())
#
#    text = ""
#    for file_id in gutenberg.fileids():
#        text += gutenberg.raw(file_id)
#
#    print(len(text))               # 11793318
    
    from cltk.corpus.latin.readers import latinlibrary
    text = latinlibrary.raw()

    from pprint import pprint
    from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer

    trainer = PunktTrainer()
    trainer.INCLUDE_ALL_COLLOCS = True
    trainer.train(text)

    tokenizer = PunktSentenceTokenizer(trainer.get_params())

    # Test the tokenizer on a piece of text
    sentences = """Q. Mucius augur multa narrare de C. Laelio socero suo memoriter et iucunde solebat nec dubitare illum in omni sermone appellare sapientem; ego autem a patre ita eram deductus ad Scaevolam sumpta virili toga, ut, quoad possem et liceret, a senis latere numquam discederem; itaque multa ab eo prudenter disputata, multa etiam breviter et commode dicta memoriae mandabam fierique studebam eius prudentia doctior. Quo mortuo me ad pontificem Scaevolam contuli, quem unum nostrae civitatis et ingenio et iustitia praestantissimum audeo dicere. Sed de hoc alias; nunc redeo ad augurem."""

    print(tokenizer.tokenize(sentences))
    # ['Mr. James told me Dr.', 'Brown is not available today.', 'I will try tomorrow.']

    # View the learned abbreviations
    print(tokenizer._params.abbrev_types)
    # set([...])

    # Here's how to debug every split decision
    for decision in tokenizer.debug_decisions(sentences):
        pprint(decision)
        print('=' * 30)

    tokenizer._params.abbrev_types.add('dr')

    print(tokenizer.tokenize(sentences))
    # ['Mr. James told me Dr. Brown is not available today.', 'I will try tomorrow.']

    for decision in tokenizer.debug_decisions(sentences):
        pprint(decision)
        print('=' * 30)