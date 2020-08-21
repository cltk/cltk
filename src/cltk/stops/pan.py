"""
Panjabi: 'Nimit Bhardwaj <nimitbhardwaj@gmail.com>'. Sahib Singh, from the site http://gurbanifiles.org/gurmukhi/index.htm, these words are the most frequent words in the Guru Granth Sahib

Note: This is in the `Gurmukhi alphabet <https://en.wikipedia.org/wiki/Gurmukhi>`_.
"""

STOPS = [
    "ਦੇ",  # used to show the possession
    "ਦੀ",  # used same as above but is just a feminine of above words
    "ਵਿਚ",  # used as preposition, for 'inside'
    "ਦਾ",  # again used as possession
    "ਨੂੰ",  #  stop word has no meaning on its own, but used in sentences
    "ਹੈ",  # usually used at the end of sentences, shows present tense
    "ਹੀ",  # again a stop word without any meaning
    "ਹੇ",  # used in same sence as 'Oh' word
    "ਕੇ",  # same used as the for possession, but it is close to hindi
    "ਉਸ",  # used in sense of 'his/her'
    "ਨਹੀਂ",  # means no of denial
    "ਤੇ",  # used for 'on' or 'after'
    "ਉਹ",  # used as 'he'
    "ਤੋਂ",  # used as 'after this'
    "ਨਾਲ",  # means 'with'
    "ਹੋ",  # used like 'doing'
    "ਇਹ",  # means 'this'
    "ਭੀ",  # means 'also'
    "ਨੇ",  # a stop word, without meaning on its own, difficult to teach its meaning
    "ਕਰ",  # means 'doing'
    "ਜਿਸ",  # used as 'who'
    "ਇਸ",  # used as 'this' refer to an object
    "ਆਪਣੇ",  # means 'our'
    "ਜੋ",  # used like 'who' but may have different meanings at different times
    "ਮੈਂ",  # means 'me'
    "ਕੋਈ",  # used like 'any' or 'anyone'
    "ਵਾਲਾ",  # used in sense like having a property of something
    "ਆਪ",  # means 'myself'
    "ਤੂੰ",  # many meanings depend on situation, may be used for 'after sometime' or 'after some place'
    "ਕਰਦਾ",  # similar to 'doing'
    "ਕਿ",  # a type of connector connect sentences similar way as 'because' does
    "ਉਹਨਾਂ",  # used as 'they'
    "ਜੀ",  # used as 'yes' but by giving some respect
    "ਤਾਂ",  # used as 'after'
    "ਕਰਨ",  # used as 'doing'
    "ਸਭ",  # means 'everyone'
    "ਜਾ",  # means 'going'
    "ਰਹਿੰਦਾ",  # means 'living' or 'live there'
    "ਵਾਲੇ",  # similar to 'ਵਾਲਾ'
    "ਹਨ",  # similar to 'ਹੈ' but used usually with plural
    "ਹੋਰ",  # used as 'and'
    "ਪਰ",  # means 'but'
    "ਜੇ",  # means 'if'
    "ਕੀ",  # various meanings like 'what'
    "ਜਾਂਦੇ",  # means 'going'
    "ਅਤੇ",  # means 'and'
    "ਕਿਸੇ",  # used as 'who' or 'whoever'
    "ਨਾਹ",  # used for denial
    "ਹੋਇਆ",  # used for 'work has done'
    "ਰਿਹਾ",  # used as 'work going on'
    "ਜਾਂਦੀ",  # used as 'going'
    "ਮਿਲ",  # means 'meet'
    "ਉਤੇ",  # used as 'above'
    "ਹੁੰਦਾ",  # a stopword used to denote present tense
    "ਤੇਰੇ",  # means 'yours'
    "ਰਹਾਉ",  # means 'liveable'
    "ਆ",  # close to meaning 'comming' but not exactly same
    "ਹੋਏ",  # close to meaning present but its not exactly same
    "ਦੂਰ",  # means 'far'
    "ਬਿਨਾ",  # means 'without'
    "ਪੈਦਾ",  # means 'birth'
    "ਲੈਂਦਾ",  # means 'taking'
    "ਮੈਨੂੰ",  # used like 'me'
    "ਕਾ",  # used like 'his' but close to hindi
    "ਦੇਂਦਾ",  # used as 'giving'
    "ਲਈ",  # no prefect meaning in engilish, but is close to 'for'
    "ਕਿਰਪਾ",  # means 'please'
    "ਦੇਣ",  # means like 'giving'
    "ਹਰ",  # used like 'every'
    "ਰਹਿੰਦੇ",  # means 'living'
    "ਮੇਰਾ",  # means 'mine'or 'my'
    "ਜੀਵਾਂ",  # means 'like'
    "ਪੈ",  # a word without any meaning, but we can say that it means like 'lie down', under some circumstances
    "ਹਰੇਕ",  # means 'everyone'
    "ਤੇਰੀ",  # means 'yours'
    "ਤੇਰਾ",  # same as above meaning
    "ਕਰਦੇ",  # used like 'they do' or 'he do'
    "ਆਪਣਾ",  # means 'our'
    "ਸਕਦਾ",  # usually used like 'able'
    "ਜਦੋਂ",  # used as 'when'
    "ਬਣ",  # usually used like 'made'
    "ਕਰਿ",  # used as 'do' but not used in modern punjabi
    "ਹੋਈ",  # usually used like 'happens'
    "ਦੀਆਂ",  # many meaning not clear but one of them is 'his possession'
    "ਥਾਂ",  # means 'place'
    "ਆਪਣੀ",  # means 'our'
    "ਕੁਝ",  # means 'something'
    "ਪੈਂਦਾ",  # no clear meaning
    "ਵਾਲੀ",  # means 'having property'
    "ਵੇਲੇ",  # used like 'saga' or 'time' or 'time of day'
    "ਆਪੇ",  # used like 'you'
    "ਆਦਿਕ",  # means like 'etc.'
    "ਵਾਸਤੇ",  # used like 'for sake of'
    "ਇਹਨਾਂ",  # used like 'their'
    "ਕਦੇ",  # used like 'ever'
    "ਮਨੁ",  # old punjabi word means 'assume'
    "ਹੋਇ",  # means 'done'
    "ਰਹੇ",  # means 'lived'
    "ਉਹੀ",  # means like 'he/she'
    "ਰਹਿ",  # no specific meaning, used with 'doing' but does not means 'doing'
    "ਮੇਰੀ",  # means 'mine'
    "ਵਿਚੋਂ",  # used like 'inside'
    "ਤਾ",  # usually used like 'submission'
    "ਪਾਇਆ",  # used for many meanins like 'wear' and 'found'
    "ਕੀਤਾ",  # means 'done'
    "ਲੈ",  # means like 'taken'
    "ਪਾ",  # used like 'worn'
    "ਸਾਰੀ",  # used like 'all'
    "ਕਈ",  # means 'many' but not know how many
    "ਲਿਆ",  # means 'taken' or used with 'done'
    "ਦਿੱਤਾ",  # means 'given'
    "ਤਰ੍ਹਾਂ",  # means 'ways'
    "ਕੰਮ",  # means 'job'
    "ਸਮਝ",  # means 'understanding'
    "ਆਪਿ",  # means 'ourselves'
    "ਜਿਵੇਂ",  # means 'like'
    "ਉੱਤੇ",  # means 'on'
    "ਤਦੋਂ",  # used like 'when' but after some event
    "ਕੋ",  # no meanings on its own
    "ਨਾ",  # used like denial or may be used 'name'
    "ਹਾਂ",  # used for ending the sentences
    "ਮੈ",  # means 'me'
    "ਨੰ:",  # no meaning on its own
    "ਸੀ",  # used to end sentences but denote past tense
    "ਨਾਹੀ",  # means no or denial
    "ਫਿਰ",  # means 'then' but this word is close to hindi
    "ਇਉਂ",  # old punjabi word close to meaning 'this way'
    "ਉਸੇ",  # old punjabi word meaning 'he/she'
    "ਰੇ",  # used like 'Oh'
    "ਸੇ",  # no meaning on its own
    "ਇਹੁ",  # means 'this way'
    "ਕਿਸ",  # used like 'whoes' or 'who'
    "ਵਲ",  # used like 'his/her side' like 'giving edge to'
]
