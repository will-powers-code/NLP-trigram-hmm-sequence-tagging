from collections import defaultdict
from lib.input import getFirstWordsTrain

class RareWords:

    def __init__(self, rareCnt, train):
        firstWords = getFirstWordsTrain()
        self.rCnt = rareCnt
        wrdMp1 = [
            [other, "_RARE_"]
        ]
        self.n = 4

        wrdMp2 = [
            [isNumLength2, "_twoDigitNum_"],
            [isNumLength4, "_fourDigitNum_"],
            [containsDigitAndAlpha, "_containsDigitAndAlpha_"],
            [containsDigitAndDash, "_containsDigitAndDash_"],
            [containsDigitAndSlash, "_containsDigitAndSlash_"],
            [containsDigitAndPeriod, "_containsDigitAndPeriod_"],
            [containsDigitAndComma, "_containsDigitAndComma_"],
            [isNum, "_othernum_"],
            [isAllCaps,"_allCaps_"],
            [isCapThenPeriod, "_capPeriod_"],
            [isFirstWord(firstWords), "_firstWord_"],
            [isWordGreaterThanN(4),"_longWord_"],
            [capitalizedWord, "_initCap_"],
            [islowerCaseWord, "_lowercase_"],
            [other, "_other_"]
        ]

        self.wrdMp = {
            1: wrdMp1,
            2: wrdMp2
        }[train]


    def mpSeqTst(self, corpus, freqs):
        return [[self.mpTst(w, freqs) for w in s] for s in corpus]  

    def getMpTrn(self,wrds):
        return dict([(w, self.mpTrn(w,n)) for w,n in wrds.items()])

    def mpTst(self, w, fq):
        return w in fq and w or self.mp(w)

    def mpTrn(self,w,cnt):
        return cnt >= self.rCnt and w or self.mp(w)

    def mp(self,w):
        return next(l for c,l in self.wrdMp if c(w))
              


def isNum(w):
    return w.isnumeric() 
    
def isNumLength(w, length):
    return isNum(w) and len(w) == length

def isNumLength2(w):
    return isNumLength(w,2)

def isNumLength4(w):
    return isNumLength(w,4)

def isAlpha(c):
    return c.isalpha()

def isDash(c):
    return c == "-"

def isSlash(c):
    return c == "/"

def isPeriod(c):
    return c == "."

def isComma(c):
    return c == ","

def contains(w, conditions):
    return all(any(condition(c) for c in w) for condition in conditions)

def containsDigitAndAlpha(w):
    return contains(w, [isNum, isAlpha])

def containsDigitAndDash(w):
    return contains(w, [isNum, isDash])

def containsDigitAndSlash(w):
    return contains(w, [isNum, isSlash])

def containsDigitAndPeriod(w):
    return contains(w, [isNum, isPeriod])

def containsDigitAndComma(w):
    return contains(w, [isNum, isComma])

def isAllCaps(w):
    return w.isalpha() and w.upper() == w

def isCapThenPeriod(w):
    return len(w)>=2 and isAllCaps(w[0]) and isPeriod(w[1])

def isWordGreaterThanN(n):
    def detect(w):
        return isAlpha(w) and len(w) > n
    return detect

def wordComplexityGreaterThan(n):
    def detect(w):
        return isAlpha(w) and len(set(w)) > n
    return detect

def isFirstWord(firstWords):
        def detect(w):
            return w in firstWords
        return detect

def capitalizedWord(w):
    return isAlpha(w) and isAllCaps(w[0])

def islowerCaseWord(w):
    return isAlpha(w) and w.lower() == w

def other(w):
    return True

def isRareChar(c):
    return ["Z","Q","J","X"].count(c) > 0

def containRareChar(w):
    return contains(w,[isRareChar])

def rareCharAndLong(w):
    return containRareChar(w) and isWordGreaterThanN(4)(w)