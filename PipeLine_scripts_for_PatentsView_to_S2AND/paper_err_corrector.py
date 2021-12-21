import json
from tqdm import tqdm
#692022 / 2028748
print("Reading err_papers...")
with open('err_patent_papers.json') as fin:
    data = json.load(fin)
print("Reading Completed.")
total = len(data.keys())

new_data = {}
key_list = {}
err_cnt = 0
pbar = tqdm(total = total)
for k in data.keys():
    paper = data.get(k)
    if len(paper.keys()) != 8:
        if paper.get("paper_id") == None:
            err_cnt += 1
            continue
        if paper.get("title") == None:
            err_cnt += 1
            continue
        if paper.get("authors") == None:
            err_cnt += 1
            continue
        if paper.get("year") == None:
            err_cnt += 1
            continue
        if paper.get("abstract") == None:
            paper["abstract"] = None
        
        if paper.get("journal_name") == None:
            paper["journal_name"] = None
        
        if paper.get("references") == None:
            paper["references"] = []

        if paper.get("venue") == None:
            paper["venue"] = None
        
        new_data[k] = paper
        key_list[k] = True
    else:
        new_data[k] = paper
        key_list[k] = True
    pbar.update(1)

print("{} / {}".format(err_cnt,total))
print(len(new_data.keys()))

print("Writing to patent_papers.json...")
with open("patent_papers.json", "w") as outfile:
    json.dump(new_data, outfile, indent=4)
print("Writing to patent_papers.json completed.")

print("Writing to key_list.json...")
with open("key_list.json", "w") as outfile:
    json.dump(key_list, outfile, indent=4)
print("Writing to key_list.json completed.")
