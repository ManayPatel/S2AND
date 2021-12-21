import csv
import json
from tqdm import tqdm

print("Reading test_canopies.json...")
with open('test_canopies.json') as fin1:
    test_canopies = json.load(fin1)
print("Reading completed.")
print("")

print("Reading train_canopies.json...")
with open('train_canopies.json') as fin1:
    train_canopies = json.load(fin1)
print("Reading completed.")
print("")

print("Reading papers...")
with open('patent_papers.json') as fin:
    data = json.load(fin)
print("Reading Completed.")
total = len(data.keys())

new_data = {}
key_list = {}
skipped_counter = 0
pbar = tqdm(total = total)
for k in data.keys():
    paper = data.get(k)
    if (test_canopies.get(k, False)) or (train_canopies.get(k, False)):
        new_data[k] = paper
    else:
        skipped_counter += 1
    pbar.update(1)
print(f"Skipped Counter {skipped_counter}\n")
print("Writing to new_patent_papers.json...")
with open("new_patent_papers.json", "w") as outfile:
    json.dump(new_data, outfile, indent=4)
print("Writing to new_patent_papers.json completed.")