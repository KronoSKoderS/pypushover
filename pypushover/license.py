from pypushover import BaseManager, send, BASE_URL

_ASSIGN_URL = BASE_URL + "licenses/assign.json"


class LicenseManager(BaseManager):
    def __init__(self, app_token, user_key=None, email=None):
        """

        """
        super().__init__(app_token, user_key=user_key)
        self._email = email

        if self._email is None and self._user_key is None:
            raise ValueError("An email or user_key is required")

        raise NotImplementedError

    def assign(self, os=None):
        assign_license(self._app_token, user=self._user_key, email=self._email, os=os)


def assign_license(token, user=None, email=None, os=None):
    """

    Args:
        token:
        user:
        email:
        os:

    Returns:

    """
    if not(user) and not(email):
        raise ValueError("An email or user_key is required")

    params = {
        'token':token
    }

    # if both user key and email are sent, we prefer the user key
    if user:
        params['user'] = user
    else:
        params['email'] = email

    if os:
        params['os'] = os

    send(_ASSIGN_URL, data_out=params)
