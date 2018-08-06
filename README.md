# math381final
text prediction using markov chains
tested in Python 3.7
requires Python 3.5 or higher

example call to create graph:

```python
import trainer, textGenerator
words = trainer.parseFile('input/AliceInWonderland.txt')
graph = trainer.getGraph(words,2)
# take a look at the graph
len(words)
len(graph)  
# look at a random key
key=list(graph.keys())[25]
graph[key]
# generate some text
textGenerator.generateText(graph)
````