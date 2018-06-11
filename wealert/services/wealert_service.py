from wealert.services.service import BaseService

from wealert.data_model.wealert import WealertGroupChat
from wealert.data_model.wealert import WealertRegularChat
from wealert.data_model.wealert import WealertGroupNewMember
from wealert.data_model.database import engine
from wealert.views.view import run_itchat


class Wealert(BaseService):
    """Kicks off the welalert service execution based on the itwechat responds.

    :param config: A dictionary with following keys
        :param logger:  The logger handle which will be used as an information
                        output.
    """
    def __init__(self, config):
        BaseService.__init__(self, config)
        self._logger = config['logger']

        WealertGroupChat.metadata.create_all(engine)
        WealertRegularChat.metadata.create_all(engine)
        WealertGroupNewMember.metadata.create_all(engine)
        self._logger.info('wealert service is initialized.')
        self.start()

    def run(self):
        """ Runs the itchat as a background service"""
        run_itchat()
