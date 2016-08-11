import logging

def apply_filter(value):
	return value

def apply_filter(value):
	s = value
	if value.index('=') > 0:
		s = value[value.index('=') + 1:]
	try:
		v = float(s)
		w = str(int(v) + 1)
		logging.info("%s -> %s", s , w)
		return w
	except:
		return value
