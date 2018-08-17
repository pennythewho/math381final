from os import listdir

from tkinter import *
from tkinter import ttk

import trainer, textGenerator as tg

pathToInput = './input'
fileExt = '.txt'


def _getInputFiles():
    lfe = len(fileExt)
    return sorted([f[:-lfe] for f in  listdir(pathToInput) if f.endswith(fileExt)])

def generate(*args):
    try:
        files = [inputs[i] for i in inputlist.curselection()]
        n = int(nvar.get())
        l = int(lenvar.get())
        includeIncomplete = incomp.get() == '1'
        graph = {}
        for f in files:
            graph = trainer.getGraph(trainer.parseFile(pathToInput+'/'+f+fileExt), n, graph)
        gentxt = tg.generateText(graph, l, includeIncompleteSentences=includeIncomplete)
        txtsrc.set('Generated from '+', '.join(files))
        txtouttxt['state'] = 'normal'
        txtouttxt.replace(1.0,END,gentxt)
        txtouttxt['state'] = 'disabled'
    except:
        pass




root = Tk()
root.title('Text Generator')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

mainframe = ttk.Frame(root, padding=5)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

inputs = _getInputFiles()
inputvar = StringVar(value=inputs)
inputlist = Listbox(mainframe, listvariable=inputvar, selectmode='multiple')
inputlist.grid(column=1, row=1, rowspan=3, sticky=(N, W, E))

nvar = StringVar()
nentry = Entry(mainframe, width=4, textvariable=nvar)
nentry.grid(column=2, row=1, sticky=(N,E))
Label(mainframe, text='n-gram size').grid(column=2,row=1,sticky=(N,W))

lenvar = StringVar()
lenentry = Entry(mainframe, width=4, textvariable=lenvar)
lenentry.grid(column=2, row=2, sticky=(N,E))
Label(mainframe, text='target length').grid(column=2,row=2,sticky=(N,W))

incomp = StringVar()
incompcb = Checkbutton(mainframe, text='allow incomplete sentences', variable=incomp)
incompcb.grid(column=2, row=3, sticky = (S,W,E))

genbutton = Button(mainframe, text='generate', command=generate)
genbutton.grid(column=3,row=3,sticky=(N,W,E))

txtsrc = StringVar()
Label(mainframe, textvariable=txtsrc).grid(column=1, row=4, columnspan=3, sticky=(N,W))
txtouttxt = Text(mainframe, width = 55, wrap='word', state='disabled')
txtouttxt.grid(column=1, row=5, columnspan=3, sticky=(S,W))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# default to generating 25 words from n=3 Alice in Wonderland
inputlist.selection_set(1,1)
incompcb.deselect()
nentry.insert(0,'3')
lenentry.insert(0,'25')

root.mainloop()



