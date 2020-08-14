# analyze the logfile of a convert-document container
# extracts for each file: file_name, mime_type, duration of conversion, status (success / error) and error_message

import json
import re
from datetime import datetime

regex_pdf_convert = re.compile(r"PDF convert: /tmp/convert/([^ ]+) \[([^\]]+)\]")
document_log = {}


def get_document(line):
    matches = re.search(regex_pdf_convert, line)
    return {
        "file_name": matches.group(1),
        "mime_type": matches.group(2)
    }


def get_log_entry(document):
    file_name = document['file_name']
    existing_entry = None
    if file_name in document_log:
        existing_entry = document_log[file_name]
    if existing_entry is None:
        document['events'] = []
        document_log[file_name] = document
        return document
    else:
        return existing_entry


def strip_nanoseconds(time):
    parts = time.split(".")
    return parts[0] + '.' + parts[1][:6].replace("Z", "")


def calculate_duration(start_time, end_time):
    start = datetime.strptime(strip_nanoseconds(start_time), "%Y-%m-%dT%H:%M:%S.%f")
    end = datetime.strptime(strip_nanoseconds(end_time), "%Y-%m-%dT%H:%M:%S.%f")
    delta = end - start
    return delta.total_seconds()


def record_event(document_data, outcome, converter_id):
    if document_data is None:
        return False
    log_entry = get_log_entry(document_data['document'])
    start_time = document_data['line']['time']
    entry = {
        "start_ts": datetime.strptime(strip_nanoseconds(start_time), "%Y-%m-%dT%H:%M:%S.%f").timestamp(),
        "start": start_time,
        "end": outcome['end_time'],
        "duration": calculate_duration(start_time, outcome['end_time']),
        "status": outcome['status'],
        "converter": converter_id,
        "error_message": document_data['error_message'] if "error_message" in document_data else None
    }

    log_entry['events'].append(entry)


def analyze_file(file, converter_id):
    with open(file, 'r') as logfile:
        current_document_data = None
        for line in logfile:
            line_data = json.loads(line)

            if line_data['log'].startswith('INFO:convert:PDF convert:'):
                outcome = {
                    'status': 'success',
                    'end_time': line_data['time']
                }
                record_event(current_document_data, outcome, converter_id)

                # new document
                document = get_document(line_data['log'])
                print("processing " + document['file_name'])
                if len(document['file_name']) > 6:
                    current_document_data = {
                        "document": document,
                        "line": line_data,
                        "error_message": None
                    }
                else:
                    current_document_data = None

            if 'Document conversion timed out' in line_data['log'] and current_document_data is not None:
                current_document_data["error_message"] = "timeout"

            if 'Disposing of LibreOffice' in line_data['log']:
                outcome = {
                    'status': 'error',
                    'end_time': line_data['time']
                }
                record_event(current_document_data, outcome, converter_id)
                current_document_data = None


analyze_file("data/v3.8/convert-document_1.log", "1")

error_count = 0
at_least_one_error_count = 1
for key, value in document_log.items():
    value['events'] = sorted(value['events'], key=lambda e: e['start_ts'])
    has_only_errors = True
    at_least_one_error = False
    for event in value['events']:
        if event['status'] == 'success':
            has_only_errors = False
        if event['status'] == 'error':
            at_least_one_error = True
    if has_only_errors:
        error_count += 1
        value['result'] = "only_errors"
    elif at_least_one_error:
        at_least_one_error_count += 1
        value['result'] = "at_least_one_error"
    else:
        value['result'] = "no_errors"

print("has only errors: " + str(error_count))
print("at least one error: " + str(at_least_one_error_count))
print(len(document_log.keys()))

# document_log = list(filter(lambda i: i["result"] != "no_errors", document_log.values()))
document_log = list(document_log.values())
document_log = sorted(document_log, key=lambda e: e['events'][0]['start_ts'])
with open('out/v3.8/result.json', 'w', encoding='utf-8') as f:
    json.dump(document_log, f, ensure_ascii=False, indent=4)
with open('out/v3.8/result_onlyerrors.json', 'w', encoding='utf-8') as f:
    json.dump(list(filter(lambda i: i["result"] == "only_errors", document_log)), f, ensure_ascii=False, indent=4)
