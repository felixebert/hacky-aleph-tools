# after running analyze_logfile.py, you can use this tool to
# collect files which were sent to the convert-document container
# use case would be e.g. to retrieve all files which have caused an error for further analysis
import json
from normality import safe_filename

ANALYZE_RESULT_FILE = "result.json"  # result of analyze_logfile.py
FILELIST = "filelist.txt"  # create a file list of your source: find -type f ./* > filelist.txt

# normalize filenames, so they match the filename in the logfile of convert-document
with open(FILELIST, "r") as f_input:
    with open("filelist_normalized.txt", "w") as f_output:
        for cnt, line in enumerate(f_input):
            filepath_parts = line.strip().split("/")
            filename = filepath_parts[len(filepath_parts) - 1]
            filename_parts = filename.split(".")
            if len(filename_parts) > 1:
                extension = filename_parts.pop().lower()
                filename_normalized = safe_filename(".".join(filename_parts), extension=extension)
                if filename_normalized is not None:
                    f_output.write("/".join(filepath_parts) + "\t" + filename_normalized + "\n")
            if cnt % 100000 == 0:
                print("prepare progress: " + str(cnt))

result = []
with open(ANALYZE_RESULT_FILE, 'r') as f:
    documents = json.load(f)
    file_names = list(map(lambda d: d['file_name'], documents))

    with open("filelist_normalized.txt") as f:
        for cnt, line in enumerate(f):
            filename = line.strip().split("\t").pop()
            if filename in file_names:
                result.append({
                    "source": line.strip().split("\t")[0],
                    "target": filename
                })
                print("MATCH for " + filename)
            if cnt % 100000 == 0:
                print("search progress: " + str(cnt))

with open("copy.sh", "w") as out:
    for entry in result:
        out.write("cp \"" + entry['source'] + "\" ./" + entry['target'] + "\n")
