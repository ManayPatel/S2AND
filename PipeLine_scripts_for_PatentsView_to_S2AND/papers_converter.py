import csv
import json
from tqdm import tqdm

#     7627233 patent.tsv
#     6980577 rawassignee.tsv
#    18562496 rawinventor.tsv
#   115170635 uspatentcitation.tsv

delim = "/t"
uuid_map = {}

print("Reading map to new UUID...")
with open("map_to_new_patentid.json", 'r') as fd:
    uuid_map = json.load(fd)
print("Reading completed.")
print("")

paper_obj = {}

print("Reading patent file...")
#patent.tsv format:
#"id" "type" "number" "country" "date" "abstract" "title" "kind" "num_claims" "filename" "withdrawn"
patent_file = open("patent.tsv")
patent_data = csv.reader(patent_file, delimiter='\t')
next(patent_data)
for row in tqdm(patent_data, desc="Patents", total=7627233):
    row_obj = {}
    if uuid_map.get(row[0]) == None:
        continue
    row_obj["paper_id"] = uuid_map.get(row[0])
    row_obj["title"] = row[6]
    row_obj["abstract"] = row[5]
    row_obj["year"] = int(row[4].split("-")[0])
    paper_obj[row_obj.get("paper_id")] = row_obj
patent_file.close()
print("Reading patent file completed.")
print("")

print("Reading rawassignee file...")
#rawassignee.tsv:
#"uuid" "patent_id" "assignee_id" "rawlocation_id" "type" "name_first" "name_last" "organization" "sequence"
rawassignee_file = open("rawassignee.tsv")
assignee_data = csv.reader(rawassignee_file, delimiter='\t')
next(assignee_data)
for row in tqdm(assignee_data, desc="Assignee", total=6980577):
    org = row[7]
    if org == "":
        org = row[5] + " " + row[6]
    if uuid_map.get(row[1]) == None:
        continue
    row_obj = paper_obj[uuid_map.get(row[1])]
    row_obj["journal_name"] = org
    row_obj["venue"] = org
    paper_obj[uuid_map.get(row[1])] = row_obj
rawassignee_file.close()
print("Reading rawassignee file completed.")
print("")

print("Reading citations file...")
#uspatentcitation.tsv:
#"uuid" "patent_id" "citation_id" "date" "name" "kind" "country" "category" "sequence"
citation_file = open("uspatentcitation.tsv")
citation_data = csv.reader(citation_file, delimiter='\t')
next(citation_data)
for row in tqdm(citation_data, desc="Citation", total=115170635):
    if uuid_map.get(row[2]) == None:
        continue
    if uuid_map.get(row[1]) == None:
        continue
    row_obj = paper_obj[uuid_map.get(row[1])]
    citations = row_obj.get("references", [])
    citations.append(uuid_map.get(row[2]))
    row_obj["references"] = citations
    paper_obj[uuid_map.get(row[1])] = row_obj
citation_file.close()
print("Reading citations file completed.")
print("")

print("Reading rawinventor file...")
#rawinventor.tsv:
#"uuid" "patent_id" "inventor_id" "rawlocation_id" "name_first" "name_last" "sequence" "rule_47" "deceased"
rawinvntr_file = open("rawinventor.tsv")
invntr_data = csv.reader(rawinvntr_file, delimiter='\t')
next(invntr_data)
for row in tqdm(invntr_data, desc="RawInventor Data", total=18562496):
    if uuid_map.get(row[1]) == None:
        continue
    author_obj = {}
    author_obj["position"] = int(row[6])
    author_obj["author_name"] = row[4] + " " + row[5]
    row_obj = paper_obj[uuid_map.get(row[1])]
    authors = row_obj.get("authors", [])
    authors.append(author_obj)
    row_obj["authors"] = authors
    paper_obj[uuid_map.get(row[1])] = row_obj
rawinvntr_file.close()
print("Reading rawinventor file completed.")
print("")

print("Writing to patent_papers.json...")
with open("err_patent_papers.json", "w") as outfile:
    json.dump(paper_obj, outfile, indent=4)
print("Writing to patent_papers.json completed.")