import logging

def apply_filter(value):
	return value

def apply_filter(value):
	key = ""
	val = value
	idx = value.index('=')
	is_key_value = idx > 0
	if is_key_value:
		key = value[:idx]
		val = value[idx + 1:]
	try:
		v = float(val)
		final_val = str(int(v) + 1)
		final_key_value = key + "=" + final_val if is_key_value else final_val
		logging.debug("%s -> %s", value , final_key_value)
		return final_key_value
	except:
		# Ignore everything, just return the original value
		return value
