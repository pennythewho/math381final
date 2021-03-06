import random, time
from itertools import accumulate

from trainer import sentenceEndingPunc

def generateText(srcGraph, targetLen=50, firstNgram=None, forceCap=False, includeIncompleteSentences=True):
    """
    :param targetLen:   the target number of words (NOT the target number of n-grams) in the generated text
                        this is just a target - we try to end the output near the end of a sentence so the output
                        might be longer than requested
    :param firstNgram:  allows user choosing the starting n-gram
                        if None or an n-gram that doesn't exist in srcGraph, one will be chosen at random
    :param forceCap:    if True, any word following a sentenceEndingPunc will be capitalized
    :param includeIncompleteSentences:  if False, will strip words preceding the first space after the
                        first sentence ending punctuation, and any words after the last sentence-ending punctuation
                        In this case, the targetLen becomes more of a guideline....it could be as small as targetLen-2n
                        or as long as approximately 2*targetLen.  If the generated text gets to that length without
                        finishing a sentence, it will stop anyway.
                        If True, the output will be of length ceil(targetLen/n)*n
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
    while not _isLongEnough(out, targetLen, includeIncompleteSentences) and srcGraph[lastNgram]:
        # get next phrases - needs to be sorted to match probabilities properly
        innerGraph = srcGraph[lastNgram]        # a dict of next keys and their TransitionStats
        nextPhrases = [p for p in innerGraph]   # just the keys
        npp = accumulate([innerGraph[p].prob for p in nextPhrases])
        i = 0 if len(innerGraph) == 1 else next(x[0] for x in enumerate(npp) if x[1] >= random.random())
        out.append(nextPhrases[i] if not forceCap else _cappedNgram(nextPhrases[i], lastNgram))
        lastNgram = nextPhrases[i]
        out = out if includeIncompleteSentences else out[_getFirstSentenceIdx(out):]
    return ' '.join(out) if includeIncompleteSentences else stripIncompleteSentences(' '.join(out))

def _cappedNgram(ngram, lastngram):
    # capitalize the first word if the lastngram exists and ended a sentence
    if lastngram and lastngram[-1] in sentenceEndingPunc:
        ngram = ngram.capitalize()
    words = ngram.split()
    # for all but the first word, capitalize if the previous word ended a sentence
    words = [words[0]] + [words[i].capitalize() if words[i-1][-1] in sentenceEndingPunc else words[i] for i in range(1, len(words))]
    return ' '.join(words)

def _isLongEnough(out, targetLen, allowIncompleteSentences):
    n = len(out[-1].split())    # length of n-grams
    wc = len(out[(0 if allowIncompleteSentences else _getFirstSentenceIdx(out)):]) * n
    # shoot for the target length in all cases, BUT
    # if allowIncompleteSentences is False, the last n-gram needs to contain the end of a sentence
    # to avoid infinite loops that might result if using a stripped punctuation graph, also stop generating text
    # if the size goes over maxLenFactor * targetLen
    return wc >= targetLen and (allowIncompleteSentences or wc > maxLenFactor*targetLen
                                      or any((c in sentenceEndingPunc) for c in out[-1]))

def _getFirstSentenceIdx(out):
    lo = len(out)
    return _findFirstInstance(out, sentenceEndingPunc, endIdx=lo)

def _findFirstInstance(text, searchChars, beginIdx=0, endIdx=None, searchBackwards=False):
    if endIdx == None:
        endIdx = len(text)
    inc = 1 if not searchBackwards else -1
    try:
        return next(i for i in range(beginIdx, endIdx, inc) for c in text[i] if c in searchChars)
    except StopIteration:
        return beginIdx


def stripIncompleteSentences(text):
    lt = len(text)
    first = _findFirstInstance(text, sentenceEndingPunc, endIdx=lt)
    first = _findFirstInstance(text, ' ', beginIdx=first, endIdx=lt) + 1
    last = _findFirstInstance(text, sentenceEndingPunc, beginIdx=-1, endIdx=(-1 * lt + first - 1), searchBackwards=True) + 1
    return text[first:None if last == 0 else last]


maxLenFactor = 10







