import csv
import json
from tqdm import tqdm

test_canopies = {}

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
for file in ('eval_als_common.txt', 'eval_als.txt', 'eval_ens.txt', 'eval_is.txt'): #*** add or remove any files needed under the test_folder/ ***
    print(f"Reading file: {file}")
    # canopies:
    #   fl:v_ln:zimmer  148
    test_file = open(f"test_folder/{file}")
    line = test_file.readline()
    while line:
        row = line.split()
        id = str(row[0].split('-')[0])
        if uuid_map.get(id, None) != None:
            uuid = str(uuid_map.get(id))
            if key_list.get(uuid, False) != False:
                test_canopies[uuid] = True
            else:
                skipped_counter += 1
        else:
            skipped_counter += 1
        line = test_file.readline()
    test_file.close()
    print("Reading file completed.")
    print("")
print(skipped_counter)

print("Writing to test_canopies.json...")
with open("test_canopies.json", 'w') as fd:
    json.dump(test_canopies, fd, indent=4)
print("Writing Completed.")