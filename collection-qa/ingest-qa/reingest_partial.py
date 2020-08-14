# execute in the aleph shell:
# exec(open("reingest_partial.py").read())
from servicelayer.jobs import Job
from aleph.queues import ingest_entity
from aleph.model import Collection, Document

job_id = Job.random_id()
collection = Collection.by_id(125)
with open('collection_ftm_failures.csv', 'r') as f:
    for document_id in f:
        print("reingest " + document_id)
        document = Document.by_id(document_id)
        proxy = document.to_proxy(ns=collection.ns)
        ingest_entity(collection, proxy, job_id=job_id, index=True)

