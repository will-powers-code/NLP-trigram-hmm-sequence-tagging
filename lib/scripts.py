import subprocess

def count_freqs(n):
    subprocess.run(f"python lib/count_freqs.py {n} lib/gene.train > lib/gene.counts",shell=True)

def eval_model_dev(testFile="gene.key",modelOutput="gene_dev.p1.out"):
    subprocess.run(f"python lib/eval_gene_tagger.py lib/{testFile} lib/{modelOutput}",shell=True)

def eval_model_train(testFile="gene.train",modelOutput="gene_train.p1.out"):
    subprocess.run(f"python lib/eval_gene_tagger.py lib/{testFile} lib/{modelOutput}",shell=True)




#import
def evalMod(typ):
    return typ=="dev" and eval_model_dev or eval_model_train