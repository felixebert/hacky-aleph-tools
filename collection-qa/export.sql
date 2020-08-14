/* export documents of a collection */
COPY (SELECT id,content_hash,schema,parent_id,meta->'file_name' AS file_name FROM document WHERE collection_id = 1) TO 'collection_documents.csv' WITH CSV DELIMITER ',' HEADER;
/* export ingest status from the ftm-table of a collection */
COPY (SELECT id, entity->'properties'->'contentHash' AS content_hash, entity->'properties'->'processingStatus' AS processing_status, entity->'schema' AS schema FROM ftm_collection_1 WHERE origin = 'ingest' AND fragment = 'default') TO 'collection_ftm.csv' WITH CSV DELIMITER ',' HEADER;
/* export ingest status from the balkhash-table of a collection */
COPY (SELECT id, properties->'contentHash' AS content_hash, properties->'processingStatus' AS processing_status, schema FROM balkhash_collection_1 WHERE schema != 'Folder' AND fragment = 'default' AND LENGTH(id) < 32) TO 'collection_balkhash.csv' WITH CSV DELIMITER ',' HEADER;
