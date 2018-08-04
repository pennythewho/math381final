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


def getGraph(words, n):
    #  TODO: handle looping at end of words (see itertools.cycle)
    phrases = [' '.join(words[i:i+n]) for i in range(0,len(words) - n + 1)]
    # graphout is a dict of dicts, with keys in the outer dict representing distinct phrases
    # the inner dict keys are the phrases that follow the key in the outer dict
    # the value of the inner dict is a TransitionStats object, which has count and prob properties
    graphout = {p:{} for p in phrases}  # start the dict with just keys
    for i in range(0,len(phrases) - n):     # so far, no looping so ignore phrases at end
        # if next phrase is a repeat, get the TransitionStats obj so you can update it
        # if the key isn't found, create a new TransitionStats obj
        t = graphout[phrases[i]].get(phrases[i+n], TransitionStats())
        t.incrementCount()
        graphout[phrases[i]][phrases[i+n]] = t  # update the graphout with the updated stats
    sumtrans = lambda p: sum([ts.count for ts in graphout[p].values()])
    # TODO: remove items from graphout that have no following phrases?  s/b unnecessary if we add looping
    # set probabilities based on the counts for each leading phrase
    for lp in graphout:
        for ts in graphout[lp].values():
            ts.updProb(sumtrans(lp))
    return graphout



punctranslator = str.maketrans({key: None for key in string.punctuation})

class TransitionStats:
    count = 0
    prob = 0.0
    def __init__(self, count=0):
        self.count = count
    def incrementCount(self):
        self.count +=1
    def updProb(self, leadingPhraseCount):
        self.prob = self.count / leadingPhraseCount
    def __repr__(self):
        return 'count: {0.count}, prob: {0.prob}'.format(self)







