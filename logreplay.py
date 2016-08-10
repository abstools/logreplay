#!/usr/bin/python

from datetime import datetime
import logging
import re
import requests
import sys
import time

def load_log(log_file):
	lines = {}
	for line in open(log_file, 'r'):
		parts = line.split(" ")
		log_time = datetime.strptime(parts[0] + " " + parts[1], '%Y-%m-%d %H:%M:%S,%f')
		# Assume that the last part of a log line is the data part
		log_query = parts[-1]
		lines[log_time] = log_query
	return lines

def filter_logs(logs, target_params, extra_params):
	if len(target_params) == 0:
		return logs
	filtered_logs = {}
	for k, v in logs.iteritems():
		# val can be 'id&' or 'id=xxx&'
		filtered_values = [val for val in v.split("&") if val in target_params or val[:val.index('=')] in target_params]
		filtered_logs[k] = "&".join(filtered_values + extra_params)
	return filtered_logs

def send_queries(logs, url, query_path):
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
		if (len(delays) > 0):
			delay = delays.pop(0)
			logging.info("Waiting %s msec(s) for next query ...", delay)
			time.sleep(delay / 1000.0)

def send_query(query, url = "http://httpbin.org", path = "/get"):
	response = requests.get(url + path, params = query)
	logging.debug("Completed: %s", response.url)
	return response.status_code

def build_delays(times):
	t_0 = times[0]
	delays = []
	for t in times:
		delta = t - t_0
		delta_ms = delta.microseconds / 1000.0
		delays.append(delta_ms)
	# First query does not wait; assert delays[0] == 0
	delays.pop(0)
	return delays

if __name__ == "__main__":
	if (len(sys.argv) < 5):
		print "Usage: logreplay.py LOG_FILE TARGET_PARAMS EXTRA_PARAMS URL QUERY_PATH"
		sys.exit(1)

	log_file = sys.argv[1]
	target_params = sys.argv[2].split(",")
	extra_params = sys.argv[3].split(",")
	url = sys.argv[4]
	query_path = sys.argv[5]

	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
	
	lines = load_log(log_file)	
	logging.info("Loaded log file. Size: %s", len(lines))

	logging.info("Using extr query parameters: %s", extra_params)
	logging.info("Using target query parameters: %s", target_params)
	logs = filter_logs(lines, target_params, extra_params)
	logging.info("Filtered logs. Size: %s", len(logs))

	send_queries(logs, url, query_path)
