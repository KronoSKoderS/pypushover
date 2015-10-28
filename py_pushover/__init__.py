import requests

from py_pushover.Constants import PRIORITIES, SOUNDS


__all__ = ['PRIORITIES', 'SOUNDS', 'client', 'groups', 'license', 'message', 'subscription', 'verification']

_base_url = "https://api.pushover.net/1/"


class _BaseManager(object):

    _api_version = 1

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

    def _send(self, url, data_out=None, check_response=True, get_method=False):
        """
        Sends a formatted request to the supplied url.  If data_out is present, then the data is encoded and sent as
        well.  A check_response value of False the HTTP response code is checked.  A customized HTTPError is raised if
        an error is detected.

        :param string url: url of the site to send the request to (http://www.site.com)
        :param dict data_out: data to be encoded with the url (?token=<app_token>&user=<user_id>)
        :param bool check_response: check http response and raise exception if an error is detected
        """
        if not data_out:
            data_out = {
                'token': self._app_token
            }
        else:
            data_out['token'] = self._app_token

        self._latest_response = _send(url, data_out=data_out, get_method=get_method)
        self.latest_response_dict = self._latest_response.json()

        if check_response:
            self._response_check()

    def _response_check(self):
        """
        Checks the HTTP Response code and raises a customized HTTPError based on the Pushover 'errors' response.
        """

        if self._latest_response.status_code == 200:
            return

        elif 400 <= self._latest_response.status_code < 500:
            error = self.latest_response_dict['errors']
            raise requests.HTTPError(error)

        else:
            raise requests.HTTPError()


def _send(url, data_out=None, get_method=False):
    if get_method:
        return requests.get(url, params=data_out).json()
    else:
        return requests.post(url, params=data_out).json()