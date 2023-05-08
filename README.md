# To view the data analysis report, see [here](https://github.com/williamcpowers8/trigram-hmm-sequence-tagging/blob/main/data-report.pdf) #

*The code must be run from the top directory for the subprocess modules to accurately call scripts.*

to run & evaluate the model with the most optimal parameters run one of the following commands:
    python models.py
    python models.py tri dev 2 2 KBO 7 .8


to run the base model run:
    python models.py base

The model can also take different parameters via the following command line arguments:
    python models.py `<m> <e> <f> <r> <s> <n> <d>`


`<m> is model type, "base"  for the base model, "tri" for HMM`

    - if running the bas model, specificy no other arguments

`<e> is the data set to evaluate the model on "dev" or "train`

`<f> is min frequency a word needs to not be tokenized as a rare words`

`<r> is the rare word classifier to use: 1 for uniclass, 2 for multiclass`

`<s> is the smoothing tecnique to use: "KBO" for katz backoff, "norm" for none`

`<n> is the length of the ngrams to use (n>1)`

`<d> is the discount factor to use in the smoothing technique`
