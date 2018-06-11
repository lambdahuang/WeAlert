import itchat
from wealert.data_model.operations import add_group_chat
from wealert.data_model.operations import add_regular_chat


@itchat.msg_register(itchat.content.NOTE, isGroupChat=True)
def group_note_receiver(msg):
    """ callback func to receive note chat
        :param msg: A dictionary contains various information of a message
    """
    if u'邀请' in msg['Content'] or u'invited' in msg['Content']:
        str = msg['Content']
        pos_start = str.find('"')
        pos_end = str.find('"', pos_start+1)
        inviter = str[pos_start+1:pos_end]
        rpos_start = str.rfind('"')
        rpos_end = str.rfind('"', 0, rpos_start)
        invitee = str[(rpos_end+1): rpos_start]
        group_name = itchat.search_chatrooms(
            userName=msg['FromUserName'])['NickName']
        msg_created_time = msg['CreateTime']
        print(
                "@%s 欢迎来到本群[微笑]，感谢%s邀请。" %
                (invitee, inviter), itchat.search_chatrooms(
                userName=msg['FromUserName'])['NickName'])


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_chat_text_receiver(msg):
    """ callback func to receive textual group chat
        :param msg: A dictionary contains various information of a message
    """
    add_group_chat(
        owner_uin=owner_dict['Uin'],
        owner_nickname=owner_dict['NickName'],
        group_name=msg['User']['NickName'],
        sender=msg['ActualNickName'],
        textual_content=msg['Text'],
        msg_created_time=msg['CreateTime']
    )


@itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
def regular_chat_text_receiver(msg):
    """ callback func to receive textual regular chat
        :param msg: A dictionary contains various information of a message
    """
    add_regular_chat(
        owner_uin=owner_dict['Uin'],
        owner_nickname=owner_dict['NickName'],
        sender=itchat.search_friends(
            userName=msg['FromUserName'])['NickName'],
        receiver=itchat.search_friends(
            userName=msg['ToUserName'])['NickName'],
        textual_content=msg['Text'],
        msg_created_time=msg['CreateTime']
    )


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


def run_itchat():
    global owner_dict
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    owner_dict = itchat.search_friends()
    itchat.run()
