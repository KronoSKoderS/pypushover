from pypushover import BaseManager, BASE_URL, send

_VERIFY_URL = BASE_URL + "/users/validate.json"


class VerificationManager(BaseManager):
    def __init__(self, app_token):
        super(VerificationManager, self).__init__(app_token)

    def verify_user(self, user_id, device=None):
        """
        Verifies whether a userID is a valid ID

        :param device:
        :param user_id:
        :return :
        """

        return verify_user(self._app_token, user_id, device=device)

    def verify_group(self, group_id):
        """
        Verifies whether a groupID is a valid ID

        :param group_id:
        :return :
        """

        return verify_group(self._app_token, group_id)


def verify_user(app_token, user, device=None):
    """
    Verifies whether a userID is a valid ID if device is given, then the user/device pair is verified.

    :param device:
    :param app_token: the application token
    :param user: the user id
    :return :
    """
    param_data = {
        'token': app_token,
        'user': user,
    }

    res = send(_VERIFY_URL, param_data)
    valid = res['status'] == 1
    valid &= res['group'] == 0

    if not device:
        valid &= device in res['devices']

    return valid


def verify_group(app_token, group_id):
    """
    Verifies whether a groupID is a valid ID.

    :param app_token
    :param group_id:
    :return :
    """
    param_data = {
        'token': app_token,
        'user': group_id,
    }

    res = send(_VERIFY_URL, param_data)
    valid = res['status'] == 1
    valid &= res['group'] == 1

    return valid
