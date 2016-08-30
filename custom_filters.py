"""
The Python script file that contains all
custom filter functions.
"""

def identity_filter(value):
    """A do-nothing custom filter that returns
	the value of the input as-is.

	value -- the value to be filtered
	"""
    return value

def get_filters():
    """The list of filter functions to apply on a value."""

    return [identity_filter]
