# utility file, doesn't get executed directly
import csv
import os

folders = {}


def get_file_path(parent_id, file_name):
    parent_path = ""
    if len(parent_id) > 0:
        parent_path = folders[parent_id]
        if isinstance(parent_path, list):
            parent_path = get_file_path(parent_path[0], parent_path[1])
            folders[parent_id] = parent_path

    return os.path.join(parent_path, file_name)


def convert_filename(i):
    return i.strip('"')


def scan_folders(documents_file):
    with open(documents_file, 'r') as f:
        csvreader = csv.DictReader(f, delimiter=',')

        for row in csvreader:
            if row['schema'] != 'Folder':
                continue

            folders[row['id']] = [row['parent_id'], convert_filename(row['file_name'])]

        print(str(len(folders)) + " folders")
        for key, folder in folders.items():
            if isinstance(folder, list):
                folders[key] = get_file_path(folder[0], folder[1])

        print("prepared " + str(len(folders)) + " folders")
