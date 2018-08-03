# math381final
text prediction using markov chains

example call to create graph:

```python
import trainer
words = trainer.parseFile('input/AliceInWonderland.txt')
graph = trainer.getGraph(words,2)
# take a look at the graph
len(words)
len(graph)   # uncomfortably close to the length of words
key=list(graph.keys())[25]
key
graph[key]  # look at a transition
max([graph[t] for t in graph])
sum([graph[t] for t in graph])  # should sum to 1
````