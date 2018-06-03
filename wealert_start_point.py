import logging
import optparse

import yaml

from services.wealert_service import Wealert

from sqlalchemy import *

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

    engine = create_engine(
        'mysql+pymysql://{user}:{pw}@{addr}:{port}/{dbname}'.format(
            user=yamlconfig['mysql_user'],
            pw=yamlconfig['mysql_password'],
            addr=yamlconfig['mysql_address'],
            port=yamlconfig['mysql_port'],
            dbname=yamlconfig['mysql_database']
        ),
        echo=True)


    config = dict()
    config['logger'] = logger
    config['db_engine'] = engine

    wealert = Wealert(config)


    import time
    while(True):
        time.sleep(1)
