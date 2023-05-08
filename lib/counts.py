#Reads Texts & Tokenizes Sentances as Documents by Counts 
from collections import defaultdict as dd


def countDicts(wMP=dd(int)):
    with open("lib/gene.counts") as f:
        
        class cnts():
            emns,trns,wrds,tags,wrdKys = dict(),dict(),dict(),dict(),dict()
        em,tr,ws,ta,wK = cnts.emns,cnts.trns,cnts.wrds,cnts.tags,cnts.wrdKys
        for line in f:
            cnt, typ, *g = line.split(); cnt = int(cnt)

            if typ == "WORDTAG":
                t, w = g; w = wMP and wMP[w] or w
                em[(t,w)] = cnt + (em[(t,w)] if (t,w) in em else 0)
                ta[t] = cnt + (ta[t] if t in ta else 0)
                ws[w] = cnt + (ws[w] if w in ws else 0)
                wK[(w,)] = cnt + (wK[(w,)] if (w,) in wK else 0)
            else: tr[(*g,)] = cnt
    
    return cnts

# def countDicts(wMP = dd(int)):
#     with open("lib/gene.counts") as f:

#         class cnts():
#             emns,trns,wrds,tags,wrdKys = dict(),dict(),dict(),dict(),dict()
#         em,tr,ws,ta,wK = cnts.emns,cnts.trns,cnts.wrds,cnts.tags,cnts.wrdKys

#         for line in f:
#             cnt, typ, *g = line.split(); cnt = int(cnt)
#             if typ == "WORDTAG":
#                 t, w = g; w = wMP[w] or w

#                 em[(t, w)] = cnt + (em[(t, w)] if (t, w) in em else 0)
#                 ws[w] = cnt + (ws[w] if w in ws else 0)
#             else:
#                 ngram = tuple(g)
#                 tr[ngram] = cnt
#     return cnts 