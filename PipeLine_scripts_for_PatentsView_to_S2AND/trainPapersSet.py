import csv
import json
from tqdm import tqdm

train_canopies = {}

print("Reading map_to_new_patentid.json...")
with open('map_to_new_patentid.json') as fin1:
    uuid_map = json.load(fin1)
print("Reading completed.")
print("")

print("Reading key_list.json...")
with open('key_list.json') as fin1:
    key_list = json.load(fin1)
print("Reading completed.")
print("")

#**** CHANGE HERE ****
skipped_counter = 0
for file in ('eval_common_characteristics.train', 'eval_mixture.train'): #*** add or remove any files needed under the train_folder/ ***
    print(f"Reading file: {file}")
    # canopies:
    #   fl:v_ln:zimmer  148
    train_file = open(f"train_folder/{file}")
    line = train_file.readline()
    while line:
        row = line.split()
        id = str(row[0].split('-')[0])
        if uuid_map.get(id, None) != None:
            uuid = str(uuid_map.get(id))
            if key_list.get(uuid, False) != False:
                train_canopies[uuid] = True
            else:
                skipped_counter += 1
        else:
            skipped_counter += 1
        line = train_file.readline()
    train_file.close()
    print("Reading file completed.")
    print("")

print(skipped_counter)

print("Writing to train_canopies.json...")
with open("train_canopies.json", 'w') as fd:
    json.dump(train_canopies, fd, indent=4)
print("Writing Completed.")