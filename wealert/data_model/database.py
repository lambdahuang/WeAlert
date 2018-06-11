from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
        'mysql+pymysql://root:AHUTLAMDA@localhost:33433'
        '/wealert?charset=utf8mb4')

# declare base
Base = declarative_base()

# declare Session
Session = sessionmaker(engine)

# create session
session = Session()
