import logging
import yaml
from wealert.services.wealert_service import Wealert

logger_format = '%(asctime)-30s %(levelname)-10s %(message)s'
formatter = logging.Formatter(logger_format)
hdlr = logging.FileHandler('./monitoring.log')
hdlr.setFormatter(formatter)

logging.basicConfig(format=logger_format)
logger = logging.getLogger('wealert')
logger.setLevel(logging.INFO)
logger.addHandler(hdlr)

if __name__ == '__main__':
    logger.info('the program is initialized.')

    with open('local_config.yaml', 'r') as fp:
        yamlconfig = yaml.load(fp.read())
    config = dict()
    config['logger'] = logger
    Wealert(config)
    import time
    while(True):
        time.sleep(1)
