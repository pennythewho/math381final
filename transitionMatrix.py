import numpy

# words = trainer.parseFile('test.txt')
# graph = trainer.getGraph(words,n)

# needs a lot of memory, fair warning!
def transitionMatrix(graph):
    msize = len(graph); # matrix size, number of unique entries
    t_mat = numpy.zeros((msize,msize)); # transistion matrix
    keys = list(graph.keys()); # list of unique keys
    for i in range(msize): # note i is the row position
        words = list(graph[keys[i]]); # list of possible words following current word
        for j in range(len(words)): # iterate through above words
            clm_pos = keys.index(words[j]); # find position of this word
            t_mat[i,clm_pos] = graph[keys[i]][words[j]].prob; # set the probability
    return numpy.transpose(numpy.matrix(t_mat)); # format it

# usage example below

#t_mat = transitionMatrix.transitionMatrix(graph);
## create a starting vector
#from random import randint
#startvector = numpy.zeros((len(graph),1));
#word = randint(0, len(graph)-1);
#word_str = list(graph.keys())[word];
#startvector[word] = 1;
#startvector = numpy.matrix(startvector);
#
##%%
## markov stuff
#
#next_itr = t_mat*startvector
#next_next_itr = t_mat*next_itr 
#
## it works but i expect it to be unvbelievably slow for large matrices
## so lets not even try to implement it, but it is now there

