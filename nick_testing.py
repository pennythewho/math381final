import trainer, textGenerator, numpy
graph = trainer.getGraph(trainer.parseFile('input/TheIliad.txt'),1)

#%%
#helper1 = list(graph.keys());
#helper2 = list(graph.values());
#helper3 = []
#for i in range(len(helper2)):
#    helper3.append(list(helper2[i].keys())[0])
#%%
#import transitionMatrix
#t_mat = transitionMatrix.transitionMatrix(graph)
#%%
#import matplotlib.pyplot as plt
#plt.imshow(t_mat)
#%%
# generate some text
textGenerator.generateText(graph,43,includeIncompleteSentences=False)