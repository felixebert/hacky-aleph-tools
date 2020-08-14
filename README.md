various hacky, difficult to understand and sometimes dangerous command line tools for aleph, which get hopefully unnecessary soon.

Covered use cases:
- analyze completeness of a collection and partially fix errors (collection-qa)
    - does the document table include all files of the source? (missing files in crawldir / upload step?)
    - partial crawldir
    - are there ingest errors or files that did not get ingested yet?
    - partial ingest
- analyze errors of convert-document (convert-document-qa)
    - extract documents that can't be converted for further analysis
- search for a mention of a person / company of interest (crossref)
