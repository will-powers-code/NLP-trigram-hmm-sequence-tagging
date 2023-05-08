#!/bin/python

from collections import defaultdict


class KBO():

    def __init__(self, n, countDict,discount,totalWords,emisns=False):
        self.countDict = countDict
        self.discount = discount
        self.n = n
        self.totalWords = totalWords
        self.emisns = emisns
        self.memoizeKeys()
        


    def prob(self, wordKey, prevKey):
        fullGram = self.emisns and (prevKey,)+wordKey or prevKey+wordKey
        prevKeyLen = self.emisns and 1 or len(prevKey)
        knownKBO = self.KnownKBO[fullGram]
        if knownKBO: return knownKBO
        else:
            mpm = self.MPMs[prevKey]
            denominator = self.unKnowKBOdenominator[prevKey]
            if prevKeyLen == 1:
                return self.ML1s[wordKey]*mpm/denominator
            else:
                return self.prob(wordKey,prevKey[1:])*mpm/denominator

    def memoizeKeys(self):
        self.MPMs = MPMs = defaultdict(lambda:1)
        self.KnownKBO = KnownKBO = defaultdict(lambda:None)
        self.ML1s = ML1s = defaultdict(int)
        self.unKnowKBOdenominator = unKnowKBOdenominator = defaultdict(lambda:1)
        countDict = self.countDict
        discount = self.discount

        vocabN = defaultdict(lambda:[])
        for fullGram in countDict:
            vocabN[len(fullGram)].append(fullGram)

        for n in range(1,self.n+1):
            for fullGram in vocabN[n]:
                if len(fullGram) == 1:
                    ML1s[fullGram] = countDict[fullGram]/self.totalWords
                if len(fullGram)>1:
                    prevKey = self.emisns and fullGram[0] or fullGram[:-1]
                    prevKeyLen = self.emisns and 1 or len(prevKey)
                    wordKey = fullGram[-1:]
                    dml = (countDict[fullGram]- discount)/(countDict[prevKey])
                    MPMs[prevKey] -= dml
                    KnownKBO[fullGram] = dml
                    unKnowKBOdenominator[prevKey] -= ML1s[wordKey] if prevKeyLen == 1 else KnownKBO[prevKey[1:]+wordKey]

                

                

        
        
        

