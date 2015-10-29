from py_pushover import BaseManager, base_url


class GroupManager(BaseManager):
    def __init__(self, app_token, group_key):
        super(GroupManager, self).__init__(app_token, group_key=group_key)
        self._group_url = base_url + "groups/{group_key}"
        self._group_info_url = self._group_url + ".json"
        self._group_add_user_url = self._group_url + "/add_user.json"
        self._group_del_user_url = self._group_url + "/delete_user.json"
        self._group_dis_user_url = self._group_url + "/disable_user.json"
        self._group_ena_user_url = self._group_url + "/enable_user.json"
        self._group_ren_url = self._group_url + "/rename.json"

    def group_info(self, group_key=None):
        """
        Fetches the group name and a list of users subscribed to the group.

        :param str group_key: The key identifying the group.  If none provided the
        classes group key is used.
        :return: A dictionary representing the json response.
        """
        if group_key:
            group = group_key
        elif self._group_key:
            group = self._group_key
        else:
            raise ValueError("A group key must be supplied")

        self._send(self._group_info_url.format(group_key=group), get_method=True)
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

