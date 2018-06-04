from mysql.wealert_db import (
        WealertGroupChatHistory,
        WealertRegularChatHistory,
        WealertGroupNewMemberHistory)

from services.service import BaseService

from sqlalchemy.orm import sessionmaker

import itchat
import json

import datetime


class Wealert(BaseService):
    """Kicks off the welalert service execution based on the itwechat responds.

    :param config: A dictionary with following keys
        :param logger:  The logger handle which will be used as an information
                        output.
    """
    def __init__(self, config):
        BaseService.__init__(self, config)
        self._logger = config['logger']
        self._db_engine = config['db_engine']
        self._session = sessionmaker(bind=self._db_engine)

        WealertGroupChatHistory.metadata.create_all(self._db_engine)
        WealertRegularChatHistory.metadata.create_all(self._db_engine)
        WealertGroupNewMemberHistory.metadata.create_all(self._db_engine)

        global wechat_responder
        wechat_responder = self
        self._logger.info('wealert service is initialized.')
        self.start()

    def run(self):
        """ Runs the itchat as a background service"""
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        self._owner_dict = itchat.search_friends()
        self._uin = self._owner_dict['Uin']
        self._nickname = self._owner_dict['NickName']
        itchat.run()

    def _message_log_preprocessing(self, msg):
        """ Preprocesses the raw message to fit the log ouput"""
        return msg[:20].replace('\n', '')

    def group_chat_receiver(self, msg):
        """ callback func to receive textual group chat
            :param msg: A dictionary contains various information of a message
        """
        group_name = msg['User']['NickName']
        sender = msg['ActualNickName']
        created_time = datetime.datetime.utcfromtimestamp(
             msg['CreateTime'])
        textual_content = msg['Text']

        self._logger.info(
                'Groupchat GroupName: {groupname} User: {user} '
                'UTC Time: {createtime} Text: {text}'.format(
                    groupname=group_name,
                    user=sender,
                    createtime=created_time,
                    text=textual_content))

        record = WealertGroupChatHistory(
                    owner_uin=self._uin,
                    owner_nickname=self._nickname,
                    group_name=group_name,
                    sender=sender,
                    content=textual_content,
                    message_type='TEXT',
                    message_time=created_time.strftime("%Y-%m-%d %H:%M:%S"))

        session = self._session()
        session.add(record)
        session.commit()

    def regular_chat_receiver(self, msg):
        """ callback func to receive textual regular chat
            :param msg: A dictionary contains various information of a message
        """
        sender = itchat.search_friends(
                userName=msg['FromUserName'])['NickName']
        receiver = itchat.search_friends(
                userName=msg['ToUserName'])['NickName']

        created_time = datetime.datetime.utcfromtimestamp(
            msg['CreateTime'])
        textual_content = msg['Text']

        self._logger.info(
                'Regularchat: Sender: {sender} Receiver: {receiver} '
                'UTC TIme: {createtime} Text: {text}'.format(
                    sender=sender,
                    receiver=receiver,
                    createtime=created_time,
                    text=textual_content
                ))

        record = WealertRegularChatHistory(
                    owner_uin=self._uin,
                    owner_nickname=self._nickname,
                    sender=sender,
                    receiver=receiver,
                    content=textual_content,
                    message_type='TEXT',
                    message_time=created_time.strftime("%Y-%m-%d %H:%M:%S"))

        session = self._session()
        session.add(record)
        session.commit()

    def group_note_receiver(self, msg):
        """ Handle group notes such as the notification of new group member.
        """
        if u'邀请' in msg['Content'] or u'invited' in msg['Content']:
            str = msg['Content']
            pos_start = str.find('"')
            pos_end = str.find('"', pos_start+1)
            inviter = str[pos_start+1:pos_end]
            rpos_start = str.rfind('"')
            rpos_end = str.rfind('"', 0, rpos_start)
            invitee = str[(rpos_end+1): rpos_start]
            print(
                "@%s 欢迎来到本群[微笑]，感谢%s邀请。" %
                (invitee, inviter), itchat.search_chatrooms(
                userName=msg['FromUserName'])['NickName'])

            group_name = itchat.search_chatrooms(
                userName=msg['FromUserName'])['NickName']

            created_time = datetime.datetime.utcfromtimestamp(
                msg['CreateTime'])

            record = WealertGroupNewMemberHistory(
                        owner_uin=self._uin,
                        owner_nickname=self._nickname,
                        group_name = group_name,
                        inviter=inviter,
                        invitee=invitee,
                        message_time=created_time.strftime("%Y-%m-%d %H:%M:%S"))

            session = self._session()
            session.add(record)
            session.commit()


"""
@itchat.msg_register(itchat.content.SYSTEM)
def get_uin(msg):
    if msg['SystemInfo'] != 'uins': return
    ins = itchat.instanceList[0]
    fullContact = ins.memberList + ins.chatroomList + ins.mpList
    print('** Uin Updated **')
    print(json.dumps(msg))
    for username in msg['Text']:
        member = itchat.utils.search_dict_list(
            fullContact, 'UserName', username)
        print(('[SYSTEM] %s: %s' % (
            member.get('NickName', ''), member['Uin']))
            .encode(sys.stdin.encoding, 'replace'))
"""

@itchat.msg_register(itchat.content.NOTE, isGroupChat=True)
def group_note_receiver(msg):
    """ callback func to receive note chat
        :param msg: A dictionary contains various information of a message
    """
    wechat_responder.group_note_receiver(msg)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_chat_text_receiver(msg):
    """ callback func to receive textual group chat
        :param msg: A dictionary contains various information of a message
    """
    global wechat_responder
    wechat_responder.group_chat_receiver(msg)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
def regular_chat_text_receiver(msg):
    """ callback func to receive textual regular chat
        :param msg: A dictionary contains various information of a message
    """
    global wechat_responder
    wechat_responder.regular_chat_receiver(msg)


def main():

    record = WealertChatHistory(content="this is a test wechat record")
    session = Session()
    session.add(record)
    session.commit()
    print('I\'m here')


if __name__ == '__main__':
    main()
