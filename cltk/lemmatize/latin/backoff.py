from pprint import pprint

from nltk.tag.api import TaggerI
from nltk.tag.sequential import *

from cltk.lemmatize.latin.principal_parts import latin_pps, latin_verb_patterns, misc_latin_patterns, rn_patterns 
from cltk.lemmatize.latin.lemmatized_sentences import pos_lemmatized_sents

from cltk.lemmatize.latin.lookup import latin_model
from cltk.lemmatize.latin.old_lookup import LEMMATA as old_latin_model

from cltk.lemmatize.latin.regexp_patterns import verb_ending_patterns


def backoff_lemmatizer(train_sents, lemmatizer_classes, backoff=None):
    """from Python Text Processing with NLTK Cookbook"""
    for cls in lemmatizer_classes:
        backoff = cls(train_sents, backoff=backoff)
    return backoff

class LemmatizerI(TaggerI):
    pass

class SequentialBackoffLemmatizer(LemmatizerI, SequentialBackoffTagger):
    def __init__(self, backoff=None):
        """
        :param backoff: The backoff tagger that should be used for this tagger.
        """
        LemmatizerI.__init__(self)
        SequentialBackoffTagger.__init__(self, backoff)


    def lemmatize(self, tokens):
        return SequentialBackoffLemmatizer.tag(self, tokens)

    def choose_tag(self, tokens, index, history):
         return self.choose_lemma(tokens, index, history)


class DefaultLemmatizer(SequentialBackoffLemmatizer, DefaultTagger):
    def __init__(self, lemma=None):
        self._lemma = lemma
        SequentialBackoffLemmatizer.__init__(self, None)
        DefaultTagger.__init__(self, self._lemma)

    def choose_lemma(self, tokens, index, history):
        return DefaultTagger.choose_tag(self, tokens, index, history)


class IdentityLemmatizer(SequentialBackoffLemmatizer):
    def __init__(self, backoff=None):
        SequentialBackoffLemmatizer.__init__(self, backoff)
        
    def lemmatize(self, tokens):
        lemmas = []
        for i in enumerate(tokens):
            lemmas.append(i[1])
        return list(zip(tokens, lemmas))

    def choose_lemma(self, tokens, index, history):
        _lemma = tokens[index]
        return _lemma


class ModelLemmatizer(SequentialBackoffLemmatizer):
    def __init__(self, model, backoff=None):
        #print('MODEL LEMMATIZER ACTIVATED')
        SequentialBackoffLemmatizer.__init__(self, backoff)
        self.model = model

    def choose_lemma(self, tokens, index, history):
        keys = self.model.keys()
        if tokens[index] in keys:
            return self.model[tokens[index]]


class ContextLemmatizer(SequentialBackoffLemmatizer, ContextTagger):
    def __init__(self, context_to_lemmatize, backoff=None):
        SequentialBackoffLemmatizer.__init__(self, backoff)
        self._context_to_lemmatize = (context_to_lemmatize if context_to_lemmatize else {})
        ContextTagger.__init__(self, self._context_to_lemmatize, backoff)

    def choose_lemma(self, tokens, index, history):
        return ContextTagger.choose_tag(self, tokens, index, history)


class NgramLemmatizer(ContextLemmatizer, NgramTagger):
    def __init__(self, n, train=None, model=None, backoff=None, cutoff=0):
        self._n = n
        self._check_params(train, model)
        ContextLemmatizer.__init__(self, model, backoff)

        NgramTagger.__init__(self, self._n, train, model, backoff, cutoff)

        if train:
            self._train(train, cutoff)

    def context(self, tokens, index, history):
        return NgramTagger.context(self, tokens, index, history)


class UnigramLemmatizer(NgramLemmatizer, UnigramTagger):
    def __init__(self, train=None, model=None, backoff=None, cutoff=0):
        NgramLemmatizer.__init__(self, 1, train, model, backoff, cutoff)
        UnigramTagger.__init__(self,train, model, backoff, cutoff)


