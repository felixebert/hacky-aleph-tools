import json
import csv

file_ids = set()
folder_ids = set()
with open('../data/collection_documents.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    for row in csvreader:
        if row['schema'] == 'Folder':
            folder_ids.add(row['id'])
        else:
            file_ids.add(row['id'])
print("found " + str(len(file_ids)) + " file ids")


failed_file_ids = set()
done = 0
total = 17644674
report_after = round(total / 20)
test_id_sent = 0
with open('../data/collection_ftm.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')

    for row in csvreader:
        done += 1
        if done % report_after == 0:
            print("done: " + str(round((done / total) * 100)) + "%")

        if "fail" not in row['processing_status']:
            continue

        file_id = row['id'].split('.')[0]
        if file_id in file_ids or len(row['id']) > 80:
            failed_file_ids.add(file_id)
            if test_id_sent < 10:
                print("missing: " + row['id'] + " - " + json.dumps(row))
                test_id_sent += 1

print("found " + str(len(failed_file_ids)) + " failures")


with open('../data/collection_documents.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    with open('../data/collection_ftm_failures.csv', 'w') as rf:
        for row in csvreader:
            if row['schema'] == 'Folder' or row['id'] not in failed_file_ids:
                continue

            rf.write(row['id'] + "\n")
