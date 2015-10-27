from py_pushover import _BaseManager


class SubscriptionManager(_BaseManager):
    def __init__(self, app_token, user_key, sub_code):
        super().__init__(app_token, user_key=user_key)
        self._sub_code = sub_code
        raise NotImplementedError

