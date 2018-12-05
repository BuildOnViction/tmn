import logging

__version__ = '0.4.2'

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger = logging.getLogger('tmn')
logger.addHandler(handler)
logger.setLevel('CRITICAL')
