# math381final
text prediction using markov chains
tested in Python 3.7
requires Python 3.5 or higher

example call to create graph:

```python
import trainer, textGenerator
pp = trainer.parseFile('input/PrideAndPrejudice.txt')
p = trainer.parseFile('input/Persuasion.txt')
e = trainer.parseFile('input/Emma.txt')
ss = trainer.parseFile('input/SenseAndSensibility.txt')
mp = trainer.parseFile('input/MansfieldPark.txt')
na = trainer.parseFile('input/NorthangerAbbey.txt')
austen2 = trainer.getGraph(pp,2)
austen2 = trainer.getGraph(p,2,austen2)
austen2 = trainer.getGraph(e,2,austen2)
austen2 = trainer.getGraph(ss,2,austen2)
austen2 = trainer.getGraph(mp,2,austen2)
austen2 = trainer.getGraph(na,2,austen2)
textGenerator.generateText(austen2,30)
````