from py_pushover import BaseManager


class ClientManager(BaseManager):
    def __init__(self, app_token):
        super().__init__(app_token)
        raise NotImplementedError
