from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = Noen

# declare base
Base = declarative_base()

# declare Session
Session = sessionmaker(engine)

# create session
session = Session()


def create_engine(yamlconfig):
    # create engine
    global engine
    engine = create_engine(
        'mysql+pymysql://{user}:{pw}@{addr}:{port}/{dbname}?charset=utf8mb4'.
        format(
            user=yamlconfig['mysql_user'],
            pw=yamlconfig['mysql_password'],
            addr=yamlconfig['mysql_address'],
            port=yamlconfig['mysql_port'],
            dbname=yamlconfig['mysql_database']
        ),
        echo=True)
