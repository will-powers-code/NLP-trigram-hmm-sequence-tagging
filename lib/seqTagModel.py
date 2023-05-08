from collections import defaultdict as dd
from lib.counts import countDicts
from lib.KBO import KBO
from lib.input import getSeq
from lib.output import output,joinSentences
from lib.scripts import count_freqs
from lib.input import splitSentences
from lib.wordMapping import RareWords
from lib.scripts import evalMod

class SeqTagModel:
 
    def createCounts(self, rCnt, mpTyp):
        #Get Counts
        count_freqs(self.n); 
        wrds = countDicts().wrds
        #Get RareWord Counts
        self.RW = RW = RareWords(rCnt, mpTyp)
        wrdMap = RW.getMpTrn(wrds)
        self.cnts = countDicts(wrdMap)

    def createLM(self, smoothing, dscnt):
        cnts = self.cnts
        emns, trns, wrdKys, tags = cnts.emns,cnts.trns,cnts.wrdKys,cnts.tags
        seqLen = sum(cnts.wrds.values())

        #Create Probabilities
        if smoothing=="KBO":
            self.emProb = KBO(2, dict({**emns,**wrdKys,**tags}), dscnt, seqLen,True).prob
            self.trProb = KBO(self.n, trns, dscnt, seqLen).prob
        else:
            self.emProb = lambda w,t: emns[t+w]/trns[t] if t+w in emns else 0
            self.trProb = lambda t,p: trns[p+t]/trns[p] if p+t in trns else 0


    def __init__(self, corpus, rareCount, wordMap, smoothing, n, dscnt):
        #Info
        self.labelKeys = [("O",),("I-GENE",)]
        self.n = n

        # config dev/train
        self.evalMod = evalMod(corpus)
        self.getSeq = getSeq(corpus)
        self.output = output(corpus)
        
        #Initialize Counts
        self.createCounts(rareCount, wordMap)

        #Create LM
        self.createLM(smoothing,dscnt)


    def predictTags(self, seq):
        corpus = splitSentences(seq)
        newCorpus = self.RW.mpSeqTst(corpus, self.cnts.wrds)
        preds = [self.predictSentenceLabels(sentence) for sentence in newCorpus]
        return joinSentences(preds)

    #Methods to Create in Children
    def predictSentenceLabels(self, seq): pass

    def trainAndTest(self):
        seq = self.getSeq()
        predLabels = self.predictTags(seq)
        self.output(seq, predLabels)
        self.evalMod()