class RegexpLemmatizer(SequentialBackoffLemmatizer, RegexpTagger):
    def __init__(self, regexps, backoff=None):
        SequentialBackoffLemmatizer.__init__(self, backoff)
        RegexpTagger.__init__(self, regexps, backoff)
        #self._regexs = [(re.compile(regexp), replacement,) for regexp, replacement in regexps]

    def choose_lemma(self, tokens, index, history):
        for regexp, pattern in self._regexs:
            m = re.match(regexp, tokens[index])
            if m:
                return (m.group(1))+pattern
    
    #def choose_tag(self, tokens, index, history):
    #    return(self.choose_lemma(tokens, index, history))



class PPLemmatizer(RegexpLemmatizer):
    def __init__(self, regexps=verb_ending_patterns, backoff=None):
        #SequentialBackoffLemmatizer.__init__(self, backoff)
        RegexpLemmatizer.__init__(self, regexps, backoff)
        self._regexs = [(re.compile(regexp), num) for regexp, num in regexps] #Different compile to make use of principal parts dictionary structure
    
    def choose_lemma(self, tokens, index, history):
        for regexp in self._regexs:
            m = re.match(regexp[0], tokens[index])
            if m:
                root = m.group(1)
                match = [lemma for (lemma, pp) in latin_pps.items() if root == pp[regexp[1]]]
                if not match:
                    pass
                else:
                    return match[0]
        #return None


    #def __repr__(self):
    #    return '<Principal Parts Lemmatizer: size=%d>' % len(self._regexs)

class RomanNumeralLemmatizer(RegexpLemmatizer):             
    def __init__(self, regexps=rn_patterns, backoff=None):
        RegexpLemmatizer.__init__(self, regexps, backoff)
        #self._regexs = [(re.compile(regexp), replacement,) for regexp, replacement in regexps]
    
    # Check RegexpTagger—might be duplicate
    def choose_lemma(self, tokens, index, history):
        for regexp, pattern in self._regexs:
            m = re.match(regexp, tokens[index])
            if m:
                return pattern
        return None

class ContextPOSLemmatizer(ContextLemmatizer):

    def __init__(self, context_to_lemmatize, include=None, backoff=None):
        SequentialBackoffLemmatizer.__init__(self, backoff) # Not necessary; needs __init__ for ContextLemmatizer
        self.include = include
        self._context_to_tag = (context_to_lemmatize if context_to_lemmatize else {})

    def _get_pos_tags(self, tokens):

        from cltk.tag.pos import POSTag
        tagger = POSTag('latin')
        tokens = " ".join(tokens)
        tags = tagger.tag_ngram_123_backoff(tokens)
        tags = [tag[1][0].lower() if tag[1] else tag[1] for tag in tags]
        return tags

    def choose_lemma(self, tokens, index, history):
        if self.include:
            if tokens[index] not in self.include:
                return None
        history = self._get_pos_tags(tokens)
        context = self.context(tokens, index, history)
        suggested_lemma = self._context_to_tag.get(context)
        return suggested_lemma

    def choose_tag(self, tokens, index, history):
        #print(self.choose_lemma(tokens,index,history))
        return(self.choose_lemma(tokens, index, history))

    def _train(self, lemma_pos_corpus, cutoff=0):
        token_count = hit_count = 0

        # A context is considered 'useful' if it's not already lemmatized
        # perfectly by the backoff lemmatizer.
        useful_contexts = set()

        # Count how many times each tag occurs in each context.
        fd = ConditionalFreqDist()
        for sentence in lemma_pos_corpus:
            tokens, lemmas, poss = zip(*sentence)
            for index, (token, lemma, pos) in enumerate(sentence):
                # Record the event.
                token_count += 1
                #print(index)

                context = self.context(tokens, index, poss)
                #print(context)
                if context is None: continue
                #print(fd[context].most_common())
                #print(fd[context][lemma])
                fd[context][lemma] += 1

                # If the backoff got it wrong, this context is useful:
                if (self.backoff is None or
                            lemma != self.backoff.tag_one(tokens, index, lemmas[:index])):
                    useful_contexts.add(context)

        # Build the context_to_lemmatize table -- for each context, figure
        # out what the most likely lemma is. Only include contexts that
        # we've seen at least `cutoff` times.
        for context in useful_contexts:
            best_lemma = fd[context].max()
            hits = fd[context][best_lemma]
            #print(fd[context].most_common())
            #print(fd[context].max())
            #print(fd[context][best_lemma])
            if hits > cutoff:
                self._context_to_tag[context] = best_lemma
                hit_count += hits


