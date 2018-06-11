from wealert.data_model.database import session
from wealert.data_model.wealert import WealertGroupChat
from wealert.data_model.wealert import WealertRegularChat
from wealert.data_model.wealert import WealertGroupNewMember
import datetime
import logging


def _message_log_preprocessing(msg):
    """ Preprocesses the raw message to fit the log ouput"""
    return msg[:20].replace('\n', '')


def add_group_chat(
        owner_uin,
        owner_nickname,
        group_name,
        sender,
        textual_content,
        msg_created_time):
    """ callback func to receive textual group chat
        :param msg: A dictionary contains various information of a message
    """
    created_time = datetime.datetime.utcfromtimestamp(
        msg_created_time)

    logging.info(
            'Groupchat GroupName: {groupname} User: {user} '
            'UTC Time: {createtime} Text: {text}'.format(
                groupname=group_name,
                user=sender,
                createtime=created_time,
                text=textual_content))

    record = WealertGroupChat(
                owner_uin=owner_uin,
                owner_nickname=owner_nickname,
                group_name=group_name,
                sender=sender,
                content=textual_content,
                message_type='TEXT',
                message_time=created_time.strftime("%Y-%m-%d %H:%M:%S"))

    session.add(record)
    session.commit()


def add_regular_chat(
        owner_uin,
        owner_nickname,
        sender,
        receiver,
        textual_content,
        msg_created_time):
    """ callback func to receive textual regular chat
        :param msg: A dictionary contains various information of a message
    """
    created_time = datetime.datetime.utcfromtimestamp(
        msg_created_time)

    logging.info(
            'Regularchat: Sender: {sender} Receiver: {receiver} '
            'UTC TIme: {createtime} Text: {text}'.format(
                sender=sender,
                receiver=receiver,
                createtime=created_time,
                text=textual_content
            ))

    record = WealertRegularChat(
                owner_uin=owner_uin,
                owner_nickname=owner_nickname,
                sender=sender,
                receiver=receiver,
                content=textual_content,
                message_type='TEXT',
                message_time=created_time.strftime("%Y-%m-%d %H:%M:%S"))

    session.add(record)
    session.commit()


def add_group_new_member_log(
        owner_uin,
        owner_nickname,
        group_name,
        inviter,
        invitee,
        textual_content,
        msg_created_time):

    created_time = datetime.datetime.utcfromtimestamp(
        msg_created_time)

    record = WealertGroupNewMember(
                owner_uin=owner_uin,
                owner_nickname=owner_nickname,
                group_name=group_name,
                inviter=inviter,
                invitee=invitee,
                message_time=created_time.strftime(
                    "%Y-%m-%d %H:%M:%S"))
    session.add(record)
    session.commit()
