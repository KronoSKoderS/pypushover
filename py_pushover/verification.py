from py_pushover import BaseManager, base_url, send

verify_url = base_url + "/users/validate.json"


class VerificationManager(BaseManager):
    def __init__(self, app_token):
        super(VerificationManager, self).__init__(app_token)

    def verify_user(self, user_id, device=None):
        """
        Validates whether a userID is a valid id and returns a Boolean as a result

        :param user_id:
        :return bool:
        """

        return verify_user(self._app_token, user_id, device=device)

    def verify_group(self, group_id, device=None):
        """
        Validates whether a groupID is a valid ID and returns a Boolean as a result

        :param group_id:
        :return bool:
        """

        return verify_group(self._app_token, group_id, device=device)


def verify_user(app_token, user, device=None):
    return verify_group(app_token, user, device)


def verify_group(app_token, group_id, device=None):

    param_data = {
        'token': app_token,
        'user': group_id,
    }

    if device:
        param_data['device'] = device

    return send(verify_url, param_data)['status'] == 1  # An HTTPError will be raised if invalid
