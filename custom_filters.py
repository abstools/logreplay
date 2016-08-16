"""
The Python script file that contains all
custom filter functions.
"""

def apply_filter(value):
    """A do-nothing custom filter that returns
	the value of the input as-is.

	value -- the value to be filtered
	"""
    return value

# def apply_filter(value):
# 	"""A custom filter that converts a double value
# 	to an integer value.

# 	value -- the value to filter that can be as 'key=value'
# 	"""
# 	key = ""
# 	val = value
# 	idx = value.index('=')
# 	is_key_value = idx > 0
# 	if is_key_value:
# 		key = value[:idx]
# 		val = value[idx + 1:]
# 	try:
# 		v = float(val)
# 		final_val = str(int(v) + 1)
# 		final_key_value = key + "=" + final_val if is_key_value else final_val
# 		logging.debug("%s -> %s", value , final_key_value)
# 		return final_key_value
# 	except:
# 		# Ignore everything, just return the original value
# 		return value