class NgramPOSLemmatizer(ContextPOSLemmatizer):
    def __init__(self, n, train=None, model=None, include=None,
                 backoff=None, cutoff=0):
        self._n = n
        self._check_params(train, model)
        ContextPOSLemmatizer.__init__(self, model, include, backoff)

        if train:
            self._train(train, cutoff)

    def context(self, tokens, index, history):
        """
        Redefines context with look-ahead of length n.
        """
        lemma_context = tuple(history[index + 1: index + self._n ])
        return tokens[index], lemma_context


class BigramPOSLemmatizer(NgramPOSLemmatizer):

    def __init__(self, train=None, model=None, include=None,
                 backoff=None, cutoff=0):
        NgramPOSLemmatizer.__init__(self, 2, train, model,
                             include, backoff, cutoff)

class TrigramPOSLemmatizer(NgramPOSLemmatizer):

    def __init__(self, train=None, model=None,
                 backoff=None, cutoff=0):
        NgramPOSLemmatizer.__init__(self, 3, train, model,
                             backoff, cutoff)
if __name__ == "__main__":

    pos_train_sents = pos_lemmatized_sents[:3000]

    lemmatized_sents = [[(item[0], item[1]) for item in sent] for sent in pos_lemmatized_sents]
    train_sents = lemmatized_sents[:3000]

    test_sents = lemmatized_sents[3000:4000]



    backoffx = None
    #backoff0 = DefaultLemmatizer(lemma="UNK")
    #backoff1 = IdentityLemmatizer()
    #backoff1 = ModelLemmatizer(model={'emathios':'emathius'})
    #backoff2 = ModelLemmatizer(model=old_latin_model, backoff=backoff1)
    #backoff3 = RegexpLemmatizer(misc_latin_patterns, backoff=backoff2)
    #backoff4 = PPLemmatizer(backoff=backoff3)
    #backoff5 = UnigramLemmatizer(train_sents, backoff=backoff3)
    #backoff6 = ModelLemmatizer(model=latin_model, backoff=backoff5)
    #lemmatizer = BigramPOSLemmatizer(pos_train_sents, include=['cum'], backoff=backoff5)
    #lemmatizer = backoff6
    
    lemmatizer = ModelLemmatizer(model=old_latin_model)

    from cltk.tokenize.word import WordTokenizer
    tokenizer = WordTokenizer('latin')

    from cltk.stem.latin.j_v import JVReplacer
    jv = JVReplacer()

    # Cicero, De Partitione Oratoria 108.1
    # General example
    sent = 'Cum serialem proxima autem aut plura significantur scripto propter verbi aut verborum ambiguitatem' #, ut liceat ei qui contra dicat eo trahere significationem scripti quo expediat ac velit, aut, si ambigue scriptum non sit, vel a verbis voluntatem et sententiam scriptoris abducere vel alio se eadem de re contrarie scripto defendere, tum disceptatio ex scripti contentione exsistit, ut in ambiguis disceptetur quid maxime significetur, in scripti sententiaeque contentione, utrum potius sequatur iudex, in contrariis scriptis, utrum magis sit comprobandum.'

    comp_sents = [[('cum', 'cum2'), ('serialem', 'serialis'), ('proxima', 'propior'), ('autem', 'autem'), ('aut', 'aut'), ('plura', 'multus'), ('significantur', 'significo'), ('scripto', 'scribo'), ('propter', 'propter'), ('uerbi', 'uerbum'), ('aut', 'aut'), ('uerborum', 'uerbum'), ('ambiguitatem', 'ambiguitas')]]



    # # Cic. Pro Font. 43.1
    # # Example for lemmatizing names
    # sent = 'Ceterum antequam destinata componam, repetendum     uidetur qualis status urbis, quae mens exercituum, quis habitus prouinciarum, quid in toto terrarum orbe ualidum, quid     aegrum fuerit, ut non modo casus euentusque rerum, qui     plerumque fortuiti sunt, sed ratio etiam causaeque noscantur. finis Neronis ut laetus primo gaudentium impetu fuerat,     ita uarios motus animorum non modo in urbe apud patres aut     populum aut urbanum militem, sed omnis legiones ducesque conciuerat, euulgato imperii arcano posse principem alibi     quam Romae fieri. sed patres laeti, usurpata statim libertate     licentius ut erga principem nouum et absentem; primores     equitum proximi gaudio patrum; pars populi integra et magnis domibus adnexa, clientes libertique damnatorum et exulum in spem erecti: plebs sordida et circo ac theatris sueta,     simul deterrimi seruorum, aut qui adesis bonis per dedecus     Neronis alebantur, maesti et rumorum auidi.'
    #
    # comp_sents = [[('ceterum', 'ceterus'), ('antequam', 'antequam'), ('destinata', 'destino'), ('componam', 'compono'),
    #                (',', ','), ('repetendum', 'repeto'), ('uidetur', 'uideo'), ('qualis', 'qualis'),
    #                ('status', 'status'), ('urbis', 'urbs'), (',', ','), ('quae', 'qui'), ('mens', 'mens'),
    #                ('exercituum', 'exercitus'), (',', ','), ('quis', 'quis'), ('habitus', 'habitus'),
    #                ('prouinciarum', 'prouincia'), (',', ','), ('quid', 'quis'), ('in', 'in'), ('toto', 'totus'),
    #                ('terrarum', 'terra'), ('orbe', 'orbis'), ('ualidum', 'ualidus'), (',', ','), ('quid', 'quis'),
    #                ('aegrum', 'aeger'), ('fuerit', 'sum'), (',', ','), ('ut', 'ut'), ('non', 'non'), ('modo', 'modo'),
    #                ('casus', 'casus'), ('euentus', 'euentus'), ('-que', '-que'), ('rerum', 'res'), (',', ','),
    #                ('qui', 'qui'), ('plerumque', 'plerusque'), ('fortuiti', 'fortuitus'), ('sunt', 'sum'), (',', ','),
    #                ('sed', 'sed'), ('ratio', 'ratio'), ('etiam', 'etiam'), ('causae', 'causa'), ('-que', '-que'),
    #                ('noscantur', 'nosco'), ('.', '.'), ('finis', 'finis'), ('neronis', 'nero'), ('ut', 'ut'),
    #                ('laetus', 'laetus'), ('primo', 'primus'), ('gaudentium', 'gaudeo'), ('impetu', 'impetus'),
    #                ('fuerat', 'sum'), (',', ','), ('ita', 'ita'), ('uarios', 'uarius'), ('motus', 'motus'),
    #                ('animorum', 'animus'), ('non', 'non'), ('modo', 'modo'), ('in', 'in'), ('urbe', 'urbs'),
    #                ('apud', 'apud'), ('patres', 'pater'), ('aut', 'aut'), ('populum', 'populus'), ('aut', 'aut'),
    #                ('urbanum', 'urbanus'), ('militem', 'miles'), (',', ','), ('sed', 'sed'), ('omnis', 'omnis'),
    #                ('legiones', 'legio'), ('duces', 'dux'), ('-que', '-que'), ('conciuerat', 'concieo'), (',', ','),
    #                ('euulgato', 'euulgo'), ('imperii', 'imperium'), ('arcano', 'arcanus'), ('posse', 'possum'),
    #                ('principem', 'princeps'), ('alibi', 'alibi'), ('quam', 'quam'), ('romae', 'roma'), ('fieri', 'fio'),
    #                ('.', '.'), ('sed', 'sed'), ('patres', 'pater'), ('laeti', 'laetus'), (',', ','),
    #                ('usurpata', 'usurpo'), ('statim', 'statim'), ('libertate', 'libertas'), ('licentius', 'licet'),
    #                ('ut', 'ut'), ('erga', 'erga'), ('principem', 'princeps'), ('nouum', 'nouus'), ('et', 'et'),
    #                ('absentem', 'absum'), (';', ';'), ('primores', 'primoris'), ('equitum', 'eques'),
    #                ('proximi', 'propior'), ('gaudio', 'gaudium'), ('patrum', 'pater'), (';', ';'), ('pars', 'pars'),
    #                ('populi', 'populus'), ('integra', 'integer'), ('et', 'et'), ('magnis', 'magnus'),
    #                ('domibus', 'domus'), ('adnexa', 'adnecto'), (',', ','), ('clientes', 'cliens'),
    #                ('liberti', 'libertus'), ('-que', '-que'), ('damnatorum', 'damnator'), ('et', 'et'),
    #                ('exulum', 'exsul'), ('in', 'in'), ('spem', 'spes'), ('erecti', 'erigo'), (':', ':'),
    #                ('plebs', 'plebs'), ('sordida', 'sordidus'), ('et', 'et'), ('circo', 'circus'), ('ac', 'atque'),
    #                ('theatris', 'theatrum'), ('sueta', 'suesco'), (',', ','), ('simul', 'simul'),
    #                ('deterrimi', 'deterior'), ('seruorum', 'seruus'), (',', ','), ('aut', 'aut'), ('qui', 'qui'),
    #                ('adesis', 'adedo'), ('bonis', 'bonus'), ('per', 'per'), ('dedecus', 'dedecus'), ('neronis', 'nero'),
    #                ('alebantur', 'alo'), (',', ','), ('maesti', 'maestus'), ('et', 'et'), ('rumorum', 'rumor'),
    #                ('auidi', 'auidus'), ('.', '.')]]

