import logging
import logging.handlers

LOG_FILENAME = 'data_tracker.log'

logger = logging.getLogger('DataTracker')
logger.setLevel(logging.INFO)


handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1000000000,
    backupCount=5)

formatter = logging.Formatter('{asctime}:{name}:{levelname:8s}:{message}', style='{')
handler.setFormatter(formatter)

logger.addHandler(handler)