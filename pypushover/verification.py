__all__ = ('VerificationManager', 'verify_user', 'verify_group')

from pypushover import BaseManager, base_url, send

verify_url = base_url + "/users/validate.json"


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

    if device:
        param_data['device'] = device

    return send(verify_url, param_data)['status'] == 1  # An HTTPError will be raised if invalid


def verify_group(app_token, group_id):
    """
    Verifies whether a groupID is a valid ID.

    :param app_token
    :param group_id:
    :return :
    """
    return verify_user(app_token, group_id)
