from py_pushover import _BaseManager


class LicenseManager(_BaseManager):
    def __init__(self, app_token, user_key=None, email=None):
        """

        """
        super().__init__(app_token, user_key=user_key)
        self._email = email

        if self._email is None and self._user_key is None:
            raise NotImplementedError  # todo: identify or create a relevant error
        raise NotImplementedError
