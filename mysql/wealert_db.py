from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

# declare base
Base = declarative_base()


class WealertGroupChatHistory(Base):
    """Group chat history"""

    __tablename__ = 'wechat_groupchat_records'
    id = Column(Integer, primary_key=True,autoincrement=True)
    owner_uin = Column(VARCHAR(length=255))  # owner uniqu wechat ID
    owner_nickname = Column(VARCHAR(length=255))
    group_name = Column(VARCHAR(length=255))
    sender = Column(VARCHAR(length=255))
    content = Column(TEXT)
    message_type = Column(VARCHAR(length=50))
    message_hash = Column(VARCHAR(length=255))  # if message is not textual content, than given the hash here
    message_time = Column(DATETIME)  # the UTC time of message creation.
    last_modified = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    Index('idx_ts', message_time)
    Index('idx_group', group_name)
    Index('idx_sender', sender)


class WealertRegularChatHistory(Base):
    """ Regular chat history"""

    __tablename__ = 'wechat_regularchat_records'
    id = Column(Integer, primary_key=True,autoincrement=True)
    owner_uin = Column(VARCHAR(length=255))  # owner uniqu wechat ID
    owner_nickname = Column(VARCHAR(length=255))
    sender = Column(VARCHAR(length=255))
    receiver = Column(VARCHAR(length=255))
    content = Column(TEXT)
    message_type = Column(VARCHAR(length=50))
    message_hash = Column(VARCHAR(length=255))  # if message is not textual content, than given the hash here
    message_time = Column(DATETIME)  # the UTC time of message creation.
    last_modified = Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    Index('idx_ts', message_time)
    Index('idx_sender', sender)

