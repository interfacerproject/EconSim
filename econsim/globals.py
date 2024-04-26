DESIGNERS_ID_OFFSET = 0
PRODUCERS_ID_OFFSET = 100000

MIN_QUALITY = 1
MAX_QUALITY = 2
MIN_FEE = 1
MAX_FEE = 2
MIN_SUS = 1
MAX_SUS = 2


_debug = False

def set_debug():
    global _debug
    _debug = True

def get_debug():
    return _debug
