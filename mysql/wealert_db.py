from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# declare base
Base = declarative_base()

class WealertGroupChatHistory(Base):
    """wechat chat history

    """
    __tablename__ = 'wechat_groupchat_records'
    id = Column(Integer, primary_key=True,autoincrement=True)
    group_name = Column(VARCHAR(length=50))
    sender = Column(VARCHAR(length=50))
    content = Column(TEXT)
    time_stamp = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    Index('idx_ts', 'time_stamp')
