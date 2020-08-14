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
total = 11153457
report_after = round(total / 20)
test_id_sent = 0
with open('../data/collection_balkhash.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')

    for row in csvreader:
        done += 1
        if done % report_after == 0:
            print("done: " + str(round((done / total) * 100)) + "%")

        if len(row['id']) > 80 or "success" in row['processing_status']:
            continue

        if row['id'] in file_ids:
            failed_file_ids.add(row['id'])
        elif test_id_sent < 10 and row['id'] not in folder_ids:
            print("missing: " + row['id'])
            test_id_sent += 1

print("found " + str(len(failed_file_ids)) + " failures")


with open('../data/collection_documents.csv', 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    with open('../data/collection_balkhash_failures.csv', 'w') as rf:
        for row in csvreader:
            if row['schema'] == 'Folder' or row['id'] not in failed_file_ids:
                continue

            rf.write(row['id'] + "\n")
