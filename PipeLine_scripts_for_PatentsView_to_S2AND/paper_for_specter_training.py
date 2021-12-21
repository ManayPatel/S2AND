import json
from tqdm import tqdm
#For creating specter embeddings
print('Reading from signatures...')
with open('patent_signatures.json') as fin0:
    sigs = json.load(fin0)
print('Reading from signatures completed.')

print('Reading from papers...')
with open('patent_papers.json') as fin1:
    papers = json.load(fin1)
print('Reading from papers completed.')

print()
print('Processing data...')
data = {}
pbar = tqdm(total = len(sigs.keys()))
for sigID, sig in sigs.items():
    paperID = str(sig.get("paper_id"))
    paper = papers.get(paperID)
    paper_obj = {}
    paper_obj['title'] = paper.get('title')
    paper_obj['abstract'] = paper.get('abstract')
    data[sigID] = paper_obj
    pbar.update(1)
print('Processing data completed.')

print()
print('Writing to train_paper.json...')
with open("train_paper.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
print('Writing to train_paper.json completed.')