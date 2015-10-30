import requests

base_url = "https://api.pushover.net/1/"


class BaseManager(object):

    def __init__(self, app_token, user_key=None, group_key=None):
        """
        Base class for the Push Over API
        :param string app_token: Application token generated from PushOver site
        :param string user_key: User key generated from PushOver site
        :param string group_key: Group key generated from PushOver site
        """
        self._app_token = app_token
        self._user_key = user_key
        self._group_key = group_key
        self.latest_response_dict = None


def send(url, data_out=None, get_method=False):
    if get_method:
        res = requests.get(url, params=data_out)
    else:
        res = requests.post(url, params=data_out)

    res.raise_for_status()
    return res.json()
