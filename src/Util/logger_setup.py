# logger set up for logging

import logging

logging.basicConfig(filename='open_controller_log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname):%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('log')
#logger.info('Application started and logging started')