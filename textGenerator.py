import random, time
from itertools import accumulate

from trainer import sentenceEndingPunc

def generateText(srcGraph, targetLen=50, firstNgram=None, forceCap=False):
    """
    :param targetLen:   the target number of words (NOT the target number of n-grams) in the generated text
                        this is just a target - we try to end the output near the end of a sentence so the output
                        might be longer than requested
    :param firstNgram:  allows user choosing the starting n-gram
                        if None or an n-gram that doesn't exist in srcGraph, one will be chosen at random
    :param forceCap:    if True, any word following a sentenceEndingPunc will be capitalized
    :return:
    """
    out = []
    random.seed(time.time())
    if not firstNgram or firstNgram not in srcGraph:
        firstNgram = list(srcGraph.keys())[random.randrange(len(srcGraph))]
    out.append(firstNgram if not forceCap else firstNgram.capitalize())
    lastNgram = firstNgram
    # keep generating until the length exceeds the targetLen but also require finishing a sentence
    # also requires that the lastNgram has something following it
    while not _isLongEnough(out, targetLen) and srcGraph[lastNgram]:
        # get next phrases - needs to be sorted to match probabilities properly
        innerGraph = srcGraph[lastNgram]        # a dict of next keys and their TransitionStats
        nextPhrases = [p for p in innerGraph]   # just the keys
        npp = accumulate([innerGraph[p].prob for p in nextPhrases])
        i = 0 if len(innerGraph) == 1 else next(x[0] for x in enumerate(npp) if x[1] >= random.random())
        out.append(nextPhrases[i] if not forceCap else _cappedNgram(nextPhrases[i], lastNgram))
        lastNgram = nextPhrases[i]
    return ' '.join(out)

def _cappedNgram(ngram, lastngram):
    # capitalize the first word if the lastngram exists and ended a sentence
    if lastngram and lastngram[-1] in sentenceEndingPunc:
        ngram = ngram.capitalize()
    words = ngram.split()
    # for all but the first word, capitalize if the previous word ended a sentence
    words = [words[0]] + [words[i].capitalize() if words[i-1][-1] in sentenceEndingPunc else words[i] for i in range(1, len(words))]
    return ' '.join(words)

def _isLongEnough(out, targetLen):
    # want it to be the target length but also have the last n-gram contain the end of a sentence
    n = len(out[-1].split())    # length of n-grams
    return len(out) >= targetLen/n and any((c in sentenceEndingPunc) for c in out[-1])







