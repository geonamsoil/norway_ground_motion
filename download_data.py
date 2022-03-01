#!/usr/bin/env python3
"""
Author: Daniel Stodle, dsto@norceresearch.no

A sample script for downloading InSAR timeseries data using the InSAR Norway API. The
script starts a query, polls for the query state until completion, then downloads the
resulting CSV files. Typical usage is either:
    python3 IDBRunQuery.py --dataset s1-asc1-v2020 --bbox=20.1404,69.3438,20.1827,69.3293 --path ./tmp/
or
    python3 IDBRunQuery.py --resume f0faedc9e5ab468e98bd2d7ab5cf4ddb --path ./tmp/

A list of valid dataset names can be obtained by executing
    python3 IDBRunQuery.py --list-datasets

Note:
 - asc1, asc2, dsc1 and dsc2 cover all of Norway.
 - asc3 and dsc3 cover only parts of Northern Norway.

1) A query is started by sending an HTTP POST to the following URL, with the bounding
   box specified as part of the URL:
   POST https://host/insar-api/<dataset>/query?bbox=<lon,lat,lon,lat>

2) The response is a JSON object containing a single field:
   { "id" : "unique query id" }

3) The query's progress can be tracked by polling this endpoint:
   GET https://host/insar-api/query-state?id=<query id>

4) The response from the query-state endpoint looks like this:
    {
      "bbox": "20.1404,69.3438,20.1827,69.3293",
      "complete": true,
      "csv": [
        "160-IW2-414-s1-asc1-v2020.csv.gz",
        "160-IW1-414-s1-asc1-v2020.csv.gz"
      ],
      "dataset": "s1-asc1-v2020",
      "duration": 20.55669140815735,
      "expires": 1634555269.487481,
      "id": "3e701ee9b4b247d3857d2d55b5d28f45",
      "messages": [
        "Query initializing",
        "Determining overlapping tiles",
        "Got 4 tiles",
        "Approximately 65536 points to store",
        "Processing tile 1 of 4",
        "Got 5079 points",
        "Tile contains points from 2 different sets",
        "Stored 2122 points to 160-IW2-414-s1-asc1-v2020.csv.gz",
        "Stored 2957 points to 160-IW1-414-s1-asc1-v2020.csv.gz",
        "Stored data from 2 different sets",
        "Finished tile 1 of 4",
        "Processing tile 2 of 4",
        "Got 1581 points",
        "Tile contains points from 2 different sets",
        "Stored 73 points to 160-IW2-414-s1-asc1-v2020.csv.gz",
        "Stored 1508 points to 160-IW1-414-s1-asc1-v2020.csv.gz",
        "Stored data from 2 different sets",
        "Finished tile 2 of 4",
        "Processing tile 3 of 4",
        "Got 15638 points",
        "Tile contains points from 2 different sets",
        "Stored 8054 points to 160-IW2-414-s1-asc1-v2020.csv.gz",
        "Stored 7584 points to 160-IW1-414-s1-asc1-v2020.csv.gz",
        "Stored data from 2 different sets",
        "Finished tile 3 of 4",
        "Processing tile 4 of 4",
        "Got 7206 points",
        "Tile contains points from 2 different sets",
        "Stored 2289 points to 160-IW2-414-s1-asc1-v2020.csv.gz",
        "Stored 4917 points to 160-IW1-414-s1-asc1-v2020.csv.gz",
        "Stored data from 2 different sets",
        "Finished tile 4 of 4",
        "All done"
      ],
      "num_points": 29504,
      "pid": 2823978,
      "progress": 1.0,
      "started": 1634551648.9307897,
      "state": "complete",
      "updated": 1634551669.487481,
      "version": "1.0.0"
    }

5) Once the query is complete (state == "complete" and complete == True), the CSVs listed
   can be downloaded:
   GET https://host/insar-api/query-download?id=<query id>&csv=<csv name>
"""
import os
import sys
import traceback
import requests
import json
import argparse
import time
import pathlib

session = requests.Session()

def start_query(options):
    url = options.host + "/insar-api/"+options.dataset+"/query?bbox="+options.bbox
    result = None
    with session.post(url, data=None) as r:
        if r.status_code != 200:
            print("Failed to start query. Make sure the host is valid: %s" % (options.host))
            raise SystemExit
        result = json.loads(r.content)
    return result["id"]

def write_state(path, state):
    with open(os.path.join(path, "state.json"), "wb") as fd:
        fd.write(state)

