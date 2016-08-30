# logreplay

An experimental research tool to replay a log file as a series of queries onto an RESTful endpoint.

To run the tool:

```bash
$ python logreplay.py /path/log-file param1,param2 extra1=1,extra2=2 URL /QueryPath
```

in which:

* `paramN` is the name of parameter to extract from log file
* `extraX=Y` is an extra parameter key-value to send to the endpoint
* `URL` is the RESTful endpoint to receive the queries extracted from the log file; e.g. `http://httpbin.org`.
* `/QueryPath` is the endpoint receiving queries; e.g. `/get`. The sent query to the endpoint is currently hard-coded to be an HTTP `GET` request.
* The log file is assumed to have the following structure on every line:

```
DATE TIME [LEVEL EXTRA] [MESSAGE]
```
in which:

  * `DATE TIME` are in standard Python format `%Y-%m-%d %H:%M:%S,%f`.
  * The last *space-separated* part of each log line is considered as the *message*. The message may contain character `&` to denote standard HTTP query parameters.
  * All the log line elements in between, including `LEVEL` or others, are ignored.

## Requirements

* logreplay should be compatible with Python 2.7+.
* You need to have Python [requests][1] package:
```bash
$ sudo apt-get install python-pip
$ (sudo) pip install requests
```


## Parameter value transformations
Before logreplay fires a request to the HTTP endpoint, it is (optionally)
possible to apply transformations on selected attributes.
To use this, implement your own transformation function in the file
custom_filters.py and enable the filter by adding the function name
to the list of activated filters returned by the get_filters function
in the same file.

* The file example/custom_filters.py shows an example transformation,
to apply on the proctime attribute in the example/example.log log file.

[1]: https://pypi.python.org/pypi/requests
