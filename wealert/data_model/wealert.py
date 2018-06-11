from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import VARCHAR
from sqlalchemy import DATETIME
from sqlalchemy import TIMESTAMP
from sqlalchemy import TEXT
from sqlalchemy import Index
from sqlalchemy import text
from wealert.database import Base


class WealertGroupChat(Base):
    """Group chat history"""

    __tablename__ = 'wechat_groupchat_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_uin = Column(VARCHAR(length=255))  # owner uniqu wechat ID
    owner_nickname = Column(VARCHAR(length=255))
    group_name = Column(VARCHAR(length=255))
    sender = Column(VARCHAR(length=255))
    content = Column(TEXT)
    message_type = Column(VARCHAR(length=50))
    # if message is not textual content, than given the hash here
    message_hash = Column(VARCHAR(length=255))
    message_time = Column(DATETIME)  # the UTC time of message creation.
    last_modified = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Index('idx_ts', message_time)
    Index('idx_group', group_name)
    Index('idx_sender', sender)


class WealertRegularChat(Base):
    """ Regular chat history"""

    __tablename__ = 'wechat_regularchat_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_uin = Column(VARCHAR(length=255))  # owner uniqu wechat ID
    owner_nickname = Column(VARCHAR(length=255))
    sender = Column(VARCHAR(length=255))
    receiver = Column(VARCHAR(length=255))
    content = Column(TEXT)
    message_type = Column(VARCHAR(length=50))
    # if message is not textual content, than given the hash here
    message_hash = Column(VARCHAR(length=255))
    message_time = Column(DATETIME)  # the UTC time of message creation.
    last_modified = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Index('idx_ts', message_time)
    Index('idx_sender', sender)


class WealertGroupNewMember(Base):
    """ Group newly added member history"""

    __tablename__ = 'wechat_group_new_member_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_uin = Column(VARCHAR(length=255))  # owner uniqu wechat ID
    owner_nickname = Column(VARCHAR(length=255))
    group_name = Column(VARCHAR(length=255))
    inviter = Column(VARCHAR(length=255))
    invitee = Column(VARCHAR(length=255))
    # if message is not textual content, than given the hash here
    message_hash = Column(VARCHAR(length=255))
    message_time = Column(DATETIME)  # the UTC time of message creation.
    last_modified = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    Index('idx_ts', message_time)
    Index('idx_group_name', group_name)
    Index('idx_inviter', inviter)
    Index('idx_invitee', invitee)
