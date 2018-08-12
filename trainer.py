import string

def parseFile(fname, stripPunc=False, stripCaps=False):
    """  Opens a file, optionally strips it of punctuation, and splits it into words

    :param fname:       the full or relative path to the file to be opened
    :param stripPunc:   True to remove all punctuation listed in punc, leaving just characters to form words
    :param stripCaps:   True to strip capitalization from words that meet all the following criteria:
                            - first letter or entire words capitalized
                            - only appear capped following sentenceEndingPunc
                            - appears at least once without capitalization when doc examined ignoring punctuation
    :return:            An ordered immutable iterable where each element is a word in the file
    """

    with open(fname, mode='rt', buffering=1) as f:
        words = f.read().split()
    if stripPunc:
        words = [w.translate(strippunctrans) for w in words]
    if stripCaps:
        tostrip = {w for w in _getCapped(words).difference(_getCappedWithoutBeginningSentence(words))
                   if w.lower().translate(strippunctrans) in _getNoPunc(words)}
        words = [w.lower() if w in tostrip else w for w in words]
    return tuple(words)


def getGraph(words, n, initgraph={}):
    """ Returns a graph

    :param words:
    :param n:
    :param initgraph:
    :return:            a dict of dicts, with keys in the outer dict representing distinct n-grams
                        the inner dict keys are the n-grams that follow the key in the outer dict
                        the value of the inner dict is a TransitionStats object, which has count and prob properties
    """
    if initgraph and n != len(list(initgraph.keys())[0].split()):
        raise ValueError('You can only add n-grams of the same size to an existing graph.')

    ngrams = [' '.join(words[i:i+n]) for i in range(0,len(words) - n + 1)]  # all n-grams same length
    graphout = {p: {} for p in ngrams[0:-n] if p not in initgraph}    # add new ngrams (except ones at the end)
    graphout = {**graphout, **initgraph}        # combine the two
    for i in range(0, len(ngrams) - n):
        # if next n-gram has already been seen, get the TransitionStats obj so you can update it
        # if the key isn't found, create a new TransitionStats obj
        t = graphout[ngrams[i]].get(ngrams[i+n], TransitionStats())
        t.incrementCount()
        graphout[ngrams[i]][ngrams[i+n]] = t  # update the graphout with the updated stats
    # set probabilities based on the counts for each leading n-gram
    totalTransitions = {k: _getTotalTransitions(graphout, k) for k in graphout}
    for lp in graphout:
        for ts in graphout[lp].values():
            ts.updProb(totalTransitions[lp])
    return graphout

def _getCapped(words):
    return {w for w in words if w == w.capitalize() or w == w.upper()}

def _getCappedWithoutBeginningSentence(words):
    return {words[i] for i in range(0, len(words))
            if (words[i] == words[i].capitalize() or words[i] == words[i].upper())   # first letter or entire word capped
            and i != 0 and words[i-1][-1] not in sentenceEndingPunc}    # not first word and does not begin sentence

def _getNoPunc(words):
    return {w.translate(strippunctrans) for w in words}


def _getTotalTransitions(graph, ngram):
    return sum([ts.count for ts in graph[ngram].values()])

# def _getAlwaysCapitalized(words):
#     """ Gets elements in words that are capitalized at least once without following a sentence-ending punctuation mark
#     and that never appear uncapitalized
#
#     :param words:   A list of words
#     :return:        Those elements of words that should always be capitalized
#     """
#     lowerwords = {w.lower() for w in words}
#     sanspuncwords = {w.translate(strippunctrans) for w in words}
#     # get list of words that never appear without being followed by a period, ignoring capitalization
#     alwayshasperiod = {w for w in words if w.endswith('.') and w.lower().translate(strippunctrans) not in lowerwords}
#     # get list of words that never appear without being capitalized, ignoring punctuation
#     alwayscapped = {w for w in words if w == w.capitalize() and w.translate(strippunctrans).lower() not in sanspuncwords}
#     caps = {w.translate(strippunctrans) for w in words if w == w.capitalize()}
#     caps = {c for c in caps if c.lower not in words}    # never appears uncapitalized
#     pass





sentenceEndingPunc = ['.', '!', '?']
punc = string.punctuation + '\u2018' + '\u2019' + '\u201c' + '\u201d'   # add smart quotes
# TODO: remove apostrophe from punc?
strippunctrans = str.maketrans({key: None for key in punc})
keepperiodtrans = str.maketrans({key: None for key in punc if key != '.'})

class TransitionStats:
    count = 0
    prob = 0.0
    def __init__(self, count=0):
        self.count = count
    def incrementCount(self, c=1):
        self.count += c
    def updProb(self, leadingPhraseCount):
        self.prob = self.count / leadingPhraseCount
    def __repr__(self):
        return 'count: {0.count}, prob: {0.prob}'.format(self)







