import csv
import status_utils

config = {
    "documents_file": '../data/collection_documents.csv',
    "output_file": '../data/collection_db_documents.csv'
}

status_utils.scan_folders(config["documents_file"])


with open(config["documents_file"], 'r') as f:
    csvreader = csv.DictReader(f, delimiter=',')
    with open(config["output_file"], 'w') as rf:
        for row in csvreader:
            if row['schema'] == 'Folder':
                continue

            file_name = status_utils.convert_filename(row['file_name'])
            file_path = status_utils.get_file_path(row['parent_id'], file_name)
            file_path = file_path.replace("collection/", "")
            rf.write("./" + file_path + "\n")

print("done")
# sort the files (prepare for faster diff):
# sort collection_documents.csv > collection_documents_sorted.csv
# sort collection_db_documents.csv > collection_db_documents_sorted.csv
# diff: diff collection_db_documents_sorted.csv collection_documents_sorted.csv > diff.txt
