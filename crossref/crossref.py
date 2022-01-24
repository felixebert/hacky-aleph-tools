# This script creates a cross-ref by executing a search for a list of names / search-terms in an input file
# as if you would enter the name yourself in the search bar of aleph
# per search term, max 10 results get stored in the outfile.
# If all 10 results are interesting you should search manually for more results

import csv
import logging
import re
import requests
import time

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

#
# SETTINGS
#
INPUT_FILE = "offshore_entities.csv"  # plain list of names / search terms, one column, no title
OUTPUT_FILE = "out.csv"
ALEPH_INSTANCE = "https://data.occrp.org/"
# use browser dev tools to get the Bearer Token from the Authorization Header in XHR requests
AUTH_TOKEN = "<PASTE YOUR BEARER AUTH TOKEN, e.g. Bearer XXXXX>"


#
#
#

def get_searchterms():
    with open(INPUT_FILE, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        result = []
        for r in csvreader:
            result.append(r[0])

        return result


def search_aleph(term):
    headers = {"Authorization": AUTH_TOKEN, "Accept": "application/json"}
    params = {
        "q": term,
        "limit": 10,
        "filter:schemata": "Thing",
        "highlight": "true",
        "highlight_count": "3",
        "highlight_length": 280
    }
    url = ALEPH_INSTANCE + "api/2/entities"
    r = requests.get(url, params=params, headers=headers)
    try:
        res = r.json()
    except Exception as e:
        log.error("got invalid response from " + r.url + " - no valid json: " + r.text)
        raise e

    if res.get("results") is not None:
        return res.get("results")
    else:
        return []


def convert_results(api_results, searchterm):
    converted_results = []
    for api_result in api_results:
        preview = ''
        if api_result.get('highlight') is not None:
            preview = ' '.join(api_result['highlight']) \
                .replace("<em>", "") \
                .replace("</em>", "") \
                .replace("<strong>", "") \
                .replace("</strong>", "")
            preview = re.sub(r"\n", "; ", preview)
        converted_result = {
            "Suchbegriff": searchterm,
            "Collection": api_result['collection']['label'],
            "Dokumentname": api_result['title'] if api_result.get('title') is not None else '',
            "Dateiname": api_result['file_name'] if api_result.get('file_name') is not None else '',
            "Autor": api_result['author'] if api_result.get('author') is not None else '',
            "Vorschau": preview,
            "Link": api_result['links']['ui']
        }
        for key, value in converted_result.items():
            converted_result[key] = value.encode("utf-8")
        converted_results.append(converted_result)

    return converted_results


results = []
searchterms = get_searchterms()
for index, searchterm in enumerate(searchterms):
    try:
        searchterm_results = search_aleph(searchterm)
        searchterm_results = convert_results(searchterm_results, searchterm)
        for result in searchterm_results:
            results.append(result)
        log.info(str(index) + "/" + str(len(searchterms)) + ", total " + str(
            len(results)) + ": search for " + searchterm + " added " + str(len(searchterm_results)) + " results")

        # avoid too many requests error
        time.sleep(1.8)
    except Exception:
        log.exception(str(index) + "/" + str(len(searchterms)) + ", total " + str(
            len(results)) + ": search for " + searchterm + " failed!")

with open(OUTPUT_FILE, 'w', newline='') as outputfile:
    fieldnames = ["Suchbegriff", "Collection", "Dokumentname", "Dateiname", "Autor", "Vorschau", "Link"]
    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)
