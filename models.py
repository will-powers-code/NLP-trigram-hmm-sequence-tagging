import numpy as np
from lib.seqTagModel import SeqTagModel
import sys

class BaselineModel(SeqTagModel):

    def predictSentenceLabels(self, s):
        return [self.predTag(s,i) for i in range(len(s))]

    def predTag(self, seq, i):
            probs = [self.emProb((seq[i],),label) for label in self.labelKeys]
            #print(probs,self.labelKeys[np.argmax(probs)][0])
            return self.labelKeys[np.argmax(probs)][0]

class TrigamHMM(SeqTagModel):
    
    def predictSentenceLabels(self, seq):
        return self.viterbi(seq)

    def viterbi(self, sentence):
        if not sentence: return []
        nGramLen = self.n
        e = self.emProb
        q = self.trProb
        n = len(sentence)
        labels = [key[0] for key in self.labelKeys]
        SeqVars = self.getSeqVariations(labels, n)
        pi = dict({(0,)+("*",)*(nGramLen-1):1})
        
        bp = dict()
        x = sentence

        s = dict()
        for i in range(2-nGramLen,n+1): s[i] = labels if i > 0 else ["*"]
        STOP = ("STOP",)
        
        
        # # For each word
        for k in range(1,n+1):
            # For every label v at w[i] and the n-2 labels before it
            for seqV in SeqVars[k]:
                mapIndex = (k,*seqV)
                prevTags = seqV[:-1]
                latestTag = (seqV[-1],)
                word = (x[k-1],)
                
                #Find the probabilities of all sequences ending in the sequence variation
                probs = []
                for w in s[k-nGramLen+1]:
                    wPreviousTags = (w,*prevTags,)
                    prevMapIndex = (k-1,)+wPreviousTags
                    probs.append(pi[prevMapIndex]*q(latestTag,wPreviousTags)*e(word,latestTag[0]))
                pi[mapIndex] = max(probs)
                bp[mapIndex] = s[k-nGramLen+1][np.argmax(probs)]


        probs = [pi[(n,*seqV)]*q(STOP,(*seqV,)) for seqV in SeqVars[n]]
        endTags = SeqVars[n][np.argmax(probs)]
        tagSeq = [None]*(n-nGramLen+1) + endTags
        
        for k in range(n-nGramLen+1, 0,-1):
            tagSeq[k-1] = bp[(k+nGramLen-1,*tagSeq[k:k+nGramLen-1])]
        return tagSeq[-n:]

    def getSeqVariations(self,labels,seqLen):
        n = self.n
        variations = [[]]
        varStars = dict()
        for i in range(1, n):
            variationsTemp = []
            for var in variations:
                for u in labels:
                    variationsTemp.append(var+[u])
            variations = variationsTemp
            if self.n-1-i > 0:
                varStars[i] = [ ["*"]*(n-1-i)+var for var in variationsTemp]

        sP = dict(varStars)
        for i in range(n-1,seqLen+1): sP[i]=variations
        return sP



ModelClass = TrigamHMM if len(sys.argv) < 2 else (BaselineModel if sys.argv[1] == "base" else TrigamHMM)
evalSet = "dev" if len(sys.argv) < 3 else sys.argv[2]
rareCount = 2 if len(sys.argv) < 4 else int(sys.argv[3])
wordMap = 2 if len(sys.argv) < 5 else int(sys.argv[4])
probType = "KBO" if len(sys.argv) < 6 else sys.argv[5]
lenGram = 7 if len(sys.argv) < 7 else int(sys.argv[6])
discount = .8 if len(sys.argv) < 8 else float(sys.argv[7])
print(len(sys.argv)>1 and sys.argv[1] or "tri", evalSet,rareCount,wordMap,probType,lenGram,discount)
model = ModelClass(evalSet,rareCount,wordMap,probType,lenGram,discount)
model.trainAndTest()