#!/usr/bin/python
"""
A log replay tool
"""

from datetime import datetime
import logging
import sys
import time
import requests
from custom_filters import get_filters


def load_log(log_file):
    """Read the log file and return lines as a dictionary

	log_file -- the path to the log file
	"""
    file_lines = {}
    for line in open(log_file, 'r'):
        parts = line.split(" ")
        log_time = datetime.strptime(parts[0] + " " + parts[1],
                                     '%Y-%m-%d %H:%M:%S,%f')
        # Assume that the last part of a log line is the data part
        log_query = parts[-1]
        file_lines[log_time] = log_query
    return file_lines


def filter_logs(logs, target_params, extra_params):
    """Filter a logs dictionary based input target parameters.

    logs -- the input logs dictionary
    target_params -- the interested set of input parameter keys
    extra_params -- the list of parameters to be added input from command line
    """
    if len(target_params) == 0:
        return logs
    filtered_logs = {}
    for key, value in logs.iteritems():
        # val can be 'id&' or 'id=xxx&'
        filtered_values = [val for val in value.split("&") \
         if val in target_params or val[:val.index('=')] in target_params]
        values = apply_custom_filters(filtered_values)
        filtered_logs[key] = "&".join(values + extra_params)
    return filtered_logs


def apply_custom_filters(values):
    """Apply custom key/value filter functions loaded
    dynamically from an external file 'custom_filters.py'

    values -- the list of values to be filtered
    """
    filtered_values = [apply_filter(v) for v in values]
    return filtered_values


def apply_filter(value):
    """Apply all filters registered in
	get_filters() to the value.

	value -- the value to be filtered
	"""
    enabled_filters = get_filters()
    for filt in enabled_filters:
        value = filt(value)
    return value


def send_queries(logs, url, query_path):
    """Send logs as HTTP requests to an endpoint

    logs -- the dictionary of logs
    url -- the endpoint that receives HTTP requests
    query_path -- the HTTP query path to use for every request as prefix
    """
    times = sorted(list(logs.keys()))
    delays = build_delays(times)
    logging.info("Using delays in milliseconds: %s", delays)
    for log_time in times:
        params = logs[log_time]
        status_code = send_query(params, url, query_path)
        if status_code != 200:
            logging.error("Request failed: %s -> %s", status_code, params)
        else:
            logging.info("200 %s", params)
        if len(delays) > 0:
            delay = delays.pop(0)
            logging.info("Waiting %s msec(s) for next query ...", delay)
            time.sleep(delay / 1000.0)


def send_query(query, url="http://httpbin.org", path="/get"):
    """Send a single HTTP query to an endpoint

    query -- the query string for the HTTP request
    url -- the endpoint URL
    path -- the endpoint prefix path
    """
    response = requests.get(url + path, params=query)
    logging.debug("Completed: %s", response.url)
    return response.status_code


def build_delays(times):
    """Build a list of delays in mill-seconds from the times
    of logs loaded from the file

    times -- the list of log time stamps loaded from the log file
    """
    t_0 = times[0]
    delays = []
    for log_t in times:
        delta = log_t - t_0
        delta_ms = delta.microseconds / 1000.0
        delays.append(delta_ms)
    # First query does not wait; assert delays[0] == 0
    delays.pop(0)
    return delays

def main(args):
    """The main function

    args -- the program arguments
    """
    log_file = args[1]
    target_params = args[2].split(",")
    extra_params = args[3].split(",")
    url = args[4]
    query_path = args[5]

    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    lines = load_log(log_file)
    logging.info("Loaded log file. Size: %s", len(lines))

    logging.info("Using extr query parameters: %s", extra_params)
    logging.info("Using target query parameters: %s", target_params)
    logs = filter_logs(lines, target_params, extra_params)
    logging.info("Filtered logs. Size: %s", len(logs))

    send_queries(logs, url, query_path)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: logreplay.py LOG_FILE TARGET_PARAMS EXTRA_PARAMS URL QUERY_PATH"
        sys.exit(1)

    main(sys.argv)
