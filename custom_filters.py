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

# def proctime_filter(value):
#     """An example filter that converts a proctime attribute
#     in seconds (of type float) to milliseconds (integer).

#     value -- the 'proctime=val' pair whose val component is transformed 
#     """
#     key = "proctime"
#     try:
#         idx = value.index(key + '=')
#         val = float(value[idx + len(key) + 1:])
#         new_val = str(int(val*1000))
#         final_key_value = key + "=" + new_val
#         return final_key_value
#     except:
#         # Ignore everything, just return the original value
#         return value

def get_filters():
    """The list of filter functions to apply on a value."""

    return [identity_filter]
#     return [proctime_filter, identity_filter]
