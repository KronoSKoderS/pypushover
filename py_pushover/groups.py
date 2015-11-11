"""
==============================================
groups - Group Management for the Pushover API
==============================================

This module defines functions and classes used for handling groups on the Pushover servers.  Users can be added,
removed, activated, or deactivated from a group.  Information can also be queried about the group.

Group Information and Renaming:
------------------

## Using the `GroupManager` class:

    >>> import py_pushover as py_po
    >>> gm = py_po.groups.GroupManager('app_token', 'group_key')
    >>> print(gm.info())

    You can also use the `group` property to query information on the group.  This is dynamically updated with every
    call to the group:

    >>> print(gm.group.name)
    >>> print(len(gm.group.users))
    >>> print(gm.group.users[0].device)

## Using the function call
    >>> print(py_po.groups.info('app_token', 'group_key'))

## Renaming the group

Using the GroupManager class
    >>> gm.rename('group name')
    >>> print(gm.group.name)

Using the function calls
    >>> py_po.groups.rename('app_token', 'group_key', 'group name')
    >>> print(py_po.groups.info('app_token', 'group_key')['name'])

User Management for a Group:
----------------------------

## Adding a user:

    >>> gm.add_user('user_key')
    >>> py_po.groups.add_user('app_token', 'group_key', 'user_key')

You can also add specifying information for the user:

    >>> gm.add_user('user_key',
    >>>     device='android',
    >>>     memo='Users android device')  # adds only device 'android' for user to group.  Attach a memo to the addition


## Removing a user:

Using the Class method:

    >>> gm.remove_user('user_key')

    You can also use the dynamic `group` property to select a user

        >>> gm.remove_user(gm.group.users[0].user_key)

Using the function call

    >>> py_po.groups.remove_user('app_token', 'group_key', 'user_key')

## Disable a user
Disabling a user doesn't remove them from the group, but disables any alerts sent to the group to be sent to them

Using the Class method call
    >>> gm.disable_user('user_key')

    You can also use the dynamic `group` property
        >>> gm.disable_user(gm.group.users[0].user_key)

Using the function call
    >>> py_po.groups.disable_user('app_token', 'group_key', 'user_key')

## Enable a user
Enabling a user does the exact opposite of the disable user.  An enabled user will receive messages sent to the group.

Using the Class method:

    >>> gm.enable_user('user_key')

    You can also use the dynamic `group` property:

        >>> gm.enable_user(gm.group.users[0].user_key)


Using the function call:

    >>> py_po.groups.enable_user('app_token', 'group_key', 'user_key')

"""

from py_pushover import BaseManager, base_url, send


_group_url = base_url + "groups/{group_key}"
_group_info_url = _group_url + ".json"
_group_add_user_url = _group_url + "/add_user.json"
_group_del_user_url = _group_url + "/delete_user.json"
_group_dis_user_url = _group_url + "/disable_user.json"
_group_ena_user_url = _group_url + "/enable_user.json"
_group_ren_url = _group_url + "/rename.json"


class _User(object):
    """
    User - Class object to represent a User associated with a group.

    This class is generated dynamically based on the response from the Pushover servers.
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k + '_key' if k == 'user' else k, v)


class _Group(object):
    """
    Group - Class object to represent a Group.

    This class is generated dynamically based on the response from the Pushover servers.
    """
    def __init__(self, **kwargs):
        self.users = None
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.users:
            self.users = [_User(**user) for user in self.users]


class GroupManager(BaseManager):
    """
    Manages the calls the groups API for Pushover, without having to supply and app token and group key everytime.

    Also enables to user to query current status of the group using the `group` property:

        >>> gm = GroupManager('app_token', 'group_key')
        >>> print(gm.group.name)  # prints the name of the group associated with 'group_key'
        >>> gm.rename('new name')
        >>> print(gm.group.name)  # prints 'new name'

    """

    def __init__(self, app_token, group_key):
        super(GroupManager, self).__init__(app_token, group_key=group_key)
        self.group = _Group(**self.info())

    def __update_group(self):
        self.group = _Group(**self.info())

    def info(self):
        """
        Fetches the group name and a list of users subscribed to the group.

        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = info(self._app_token, self._group_key)
        self.group = _Group(**self.latest_response_dict)
        return self.latest_response_dict

    def add_user(self, user, device=None, memo=None):
        """
        Adds the selected user to the group

        :param str user: the user id of the user to add
        :param str device: the associated device name (optional)
        :param str memo: memo (optional)
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = add_user(self._app_token, self._group_key, user, device=device, memo=memo)
        self.__update_group()
        return self.latest_response_dict

    def remove_user(self, user):
        """
        Removes the selected user from the group
        :param str user: the user id of the user to deleted
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = remove_user(self._app_token, self._group_key, user)
        self.__update_group()
        return self.latest_response_dict

    def disable_user(self, user):
        """
        Disables the user from receiving notifications sent to the group
        :param str user: the user id of the user to disable
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = disable_user(self._app_token, self._group_key, user)
        self.__update_group()
        return self.latest_response_dict

    def enable_user(self, user):
        """
        Enables the user to receive notifications sent to the group
        :param str user: the user id of the user to enable
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = enable_user(self._app_token, self._group_key, user)
        self.__update_group()
        return self.latest_response_dict

    def rename(self, name):
        """
        Renames the group
        :param str name: the name of the group to change to
        :return: A dictionary representing the json response.
        """

        self.latest_response_dict = rename(self._app_token, self._group_key, name)
        self.__update_group()
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
