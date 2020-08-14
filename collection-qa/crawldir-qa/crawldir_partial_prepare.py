import os
import status_utils

status_utils.scan_folders("../data/collection_documents.csv")
folders = dict((v[7:], k) for k, v in status_utils.folders.items())
print("prepared folders")

files_to_crawl = {}
folders_to_crawl = {}
folders_to_skip = set()

done = 0
total = 3181459
report_after = round(total / 20)
with open("../data/filelist_diff.txt", 'r') as f:
    for line in f:
        done += 1
        if done % report_after == 0:
            print("done: " + str(round((done / total) * 100)) + "%")

        path = line[2:]
        path = os.path.normpath(path).strip()
        parent_folder = os.path.split(path)[0]

        if parent_folder in folders_to_skip or parent_folder in folders_to_crawl:
            # print("skip " + path)
            continue
        elif parent_folder in folders:
            folder_id = folders[parent_folder]
            files_to_crawl[path] = folder_id
            # print("found direct parent - folder id: " + str(folder_id) + " parent folder: " + parent_folder + " path: " + path)
        else:
            while len(parent_folder) > 0:
                folders_to_skip.add(parent_folder)
                next_parent_folder = os.path.split(parent_folder)[0]
                if len(next_parent_folder) <= 0:
                    print("did not found a parent: " + path)
                    break
                # print("search for secondary parent: " + parent_folder)
                if next_parent_folder in folders:
                    folder_id = folders[next_parent_folder]
                    folders_to_crawl[parent_folder] = folder_id
                    # print("found secondary parent - folder id: " + str(
                    #    folder_id) + " parent folder: " + parent_folder + " path: " + path)
                    break
                parent_folder = next_parent_folder

with open("../data/missing_files_crawldir.csv", "w") as f:
    for key, value in files_to_crawl.items():
        f.write("\"" + key + "\"," + value + "\n")

    for key, value in folders_to_crawl.items():
        f.write("\"" + key + "\"," + value + "\n")