#     sent = """Bella per Emathios plus quam ciuilia campos
#      iusque datum sceleri canimus, populumque potentem
#      in sua uictrici conuersum uiscera dextra
#      cognatasque acies, et rupto foedere regni
#      certatum totis concussi uiribus orbis
#      in commune nefas, infestisque obuia signis
#      signa, pares aquilas et pila minantia pilis.
#            quis furor, o ciues, quae tanta licentia ferri?
#      gentibus inuisis Latium praebere cruorem
#      cumque superba foret Babylon spolianda tropaeis
#      Ausoniis umbraque erraret Crassus inulta
#      bella geri placuit nullos habitura triumphos?
#      heu, quantum terrae potuit pelagique parari
#      hoc quem ciuiles hauserunt sanguine dextrae,
#      unde uenit Titan et nox ubi sidera condit
#      quaque dies medius flagrantibus aestuat horis
#      et qua bruma rigens ac nescia uere remitti
#      astringit Scythico glacialem frigore pontum!
#      sub iuga iam Seres, iam barbarus isset Araxes
#      et gens siqua iacet nascenti conscia Nilo.
#      tum, si tantus amor belli tibi, Roma, nefandi,
#      totum sub Latias leges cum miseris orbem,
#      in te uerte manus: nondum tibi defuit hostis.
#      at nunc semirutis pendent quod moenia tectis
#      urbibus Italiae lapsisque ingentia muris
#      saxa iacent nulloque domus custode tenentur
#      rarus et antiquis habitator in urbibus errat,
#      horrida quod dumis multosque inarata per annos
#      Hesperia est desuntque manus poscentibus aruis,
#      non tu, Pyrrhe ferox, nec tantis cladibus auctor
#      Poenus erit: nulli penitus descendere ferro
#      contigit; alta sedent ciuilis uolnera dextrae."""
#     
#     comp_sents = [[('bella', 'bellum'), ('per', 'per'), ('emathios', 'emathius'), ('plus', 'multus'), ('quam', 'quam'), ('ciuilia', 'ciuilis'), ('campos', 'campus'), ('ius', 'ius'), ('-que', '-que'), ('datum', 'do'), ('sceleri', 'scelus'), ('canimus', 'cano'), (',', ','), ('populum', 'populus'), ('-que', '-que'), ('potentem', 'potens'), ('in', 'in'), ('sua', 'suus'), ('uictrici', 'uictrix'), ('conuersum', 'conuerto'), ('uiscera', 'uiscera'), ('dextra', 'dexter'), ('cognatas', 'cognatus'), ('-que', '-que'), ('acies', 'acies'), (',', ','), ('et', 'et'), ('rupto', 'rumpo'), ('foedere', 'foedus'), ('regni', 'regnum'), ('certatum', 'certo'), ('totis', 'totus'), ('concussi', 'concutio'), ('uiribus', 'uis'), ('orbis', 'orbis'), ('in', 'in'), ('commune', 'communis'), ('nefas', 'nefas'), (',', ','), ('infestis', 'infestus'), ('-que', '-que'), ('obuia', 'obuius'), ('signis', 'signum'), ('signa', 'signum'), (',', ','), ('pares', 'par'), ('aquilas', 'aquila'), ('et', 'et'), ('pila', 'pilum'), ('minantia', 'minor'), ('pilis', 'pilum'), ('.', '.'), ('quis', 'quis'), ('furor', 'furor'), (',', ','), ('o', 'o'), ('ciues', 'ciuis'), (',', ','), ('quae', 'qui'), ('tanta', 'tantus'), ('licentia', 'licentia'), ('ferri', 'ferrum'), ('?', '?'), ('gentibus', 'gens'), ('inuisis', 'inuideo'), ('latium', 'latium'), ('praebere', 'praebeo'), ('cruorem', 'cruor'), ('cumque', 'cumque'), ('superba', 'superbus'), ('foret', 'sum'), ('babylon', 'babylon'), ('spolianda', 'spolio'), ('tropaeis', 'tropaeum'), ('ausoniis', 'ausonius'), ('umbra', 'umbra'), ('-que', '-que'), ('erraret', 'erro'), ('crassus', 'crassus'), ('inulta', 'inultus'), ('bella', 'bellum'), ('geri', 'gero'), ('placuit', 'placeo'), ('nullos', 'nullus'), ('habitura', 'habeo'), ('triumphos', 'triumphus'), ('?', '?'), ('heu', 'heu'), (',', ','), ('quantum', 'quantus'), ('terrae', 'terra'), ('potuit', 'possum'), ('pelagi', 'pelagus'), ('-que', '-que'), ('parari', 'paro'), ('hoc', 'hic'), ('quem', 'qui'), ('ciuiles', 'ciuilis'), ('hauserunt', 'haurio'), ('sanguine', 'sanguis'), ('dextrae', 'dexter'), (',', ','), ('unde', 'unde'), ('uenit', 'uenio'), ('titan', 'titan'), ('et', 'et'), ('nox', 'nox'), ('ubi', 'ubi'), ('sidera', 'sidus'), ('condit', 'condo'), ('qua', 'qui'), ('-que', '-que'), ('dies', 'dies'), ('medius', 'medius'), ('flagrantibus', 'flagro'), ('aestuat', 'aestuo'), ('horis', 'hora'), ('et', 'et'), ('qua', 'qui'), ('bruma', 'bruma'), ('rigens', 'rigeo'), ('ac', 'atque'), ('nescia', 'nescius'), ('uere', 'uerus'), ('remitti', 'remitto'), ('astringit', 'astringo'), ('scythico', 'scythicus'), ('glacialem', 'glacialis'), ('frigore', 'frigus'), ('pontum', 'pontus'), ('!', '!'), ('sub', 'sub'), ('iuga', 'iugum'), ('iam', 'iam'), ('seres', 'seres'), (',', ','), ('iam', 'iam'), ('barbarus', 'barbarus'), ('isset', 'eo'), ('araxes', 'araxes'), ('et', 'et'), ('gens', 'gens'), ('siqua', 'siquis'), ('iacet', 'iaceo'), ('nascenti', 'nascor'), ('conscia', 'conscius'), ('nilo', 'nilus'), ('.', '.'), ('tum', 'tum'), (',', ','), ('si', 'si'), ('tantus', 'tantus'), ('amor', 'amor'), ('belli', 'bellum'), ('tibi', 'tu'), (',', ','), ('roma', 'roma'), (',', ','), ('nefandi', 'nefandus'), (',', ','), ('totum', 'totus'), ('sub', 'sub'), ('latias', 'latius'), ('leges', 'lex'), ('cum', 'cum2'), ('miseris', 'mitto'), ('orbem', 'orbis'), (',', ','), ('in', 'in'), ('te', 'tu'), ('uerte', 'uerto'), ('manus', 'manus'), (':', ':'), ('nondum', 'nondum'), ('tibi', 'tu'), ('defuit', 'desum'), ('hostis', 'hostis'), ('.', '.'), ('at', 'at'), ('nunc', 'nunc'), ('semirutis', 'semirutus'), ('pendent', 'pendeo'), ('quod', 'qui'), ('moenia', 'moenia'), ('tectis', 'tectum'), ('urbibus', 'urbs'), ('italiae', 'italia'), ('lapsis', 'labor'), ('-que', '-que'), ('ingentia', 'ingens'), ('muris', 'murus'), ('saxa', 'saxum'), ('iacent', 'iaceo'), ('nullo', 'nullus'), ('-que', '-que'), ('domus', 'domus'), ('custode', 'custos'), ('tenentur', 'teneo'), ('rarus', 'rarus'), ('et', 'et'), ('antiquis', 'antiquus'), ('habitator', 'habitator'), ('in', 'in'), ('urbibus', 'urbs'), ('errat', 'erro'), (',', ','), ('horrida', 'horridus'), ('quod', 'qui'), ('dumis', 'dumus'), ('multos', 'multus'), ('-que', '-que'), ('inarata', 'inaratus'), ('per', 'per'), ('annos', 'annus'), ('hesperia', 'hesperia'), ('est', 'sum'), ('desunt', 'desum'), ('-que', '-que'), ('manus', 'manus'), ('poscentibus', 'posco'), ('aruis', 'aruum'), (',', ','), ('non', 'non'), ('tu', 'tu'), (',', ','), ('pyrrhe', 'pyrrhus'), ('ferox', 'ferox'), (',', ','), ('nec', 'neque'), ('tantis', 'tantus'), ('cladibus', 'clades'), ('auctor', 'auctor'), ('poenus', 'poenus'), ('erit', 'sum'), (':', ':'), ('nulli', 'nullus'), ('penitus', 'penitus'), ('descendere', 'descendo'), ('ferro', 'ferrum'), ('contigit', 'contingo'), (';', ';'), ('alta', 'altus'), ('sedent', 'sedeo'), ('ciuilis', 'ciuilis'), ('uolnera', 'uolnus'), ('dextrae', 'dexter'), ('.', '.')]]

