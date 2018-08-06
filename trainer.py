import string

def parseFile(fname, stripPunc=False):
    """  Opens a file, optionally strips it of punctuation, and splits it into words

    :param fname:               the full or relative path to the file to be opened
    :param stripPunc:           True to remove all punctuation, leaving just characters to form words
                                False to keep punctuation
    :return:                    An ordered immutable iteratable where each element is a word in the file
    """

    with open(fname, mode='rt', buffering=1) as f:
        words = f.read().split()
    if stripPunc:
        words = [w.translate(punctranslator) for w in words]
    return tuple(words)


def getGraph(words, n, initgraph={}):
    #  TODO: handle looping at end of words (use itertools.cycle?)
    ngrams = [' '.join(words[i:i+n]) for i in range(0,len(words) - n + 1)]
    # graphout is a dict of dicts, with keys in the outer dict representing distinct n-grams
    # the inner dict keys are the n-grams that follow the key in the outer dict
    # the value of the inner dict is a TransitionStats object, which has count and prob properties
    graphout = {p:{} for p in ngrams if p not in initgraph}  # start the dict with just keys not already in initgraph
    graphout = {**graphout, **initgraph}    # now combine the two
    for i in range(0,len(ngrams) - n):     # so far, no looping so ignore n-grams at end
        # if next n-gram has already been seen, get the TransitionStats obj so you can update it
        # if the key isn't found, create a new TransitionStats obj
        t = graphout[ngrams[i]].get(ngrams[i+n], TransitionStats())
        t.incrementCount()
        graphout[ngrams[i]][ngrams[i+n]] = t  # update the graphout with the updated stats
    # TODO: remove items from graphout that have no following ngrams?  s/b unnecessary if we add looping
    # set probabilities based on the counts for each leading n-gram
    for lp in graphout:
        for ts in graphout[lp].values():
            ts.updProb(_getTotalTransitions(graphout, lp))
    return graphout


def _getTotalTransitions(graph, ngram):
    return sum([ts.count for ts in graph[ngram].values()])




punctranslator = str.maketrans({key: None for key in string.punctuation})

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







