import csv

balkhash_ids = set()

with open('../data/collection_balkhash.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    for row in csvreader:
        balkhash_ids.add(row['id'])
print("got " + str(len(balkhash_ids)) + " balkhash ids")

done = 0
with open('../data/collection_ftm.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    for row in csvreader:
        file_id = row['id'].split('.')[0]
        if file_id in balkhash_ids:
            balkhash_ids.remove(file_id)
        done += 1
        if done % 100000 == 0:
            print("done: " + str(done))

with open('../data/collection_ftm_bh_missing.csv', 'w') as rf:
    for b_id in balkhash_ids:
        rf.write(b_id + "\n")
