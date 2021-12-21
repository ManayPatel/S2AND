import csv
import json
from tqdm import tqdm

print("Reading canopies file...")
with open("train_canopies.json") as fd:
    canopies = json.load(fd)
print("Reading canopies file completed.")
print("")

print("Reading Test Canopies files...")
with open("test_canopies.json") as fd:
    canopies.update(json.load(fd))
print("Reading canopies file completed.")
print("")

print("Reading new uuid map...")
with open("map_to_new_patentid.json") as fd:
    uuid_map = json.load(fd)
print("Reaading completed.")
print("")


print("Reading from key_list.json...")
with open("key_list.json") as fd:
    key_list = json.load(fd)
print("Reading completed.")
print("")

paper_to_name = {}
print("Creating paper to name map...")
#rawinventor.tsv:
#"uuid" "patent_id" "inventor_id" "rawlocation_id" "name_first" "name_last" "sequence" "rule_47" "deceased"
inventor_file = open("rawinventor.tsv")
inventors = csv.reader(inventor_file, delimiter='\t')
next(inventors)
for row in tqdm(inventors, desc="Converting inventors", total=18562496):
    paper = str(uuid_map.get(row[1]))
    if canopies.get(paper, False) and key_list.get(paper, False):
        seq = int(row[6])
        nameBlock = {}
        nameBlock['name_first'] = row[4]
        nameBlock['name_last'] = row[5]
        seq_obj = paper_to_name.get(uuid_map.get(row[1]), {})
        seq_obj[seq] = nameBlock
        paper_to_name[uuid_map.get(row[1])] = seq_obj
print("Map created.")
print("")

#**** CHANGE HERE *******
skipped_counter = 0
accepted_counter = 0
print("Reading train file...")
canopies_file = open("test_folder/eval_als_common.txt") #****Change this directory to the one needed****
#File format:
#7689817-0       62482410
#7953916-1       62482410
sig_map = {}
cluster_map = {}
auth_to_clus = {}
sig_counter = 0
cluster_counter = 1
line = canopies_file.readline()
pbar = tqdm(total = 30336)
while line:
    row = line.split()
    cluster = row[1]
    paper = row[0].split('-')[0]
    seq = int(row[0].split('-')[1])
    if canopies.get(str(uuid_map.get(paper)), False) and key_list.get(str(uuid_map.get(paper)), False):
        accepted_counter += 1
        #****SIG_MAP****
        signature = {"author_id" : cluster}
        signature["paper_id"] = int(uuid_map.get(paper))
        signature["signature_id"] = sig_counter

        nameBlock = paper_to_name.get(uuid_map.get(paper)).get(seq)
        if nameBlock == None:
            line = canopies_file.readline()
            pbar.update(1)
            continue
        first = nameBlock['name_first']
        block = first[0].lower() + ' ' + nameBlock['name_last'].lower()
        author_obj = {"given_block" : block}
        author_obj["block"] = block
        author_obj['position'] = seq
        author_obj['first'] = first.split()[0]
        if len(first.split()) > 1:
            author_obj['middle'] = first.split()[1]
        else:
            author_obj['middle'] = None
        author_obj['last'] = nameBlock['name_last']
        author_obj['suffix'] = None
        author_obj['affiliations'] = []
        author_obj['email'] = None

        signature['author_info'] = author_obj
        sig_map[int(sig_counter)] = signature

        #****CLUSTER_MAP*****\
        if auth_to_clus.get(cluster) == None:
            clusterID = "PV_" + str(cluster_counter)
            auth_to_clus[cluster] = clusterID
            cluster_counter += 1
            cluster_obj = {}
            cluster_obj['cluster_id'] = clusterID
            cluster_obj['signature_ids'] = []
            cluster_obj['model_version'] = -1
            cluster_map[clusterID] = cluster_obj
        
        cluster_obj = cluster_map.get(auth_to_clus.get(cluster))
        sigs = cluster_obj.get('signature_ids')
        sigs.append(str(sig_counter))
        cluster_obj['signature_ids'] = sigs
        cluster_map[auth_to_clus.get(cluster)] = cluster_obj
        sig_counter += 1
    else:
        skipped_counter += 1
    line = canopies_file.readline()
    pbar.update(1)
canopies_file.close()
print("Reading train file completed.")
print("")

print(f"Total number of accepted lines/skipped lines: {accepted_counter}/{skipped_counter}")
print(f"Number of signatures: {len(sig_map)}")
print(f"Number of clusters: {len(cluster_map)}")

print("Writing out clusters file...")
with open("patent_clusters.json", "w") as outfile:
    json.dump(cluster_map, outfile, indent=4)
print("Writing out clusters file completed.")
print("")

print("Writing out signatures file...")
with open("patent_signatures.json", "w") as outfile:
    json.dump(sig_map, outfile, indent=4)
print("Writing out signatures file completed.")
print("")