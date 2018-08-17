import trainer, textGenerator, numpy
words = trainer.parseFile('input/1liners.txt');
graph = trainer.getGraph(words,2)

#%%
#helper1 = list(graph.keys());
#helper2 = list(graph.values());
#helper3 = []
#for i in range(len(helper2)):
#    helper3.append(list(helper2[i].keys())[0])
#%%
import transitionMatrix
t_mat = transitionMatrix.transitionMatrix(graph)
#%%
import matplotlib
from matplotlib.pyplot import *
#%%
matplotlib.pyplot.imsave('1liners_2.png',t_mat,cmap=cm.get_cmap('afmhot'))

#%%
#import matplotlib.pyplot as plt
#plt.imshow(t_mat)
#%%
# generate some text
textGenerator.generateText(graph,45,includeIncompleteSentences=True, firstNgram='Master')

#%%
from random import shuffle
words2 = (list(words))
#%%
shuffle(words2)
#%%
graph2 = trainer.getGraph(words2,2)
#%%
t_mat2 = transitionMatrix.transitionMatrix(graph2)
#%%
matplotlib.pyplot.imsave('1liners_2_shuff.png',t_mat2,cmap=cm.get_cmap('afmhot'))
