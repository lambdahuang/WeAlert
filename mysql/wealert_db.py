from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create sql engine
engine = create_engine(
        'mysql+pymysql://root:AHUTLAMDA@localhost:33433/wealert',
        echo=True)

# declare base
Base = declarative_base()

# initialize session
Session = sessionmaker(bind=engine)


class WealertChatHistory(Base):
    """wechat chat history

    """
    __tablename__ = 'wechat_chat_records'
    id = Column(Integer, primary_key=True,autoincrement=True)
    content = Column(TEXT)
    time_stamp = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    Index('idx_ts', 'time_stamp')
