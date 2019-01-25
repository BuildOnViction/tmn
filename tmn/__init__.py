import logging

__version__ = '0.5.0'

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger = logging.getLogger('tmn')
logger.addHandler(handler)
logger.setLevel('CRITICAL')
