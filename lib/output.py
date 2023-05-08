def outPutLabels(words, labels , file):
    text = ""
    for i in range(len(words)):
        if words[i] != "":
            text+= f"{words[i]} {labels[i]}\n"
        else:
            text+="\n"
    f = open(file, "w")
    f.write(text)
    f.close()

def outPutLabelsDev(words,labels) : 
    outPutLabels( words, labels , "lib/gene_dev.p1.out")

def outPutLabelsTrain(words,labels): 
    outPutLabels(words, labels , "lib/gene_train.p1.out")

def output(typ):
    return typ=="dev" and outPutLabelsDev or outPutLabelsTrain

def joinSentences(corpus):
    sequence = []
    for sentence in corpus:
        for word in sentence:
            sequence.append(word)
        sequence.append("")
    return sequence
