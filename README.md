# logreplay

An experimental research tool to replay a log file as a series of queries onto an RESTful endpoint with a lot of assumptions and conventions.

To run the tool:

```bash
$ python logreplay.py /path/log-file param1,param2 extra1=1,extra2=2 URL /QueryPath
```

in which:

* `paramN` is the name of parameter to extract from log file
* `extraX=Y` is an extra parameter key-value to send to the endpoint
* `URL` is the RESTful endpoint to receive the queries extracted from the log file; e.g. `http://httpbin.org`.
* `/QueryPath` is the endpoint receiving queries; e.g. `/get`
* The log file is assumed to have the following structure on every line:

```
DATE TIME [LEVEL EXTRA] [MESSAGE]
```
in which:

  * `DATE TIME` are in standard Python format `%Y-%m-%d %H:%M:%S,%f`.
  * The last *space-separated* part of each log line is considered as the *message*. The message may contain character `&` to denote standard HTTP query parameters.
  * All the log line elements in between, including `LEVEL` or others, are ignored.

