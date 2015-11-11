from py_pushover import BaseManager, base_url, send

_group_url = base_url + "groups/{group_key}"
_group_info_url = _group_url + ".json"
_group_add_user_url = _group_url + "/add_user.json"
_group_del_user_url = _group_url + "/delete_user.json"
_group_dis_user_url = _group_url + "/disable_user.json"
_group_ena_user_url = _group_url + "/enable_user.json"
_group_ren_url = _group_url + "/rename.json"


class GroupManager(BaseManager):
    """
    Manages the calls the groups API for Pushover, without having to supply and app token and group key everytime.
    """
    def __init__(self, app_token, group_key):
        super(GroupManager, self).__init__(app_token, group_key=group_key)

    def info(self):
        """
        Fetches the group name and a list of users subscribed to the group.

        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = info(self._app_token, self._group_key)
        return self.latest_response_dict

    def group_add_user(self, user, device=None, memo=None):
        """
        Adds the selected user to the group

        :param str user: the user id of the user to add
        :param str device: the associated device name (optional)
        :param str memo: memo (optional)
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = add_user(self._app_token, self._group_key, user, device=device, memo=memo)
        return self.latest_response_dict

    def group_remove_user(self, user):
        """
        Removes the selected user from the group
        :param str user: the user id of the user to deleted
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = remove_user(self._app_token, self._group_key, user)
        return self.latest_response_dict

    def group_disable_user(self, user):
        """
        Disables the user from receiving notifications sent to the group
        :param str user: the user id of the user to disable
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = disable_user(self._app_token, self._group_key, user)
        return self.latest_response_dict

    def group_enable_user(self, user):
        """
        Enables the user to receive notifications sent to the group
        :param str user: the user id of the user to enable
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = enable_user(self._app_token, self._group_key, user)
        return self.latest_response_dict

    def group_rename(self, name):
        """
        Renames the group
        :param str name: the name of the group to change to
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = rename(self._app_token, self._group_key, name)
        return self.latest_response_dict


def info(app_token, group):
    """
    Fetches the group name and a list of users subscribed to the group.

    :param str app_token: your applications token
    :param str group: the group id to return info on
    :return: A dictionary representing the json response.
    """
    param_data = {
        'token': app_token,
    }

    return send(_group_info_url.format(group_key=group), param_data, get_method=True)


def add_user(app_token, group, user, device=None, memo=None):
    """
    Adds the selected user to the group

    :param str app_token: your applications token
    :param str group: the group id
    :param str user: the user id of the user to add
    :param str device: the associated device name (optional)
    :param str memo: memo (optional)
    :return: A dictionary representing the json response.
    """

    param_data = {
        'token': app_token,
        'user': user
    }

    if device:
        param_data['device'] = device
    if memo:
        param_data['memo'] = memo

    return send(_group_add_user_url.format(group_key=group), param_data)


def remove_user(app_token, group, user):
    """
    Removes the selected user from the group
    :param str app_token: your applications token
    :param str group: the group id
    :param str user: the user id of the user to deleted
    :return: A dictionary representing the json response.
    """

    param_data = {
        'token': app_token,
        'user': user
    }

    return send(_group_del_user_url.format(group_key=group), param_data)


def disable_user(app_token, group, user):
    """
    Disables the user from receiving notifications sent to the group
    :param str app_token: your applications token
    :param str group: the group id
    :param str user: the user id of the user to disable
    :return: A dictionary representing the json response.
    """

    param_data = {
        'token': app_token,
        'user': user
    }

    return send(_group_dis_user_url.format(group_key=group), param_data)


def enable_user(app_token, group, user):
    """
    Enables the user to receive notifications sent to the group
    :param str app_token: your applications token
    :param str group: the group id
    :param str user: the user id of the user to enable
    :return: A dictionary representing the json response.
    """
    param_data = {
        'token': app_token,
        'user': user
    }

    return send(_group_ena_user_url.format(group_key=group), param_data)


def rename(app_token, group, name):
    """
    Renames the group
    :param str app_token: your applications token
    :param str group: the group id
    :param str name: the name of the group to change to
    :return: A dictionary representing the json response.
    """

    param_data = {
        'token': app_token,
        'name': name
    }

    return send(_group_ren_url.format(group_key=group), param_data)