#     sent = 'Cum autem aut plura significantur scripto propter verbi aut verborum ambiguitatem, ut liceat ei qui contra dicat eo trahere significationem scripti quo expediat ac velit, aut, si ambigue scriptum non sit, vel a verbis voluntatem et sententiam scriptoris abducere vel	alio se eadem de re contrarie scripto defendere, tum disceptatio ex scripti contentione exsistit, ut	in ambiguis disceptetur quid maxime significetur, in scripti sententiaeque contentione, utrum potius sequatur iudex, in contrariis scriptis, utrum magis sit comprobandum.'
# 
#     comp_sents = [
#         [('cum', 'cum2'), ('autem', 'autem'), ('aut', 'aut'), ('plura', 'multus'), ('significantur', 'significo'),
#          ('scripto', 'scribo'), ('propter', 'propter'), ('uerbi', 'uerbum'), ('aut', 'aut'), ('uerborum', 'uerbum'),
#          ('ambiguitatem', 'ambiguitas'), (',', ','), ('ut', 'ut'), ('liceat', 'licet'), ('ei', 'is'), ('qui', 'qui'),
#          ('contra', 'contra'), ('dicat', 'dico'), ('eo', 'is'), ('trahere', 'traho'),
#          ('significationem', 'significatio'), ('scripti', 'scribo'), ('quo', 'quo'), ('expediat', 'expedio'),
#          ('ac', 'atque'), ('uelit', 'uolo'), (',', ','), ('aut', 'aut'), (',', ','), ('si', 'si'),
#          ('ambigue', 'ambiguus'), ('scriptum', 'scribo'), ('non', 'non'), ('sit', 'sum'), (',', ','), ('uel', 'uel'),
#          ('a', 'ab'), ('uerbis', 'uerbum'), ('uoluntatem', 'uoluntas'), ('et', 'et'), ('sententiam', 'sententia'),
#          ('scriptoris', 'scriptor'), ('abducere', 'abduco'), ('uel', 'uel'), ('alio', 'alius'), ('se', 'sui'),
#          ('eadem', 'idem'), ('de', 'de'), ('re', 'res'), ('contrarie', 'contrarius'), ('scripto', 'scribo'),
#          ('defendere', 'defendo'), (',', ','), ('tum', 'tum'), ('disceptatio', 'disceptatio'), ('ex', 'ex'),
#          ('scripti', 'scribo'), ('contentione', 'contentio'), ('exsistit', 'exsisto'), (',', ','), ('ut', 'ut'),
#          ('in', 'in'), ('ambiguis', 'ambiguus'), ('disceptetur', 'discepto'), ('quid', 'quis'), ('maxime', 'magnus'),
#          ('significetur', 'significo'), (',', ','), ('in', 'in'), ('scripti', 'scribo'), ('sententiae', 'sententia'),
#          ('-que', '-que'), ('contentione', 'contentio'), (',', ','), ('utrum', 'utrum'), ('potius', 'potis'),
#          ('sequatur', 'sequor'), ('iudex', 'iudex'), (',', ','), ('in', 'in'), ('contrariis', 'contrarius'),
#          ('scriptis', 'scribo'), (',', ','), ('utrum', 'utrum'), ('magis', 'magis'), ('sit', 'sum'),
#          ('comprobandum', 'comprobo'), ('.', '.')]]

    sent = sent.lower()
    sent = jv.replace(sent)

    tokens = tokenizer.tokenize(sent)


    lemmas = lemmatizer.lemmatize(tokens)

    #pprint(lemmas)

    compare = list(zip(lemmas, comp_sents[0]))

    print('\n-----CORRECT LEMMAS-----\n')
    for item in compare:
        if item[0] == item[1]:
            print("Result: ", item[0], "Correct: ", item[1])

    print('\n-----INCORRECT LEMMAS-----\n')
    for item in compare:
        if item[0] != item[1] and item[0][1] != None:
            print("Result: ", item[0], "Correct: ", item[1])
            
    print('\n-----MISSED LEMMAS-----\n')
    for item in compare:
        if item[0][1] == None:
            print("Result: ", item[0], "Correct: ", item[1])


    acc = lemmatizer.evaluate(test_sents)
    print('{:.2%}'.format(acc))

