import string
from itertools import groupby

def parseFile(fname, stripPunc=True):
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
    transitions = [(phrases[i], phrases[i + n]) for i in range(0, len(phrases) - n)]
    transitions.sort()
    transitionCounts = {t: len(list(g)) for t,g in groupby(transitions)}
    totalTransitions = len(transitions)
    return {t: transitionCounts[t]*1.0/totalTransitions for t in transitionCounts}








punctranslator = str.maketrans({key: None for key in string.punctuation})




