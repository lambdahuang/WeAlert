from threading import Thread


class BaseService(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.deamon = True

    def run(self):
        raise NotimplementedError
