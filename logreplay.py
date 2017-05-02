#!/usr/bin/python
"""
A log replay tool
"""

from datetime import datetime
import argparse
import logging
import sys
import time
import requests
import threading
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


def filter_logs(logs, log_params, extra_params, delay):
    """Filter a logs dictionary based input target parameters.

    logs -- the input logs dictionary
    target_params -- the parameters to extract from the log file
    extra_params -- the extra parameters to be added (inputted from command line)
    delay -- add delay as an extra parameter
    """
    if len(log_params) == 0:
        return logs

    times = sorted(list(logs.keys()))
    delays = build_delays(times)

    filtered_logs = {}
    for key, value in sorted(logs.items()):
        # val can be 'id&' or 'id=xxx&'
        filtered_values = [val for val in value.split("&") \
         if val in log_params or val[:val.index('=')] in log_params]
        
        if (delay and len(delays) > 0):
            delay_val = delays.pop(0)
            #logging.info("delay before trans: %s", delay_val)
            delay_param = "delay=" + str(delay_val)
            #logging.info("delay after string conv: %s", delay_param)
            filtered_values.append(delay_param)

        values = apply_custom_filters(filtered_values)
        #logging.info("delay after trans: %s", values)
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


def send_queries(logs, url, use_delay):
    """Send logs as HTTP requests to an endpoint

    logs -- the dictionary of logs
    url -- the URL of the HTTP endpoint to send requests to
    """
    times = sorted(list(logs.keys()))
    delays = build_delays(times)
    for log_time in times:
        params = logs[log_time]

        # sent query in separate thread
        t = threading.Thread(target=send_query, args=(params,url,))
        t.start()

        if (use_delay and len(delays) > 0):
            delay = delays.pop(0)
            logging.info("Waiting %s msec(s) for next query ...", delay)
            time.sleep(delay / 1000.0)


def send_query(query, url="http://httpbin.org/get"):
    """Send a single HTTP query to an endpoint

    query -- the query string for the HTTP request
    url -- the endpoint URL
    """
    response = requests.get(url, params=query)
    logging.debug("Completed: %s", response.url)
    if response.status_code != 200:
        logging.error("Request failed: %s -> %s", response.status_code, query)
    else:
        logging.info("200 %s", query)
    return response.status_code


def build_delays(times):
    """Build a list of delays in milli-seconds from the times
    of each line in the log file

    times -- the list of time stamps loaded from the log file
    """
    delays = []
    for prev_t, cur_t in zip(times,times[1:]):
        delta = cur_t - prev_t
        delta_ms = delta.total_seconds() * 1000.0
        delays.append(delta_ms)
    return delays

def args_parser():
    """ Create a CLI argument parser
    """
    parser = argparse.ArgumentParser(prog = 'logreplay.py',
        description = 'A tool to replay a log file onto an HTTP endpoint as a series of queries. Requires Python 3.x.')
    parser.add_argument('log_file', metavar = 'LOG_FILE',
        help = "The path of the log file to replay.")
    parser.add_argument('target_params', metavar = 'TARGET_PARAMS',
        help = "The list of attributes from each query in the log file to use in replaying.")
    parser.add_argument('url', metavar = 'URL',
        help = "The URL of the HTPP endpoint.")
    parser.add_argument('--extra_params', required = False, default = '',
        help = "Extra parameters with a fixed value, given as a comma-separated list of key=value pairs.")
    parser.add_argument('--pass_delay', action="store_true",
        help = "Add the delay between queries from the log as an extra query parameter.")
    parser.add_argument('--use_delay', action="store_true",
        help = "During replaying, use for the delay between successive queries from the log file.")
    return parser

def main(args):
    """The main function

    args -- the command line arguments
    """
    log_file = args.log_file
    target_params = args.target_params.split(",")
    url = args.url
    extra_params = args.extra_params.split(",")
    pass_delay = args.pass_delay
    use_delay = args.use_delay

    lines = load_log(log_file)
    params = target_params
    params.extend(extra_params)
    logging.info("Loaded log file. Size: %s", len(lines))

    logging.info("Selected query parameters: %s", target_params)
    logging.info("Using extra query parameters: %s", extra_params)
    logging.info("All parameters: %s", params)
    logs = filter_logs(lines, target_params, extra_params, pass_delay)
    logging.info("Filtered logs. Size: %s", len(logs))

    send_queries(logs, url, use_delay)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    cli_parser = args_parser()
    args = cli_parser.parse_args()
    main(args)