def poll_query(options, qid):
    state = None
    print("Query with id %s is executing.." % (qid))
    url = options.host + "/insar-api/"+"query-state?id="+qid
    print("State URL: %s" % (url))
    errors = 0
    # Give query some time to start server side before polling state.
    time.sleep(1)
    while errors < 10:
        try:
            with session.get(url) as r:
                if r.status_code != 200:
                    errors += 1
                    print("HTTP error occured fetching query state: "+
                          "%d. Ignoring and retrying if count < 10: %d" % (r.status_code, errors))
                else:
                    write_state(options.path, r.content)
                    state = json.loads(r.content)
        except:
            errors += 1
            print("Exception occured while polling query state. Retrying: %d" % (errors))
            traceback.print_exc()
        if state:
            print("State: %s %.1f%% complete [%s] Time: %.1f seconds" %
                  (state["state"], state["progress"]*100, state["messages"][-1], state["duration"]))
            if state["state"] == "error":
                print("Error occured executing query. Try again with a smaller area.")
                raise SystemExit
            if state["complete"] == True:
                break
        # We could do something more fancy to estimate how long we need to sleep. But kinda cool to
        # get progress updates too.
        time.sleep(2)
    if errors >= 10:
        print("Giving up on this query")
        raise SystemExit
    return state

def download_results(options, state):
    print("Query finished. Downloading results..")
    for csv in state["csv"]:
        url = options.host + "/insar-api/"+"query-download?id="+qid+"&csv="+csv
        try:
            print("Fetching %s" % (csv))
            filename = csv
            if filename.endswith(".gz"):
                filename = filename[:-3]
            with open(os.path.join(options.path, filename), "wb") as fd,\
                 session.get(url, stream=True) as r:
                for data in r.iter_content(chunk_size=1024*1024):
                    fd.write(data)
            print("Finished downloading %s" % (csv))
        except:
            print("Exception occured while downloading csv %s. "+
                  "Feel free to try a manual download:" % (csv))
            print("URL: %s" % (url))
            traceback.print_exc()
    print("All results downloaded (hopefully)")

if __name__ == "__main__":
    datasets = [ "in-asc1-v20a", "in-asc2-v20a", "in-asc3-v20a",
                 "in-dsc1-v20a", "in-dsc2-v20a", "in-dsc3-v20a" ]
    parser = argparse.ArgumentParser(description="IDBRunQuery")
    parser.add_argument("--path", default=None, required=False, action="store",
                        help="The directory to store query results in.")
    parser.add_argument("--bbox", default=None, required=False, action="store",
                        help="The bounding box in lon,lat,lon,lat. "+
                        "NOTE: Specify as --bbox=lon,lat,lon,lat")
    parser.add_argument("--dataset", default=None, required=False, action="store",
                        help="The dataset to perform the query on. "+
                        "Valid datasets are %s" % (",".join(datasets)))
    parser.add_argument("--host", default="https://insar.ngu.no", action="store",
                        help="Host to query.")
    parser.add_argument("--resume", default=None, action="store",
                        help="Query ID to resume")
    parser.add_argument("--cert", default="", action="store",
                        help="The root certificate to use for verifying the remote host")
    parser.add_argument("--list-datasets", default=False, action="store_true")
    options = parser.parse_args()
    if len(options.cert) > 0:
        session.verify = options.cert
        print(f"Verifying remote certificate using root certificate at {options.cert}")
    # Try to make host comply with http[s]://host[:port]
    if not options.host.startswith("http"):
        options.host = "https://" + options.host
    if options.host.endswith("/"):
        options.host = options.host[:-1]
    if options.list_datasets:
        with session.get(options.host + "/insar-api/list-datasets") as r:
            datasets = json.loads(r.content)
            groups = { }
            for ds in datasets:
                if ds["group"] in groups:
                    groups[ds["group"]].append(ds)
                else:
                    groups[ds["group"]] = [ds]
            for group_name, datasets in groups.items():
                print(f"{group_name}:")
                for ds in datasets:
                    print(f"  * {ds['displayName']}: {ds['name']}")
            raise SystemExit
    if not options.path:
        print("The --path argument is required")
        raise SystemExit
    # Make destination directory
    pathlib.Path(options.path).mkdir(parents=True, exist_ok=True)
    qid = None
    if options.resume != None:
        qid = options.resume
    else:
        if not options.bbox or not options.dataset:
            print("You must specify a --bbox and --dataset.")
            raise SystemExit
        qid = start_query(options)
    state = poll_query(options, qid)
    download_results(options, state)
