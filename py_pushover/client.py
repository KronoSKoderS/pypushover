from py_pushover import _BaseManager


class ClientManager(_BaseManager):
    def __init__(self, app_token):
        super().__init__(app_token)
        raise NotImplementedError
