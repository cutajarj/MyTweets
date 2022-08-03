#!/usr/bin/python
"""Fetches relevant metrics from Storm-UI"""

from __future__ import print_function
import sys
from time import sleep, time
from threading import Thread
import json
import os
import pycurl
import socket
from StringIO import StringIO
import re
import urllib

PERIOD = 30 # in secs
BLOCKSIZE = 2 # number of topologies per thread

URL = "http://0:8081/api/v1"
BASE = "platform.ofs.cluster"
HOSTNAME = socket.gethostname()

CLUSTER_METRICS = ["slotsUsed", "slotsTotal", "slotsFree", "executorsTotal", "topologies", "supervisors", "tasksTotal"]
SUPERVISOR_METRICS = ["slotsTotal", "slotsUsed"]
TOPOLOGIES_METRICS = ["workersTotal", "executorsTotal", "tasksTotal", "replicationCount"]
SPOUTS_METRICS = ["acked", "completeLatency", "emitted", "executors", "failed", "tasks", "transferred"]
BOLTS_METRICS = ["acked", "capacity", "emitted", "executeLatency", "executed", "executors", "failed", "processLatency", "tasks", "transferred"]

EMPTY=""

blacklist=["sp1","nxt","drk","dark","prd","prf","prod","ie1","ie2","release","\d{1,}","_{2,}","-{2,}"]

#compile regexp
rx_blacklist = re.compile('|'.join(blacklist), re.IGNORECASE)
rx_nonAlpha_termination=re.compile('[^a-zA-Z]+$')
rx_spaces=re.compile('\s+')

def multiple_replace(text, list):
    return rx_blacklist.sub(EMPTY, text)

def is_leader():
    for nimbus in get_json(URL + "/nimbus/summary", "nimbuses"):
        if nimbus["host"] == HOSTNAME:
            if nimbus["version"] == "0.11.0-SNAPSHOT":
                return nimbus["isLeader"] is True
            else:
                return nimbus["status"] == "Leader"

    return False

def sublist(full_list, size):
    return [full_list[i:i+size] for i in range(0, len(full_list), size)]

def metric(prefix, metricname, timestamp, value, dimensions):
    """ Prints out the metric """
    tags = " ".join(["%s=%s" % (k,v) for k,v in dimensions.iteritems()])
    sys.stdout.write("%s.%s %s %s %s\n" % (prefix, metricname, timestamp, value, tags)) # print is not threadsafe

def get_json_object(endpoint):
    """ Retrieves the JSON object from the API """
    data = StringIO()

    request = pycurl.Curl()
    request.setopt(request.URL,endpoint)
    request.setopt(request.WRITEFUNCTION, data.write)
    result = request.perform()

    json_data = data.getvalue()
    return json.loads(json_data)

def get_json(endpoint, jsonField):
    """ Retrieves the JSON field from the API object """
    return get_json_object(endpoint)[jsonField]

def print_supervisors():
    for supervisor in get_json(URL + "/supervisor/summary", "supervisors"):
        host = supervisor["host"]
        for metricname in SUPERVISOR_METRICS:
            metric(BASE+".supervisors", metricname, timestamp, supervisor[metricname], {"host":host})

def print_cluster():
    cluster_info = get_json_object(URL + "/cluster/summary")
    for metricname in CLUSTER_METRICS:
        metric(BASE, metricname, timestamp, cluster_info[metricname], {})

def print_lag(topology_id, topology_name):
    lags = get_json_object(URL + "/topology/" + topology_id + "/lag")
    for (spout, infoSpout) in lags.items():
        if "spoutLagResult" in infoSpout:
            for (topic, infoTopic) in infoSpout["spoutLagResult"].items():
                for (partition, infoPartition) in infoTopic.items():
                    if infoPartition["consumerCommittedOffset"] != -1:
                        metric(BASE + ".topology." + topology_name, "lag", timestamp, infoPartition["lag"], {"topic": topic, "partition": partition})

def print_errors(topology_name, component, topology_id, component_id, component_type = "bolt"):
    last_error_time = component["errorLapsedSecs"]
    if (last_error_time is not None and last_error_time <= PERIOD):
        comp_stats = get_component_stats(topology_id, component_id)
        all_errors = comp_stats["componentErrors"]
        error_nr = len([error["errorLapsedSecs"] <= PERIOD for error in all_errors])
        metric(BASE+".topology."+topology_name, "errors", timestamp, error_nr, {"host":component["errorHost"], component_type:component_id})

def get_component_stats(topology_id, component_id):
    return get_json_object(URL + "/topology/" + topology_id + "/component/" + urllib.quote(component_id))

def get_topology_name(topology_name):
    try:
        blacklist_result = multiple_replace(topology_name, blacklist)
        sanitized_name = rx_nonAlpha_termination.sub(EMPTY, blacklist_result)
        return sanitized_name
    except Exception as e:
        return ""

def print_topologies(topologies):
    for topology in topologies:
        if topology["status"] == "ACTIVE":
            topology_name = get_topology_name(topology["name"])
            topology_id = str(topology["id"]) # Unicode to string

            print_lag(topology_id, topology_name)

            # Per-topology metrics
            for metricname in TOPOLOGIES_METRICS:

                metric(BASE+".topology."+topology_name, metricname, timestamp, topology[metricname], {})

                # Topology-specific metrics
            stats = get_json_object(URL + "/topology/" + topology_id)
            for spout in stats["spouts"]:
                spout_id = str(spout["spoutId"])
                # comp_stats = get_component_stats(topology_id, spout_id)
                # host = comp_stats["executorStats"][0]["host"]
                host = "none"
                trimmed_spout_id=rx_spaces.sub('-',spout_id)
                for metricname in SPOUTS_METRICS:
                    metric(BASE+".topology."+topology_name, metricname, timestamp, spout[metricname], {"spout":trimmed_spout_id, "host":host})

                # Error metrics.
                print_errors(topology_name, spout, topology_id, spout_id, "spout")

            for bolt in stats["bolts"]:
                bolt_id = str(bolt["boltId"])
                # comp_stats = get_component_stats(topology_id, spout_id)
                # host = comp_stats["executorStats"][0]["host"]
                host = "none"
                trimmed_bolt_id=rx_spaces.sub('-',bolt_id)
                for metricname in BOLTS_METRICS:
                    metric(BASE+".topology."+topology_name, metricname, timestamp, bolt[metricname], {"bolt":trimmed_bolt_id, "host":host})

                # Error metrics.
                print_errors(topology_name, bolt, topology_id, bolt_id)

if __name__ == "__main__":
    # TODO Change this!
    for i in range(1):

        timestamp = int(time()) # int removes the msecs section

        if (is_leader()):

            threads = []

            cluster_thread = Thread(target=print_cluster)
            cluster_thread.start()
            threads.append(cluster_thread)

            supervisor_thread = Thread(target=print_supervisors)
            supervisor_thread.start()
            threads.append(supervisor_thread)

            all_topologies = get_json(URL + "/topology/summary", "topologies")
            for block in sublist(all_topologies, BLOCKSIZE):
                t = Thread(target=print_topologies, args=(block,))
                t.start()
                threads.append(t)

            for thread in threads:
                thread.join()

        sys.stdout.flush()
        now = int(time())
        sleep_for = max(PERIOD - (now - timestamp), 0)
        # TODO remove this:
        print("Completed in ", (now - timestamp))
        sleep(sleep_for) # sleeps main thread for period, adjusted for the processing time.

sys.exit(0)
