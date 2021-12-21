import numpy as np
import json
import pickle

with open ('patent_signatures.json', 'r') as fin:
    sigs = json.load(fin)

embedArr = []
paperArr = []
file1 = open('specter.json')
Lines = file1.readlines()
for line in Lines:
    train = json.loads(line)
    sigID = train.get('paper_id')
    sig = sigs.get(sigID)
    paperID = sig.get("paper_id")
    embed = train.get("embedding")
    embedArr.append(embed)
    paperArr.append(paperID)
file1.close()

with open('patent_specter.pickle', 'wb') as fin:
    pickle.dump((np.array(embedArr), np.array(paperArr)), fin)