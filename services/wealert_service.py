from mysql.wealert_db import WealertGroupChatHistory
from services.service import BaseService

from sqlalchemy.orm import sessionmaker

import itchat
import json

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

        global wechat_responder
        wechat_responder = self
        self._logger.info('wealert service is initialized.')
        self.start()

    def run(self):
        """ Runs the itchat as a background service"""
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        itchat.run()

    def group_chat_receiver(self, msg):
        """ callback func to receive textual group chat
            :param msg: A dictionary contains various information of a message
        """
        print(json.dumps(msg))


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_chat_text_receiver(msg):
    """ callback func to receive textual group chat
        :param msg: A dictionary contains various information of a message
    """
    global wechat_responder
    wechat_responder.group_chat_receiver(msg)
    # return msg



def main():

    record = WealertChatHistory(content="this is a test wechat record")
    session = Session()
    session.add(record)
    session.commit()
    print('I\'m here')


if __name__ == '__main__':
    main()
