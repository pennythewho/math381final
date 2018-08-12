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


def getGraph(words, n, initgraph={}, includeTrailingNgrams=False):
    """ Returns a graph

    :param words:       the source document parsed into words
    :param n:           the length of n-grams
    :param initgraph:   another graph to which the n-grams in words should be added
    :param includeTrailingNgrams:  True to include n-grams at the end of the source that have no following n-grams
                        Should only be used to generate a full Markov transition matrix
                        text generation may fail if given a graph (especially a small one) with this set to true
    :return:            a dict of dicts, with keys in the outer dict representing distinct n-grams
                        the inner dict keys are the n-grams that follow the key in the outer dict
                        the value of the inner dict is a TransitionStats object, which has count and prob properties
    """
    if initgraph and n != len(list(initgraph.keys())[0].split()):
        raise ValueError('You can only add n-grams of the same size to an existing graph.')

    ngrams = [' '.join(words[i:i+n]) for i in range(0, len(words) - n + 1)]  # all n-grams same length
    leadingngrams = ngrams[0:-n] if not includeTrailingNgrams else ngrams
    graphout = {p: {} for p in leadingngrams if p not in initgraph}    # add new ngrams (except ones at the end)
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


sentenceEndingPunc = ['.', '!', '?']
punc = string.punctuation + '\u2018' + '\u2019' + '\u201c' + '\u201d'   # add smart quotes
strippunctrans = str.maketrans({key: None for key in punc})

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







