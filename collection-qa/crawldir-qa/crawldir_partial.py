# run crawldir for specific files
# execute in the aleph shell:
# exec(open("crawldir_partial.py").read())
import csv
from pathlib import Path
from servicelayer.jobs import Job
from aleph.logic.documents import crawl_directory
from aleph.model import Collection, Document

BASE_SOURCE_PATH = "/"  # source of your documents on the filesystem, relative to the container
COLLECTION_ID = 1

job_id = Job.random_id()
collection = Collection.by_id(COLLECTION_ID)
with open('missing_files_crawldir.csv', 'r') as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        document_path = row[0]
        document_parent_id = row[1]
        full_document_path = BASE_SOURCE_PATH + document_path

        print("crawl " + full_document_path)
        path = Path(full_document_path)
        document_parent = Document.by_id(document_parent_id)
        crawl_directory(collection, path, parent=document_parent, job_id=job_id)

