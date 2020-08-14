import csv

file_ids = set()

with open('../data/collection_documents.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    for row in csvreader:
        file_ids.add(row['id'])

print("got " + str(len(file_ids)) + " file ids")

done = 0
removed = 0
with open('../data/collection_ftm.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    for row in csvreader:
        file_id = row['id'].split('.')[0]
        if file_id in file_ids:
            file_ids.remove(file_id)
            removed += 1
        elif len(row['id']) < 80:
            print(file_id)
        done += 1
        if done % 100000 == 0:
            print("done: " + str(done))
print(str(removed))

with open('../data/collection_ftm_missing.csv', 'w') as rf:
    for f_id in file_ids:
        rf.write(f_id + "\n")
