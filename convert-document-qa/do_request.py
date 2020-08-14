# send documents to convert-document

import requests
from requests import RequestException

import os

root_dir = "./documents"
files = os.listdir(root_dir)
failed = []
count = 0


def do_request(file_path, file_name):
    global count, failed, files
    fh = open(file_path, 'rb')
    print("convert " + file_name)
    count += 1
    try:
        files = {'file': (file_name, fh, "application/msword")}
        res = requests.post("http://localhost:3000/convert",
                            files=files,
                            timeout=(5, 305),
                            stream=True)
        res.raise_for_status()
        print("OK - " + str(count) + " / " + str(len(files)))
    except RequestException:
        print("Conversion failed")
        failed.append(file_name)
        print(str(len(failed)) + " failed after " + str(count) + " conversions")
        print("\n".join(failed))
    finally:
        fh.close()


for file in files:
    if file.endswith(".docx") or file.endswith(".doc"):
        do_request(root_dir + file, file)

print(str(len(failed)) + " failed after " + str(count) + " conversions")
print("\n".join(failed))
