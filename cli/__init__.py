import logging

logging_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=logging_fmt, level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)
