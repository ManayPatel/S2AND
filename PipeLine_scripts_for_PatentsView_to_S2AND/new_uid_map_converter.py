import csv
import json
from tqdm import tqdm

delim = "/t"
uuid_map = {}
uuid_counter = 0

print("Creating new UUID with only numbers...")
#rawinventor.tsv:
#"uuid" "patent_id" "inventor_id" "rawlocation_id" "name_first" "name_last" "sequence" "rule_47" "deceased"
inventor_file = open("rawinventor.tsv")
inventors = csv.reader(inventor_file, delimiter='\t')
next(inventors)
for row in tqdm(inventors, desc="Rawinventors", total=18562496):
    invntID = row[2].split('-')[0]
    if uuid_map.get(row[1]) == None:
        uuid_map[row[1]] = uuid_counter
        uuid_counter += 1
print("Converting completed.")
print("")

print("Writing to map_to_new_patentid.json...")
with open("map_to_new_patentid.json", "w") as outfile:
    json.dump(uuid_map, outfile, indent=4)
print("Writing to map_to_new_patentid.json completed.")