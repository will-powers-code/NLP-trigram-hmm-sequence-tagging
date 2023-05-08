def getDevSequence():
    name = "lib/gene.dev"
    with open(name) as f:
        return [l.strip() for l in f]

def getTrainSequence():
    name = "lib/gene.train"
    seq = []
    with open(name) as f:
        for l in f:
            words = l.strip().split()
            if not words:
                seq.append("")
            else:
                seq.append(words[0])
    return seq

def getSeq(typ):
    return typ == "dev" and getDevSequence or getTrainSequence

def splitSentences(seq):
    i = 0
    si = 0
    corpus = [[]]
    while i < len(seq):
        if seq[i] == "":
            si += 1 
            corpus.append([])
        else:
            corpus[si].append(seq[i])
        i+=1
    return corpus


def getFirstWordsTrain():
    trainSequence = getTrainSequence()
    firstWords = set()
    for i in range(len(trainSequence)):
        if i == 0 or trainSequence[i-1] == "":
            firstWords.add(trainSequence[i])
    return firstWords


