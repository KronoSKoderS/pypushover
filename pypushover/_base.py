import requests
try:
    from json import JSONDecodeError as decode_error
except ImportError as e:
    decode_error = ValueError

base_url = "https://api.pushover.net/1/"


class BaseManager(object):

    def __init__(self, app_token, user_key=None, group_key=None):
        """
        Base class for the Pushover API
        :param string app_token: Application token generated from PushOver site
        :param string user_key: User key generated from PushOver site
        :param string group_key: Group key generated from PushOver site
        """
        self._app_token = app_token
        self._user_key = user_key
        self._group_key = group_key
        self.latest_response_dict = None


class PushoverError(Exception):
    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors

    def __str__(self):
        return repr(self.message)


def send(url, data_out=None, get_method=False):
    """
    Sends a request to the selected url with the payload `data_out`.  Set `get_method` to True to send as a GET request.
    Default request is a POST.

    :param str url: url to send the request to
    :param dict data_out: payload data to send
    :param bool get_method: True = GET request; False = POST request (default)
    :return dict: a dictionary with the json results of the request.
    """
    if get_method:
        res = requests.get(url, params=data_out)
    else:
        res = requests.post(url, params=data_out)

    try:
        ret_dict = res.json()
        if ret_dict['status'] == 0:
            raise PushoverError(ret_dict['errors'])

        return ret_dict

    except decode_error:
        res.raise_for_status()


