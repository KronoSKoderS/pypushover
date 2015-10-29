from py_pushover import BaseManager, base_url, send

_group_url = base_url + "groups/{group_key}"
_group_info_url = _group_url + ".json"
_group_add_user_url = _group_url + "/add_user.json"
_group_del_user_url = _group_url + "/delete_user.json"
_group_dis_user_url = _group_url + "/disable_user.json"
_group_ena_user_url = _group_url + "/enable_user.json"
_group_ren_url = _group_url + "/rename.json"

class GroupManager(BaseManager):
    def __init__(self, app_token, group_key):
        super(GroupManager, self).__init__(app_token, group_key=group_key)


    def info(self):
        """
        Fetches the group name and a list of users subscribed to the group.

        :param str group_key: The key identifying the group.  If none provided the
        classes group key is used.
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = info(self._app_token, self._group_key)
        return self.latest_response_dict

    def group_add_user(self, user, group_key=None, device=None, memo=None):
        """

        required params: user
        optional params: device, memo
        :return:
        """

        group = None

        if group_key:
            group = group_key
        elif self._group_key:
            group = self._group_key
        else:
            raise ValueError("A group key must be supplied")

        param_data = {
            'user': user
        }

        if device:
            param_data['device'] = device
        if memo:
            param_data['memo'] = memo

        self._send(self._group_add_user_url.format(group_key=group), param_data)

    def group_remove_user(self, user, group_key=None):
        """

        required params: user
        :return:
        """

        if group_key:
            group = group_key
        elif self._group_key:
            group = self._group_key
        else:
            raise ValueError("A group key must be supplied")

        param_data = {
            'user': user
        }

        self._send(self._group_del_user_url.format(group_key=group), param_data)

    def group_disable_user(self, user, group_key=None):
        """

        required params: user
        :return:
        """

        if group_key:
            group = group_key
        elif self._group_key:
            group = self._group_key
        else:
            raise ValueError("A group key must be supplied")

        param_data = {
            'user': user
        }

        self._send(self._group_dis_user_url.format(group_key=group), param_data)

    def group_enable_user(self, user, group_key=None):
        """

        required params: token, user
        :return:
        """

        group = None

        if group_key:
            group = group_key
        elif self._group_key:
            group = self._group_key
        else:
            raise ValueError("A group key must be supplied")

        param_data = {
            'user': user
        }

        self._send(self._group_ena_user_url.format(group_key=group), param_data)

    def group_rename(self, name, group_key=None):
        """

        required params: token, name
        :return:
        """

        if group_key:
            group = group_key
        elif self._group_key:
            group = self._group_key
        else:
            raise ValueError("A group key must be supplied")

        param_data = {
            'name': name
        }

        self._send(self._group_ren_url.format(group_key=group), param_data)

def info(app_token, group):
    return send(_group_info_url.format(group_key=group), params={'token':app_token}, get_method=True)

def add_user(app_token, group, user):
    raise NotImplementedError

def remove_user(app_token, group, user):
    raise NotImplementedError

def disable_user(app_token, group, user):
    raise NotImplementedError

def enable_user(app_token, group, user):
    raise NotImplementedError

def rename(app_token, group, user)
    raise NotImplementedError
