import json

try:  # Python 3
    import urllib.request as urllib_request
    from urllib.parse import urlencode as urllib_encode
    PYTHON_VER = 3

except ImportError:  # Python 2
    import urllib2 as urllib_request
    from urllib import urlencode as urllib_encode
    PYTHON_VER = 2

_MAX_EXPIRE = 86400
_MIN_RETRY = 30


class Sounds(object):
    """
    Sounds - Collection of Push Notification sounds.

    This is to be used with the 'sounds' argument of the PushOverManager.push_notification method.

    see also: https://pushover.net/api#sounds
    """
    Short_Pushover = 'pushover'
    Short_Bike = 'bike'
    Short_Bugle = 'bugle'
    Short_Cash_Register = 'cashregister'
    Short_Classical = 'classical'
    Short_Cosmic = 'cosmic'
    Short_Gamelan = 'gamelan'
    Short_Incoming = 'incoming'
    Short_Intermission = 'intermission'
    Short_Magic = 'magic'
    Short_Mechanical = 'mechanical'
    Short_Piano_Bar = 'pianobar'
    Short_Siren = 'siren'
    Short_Space_Alarm = 'spacealarm'
    Short_Tug_Boat = 'tugboat'
    Long_Alien_Alarm = 'alien'
    Long_Climb = 'climb'
    Long_Persistent = 'persistent'
    Long_Pushover_Echo = 'echo'
    Long_Up_Down = 'updown'
    Silent = 'none'


class Priority(object):
    """
    Priority - Collection of Priorities.

    This is to be used with the 'priority' arguemnt of the PushOverManager.push_notification method.

    see also: https://pushover.net/api#priority
    """
    Lowest = -2     # no notification/alert
    Low = -1        # quiet notification
    Normal = 0      # normal
    High = 1        # high-priority (bypass user's quiet hours)
    Emergency = 2   # require confirmation from the user (bypass users's quiet hours)


class PushOverManager(object):
    """
    Push Over Manager - Class for interfacing with the Pushover API.

    Properties:
    -----------
    latest_response

    Methods:
    --------
    push_notification - pushes a notification to a device, user or group.
    check_receipt
    cancel_retries
    validate_user
    validate_group
    group_info
    group_add_user
    group_remove_user
    group_disable_user
    group_enable_user
    group_rename
    """
    _push_url = "https://api.pushover.net/1/messages.json"
    _validate_url = "https://api.pushover.net/1/users/validate.json"
    _receipt_url = "https://api.pushover.net/1/receipts/{receipt}.json?token={app_token}"
    _cancel_receipt_url = "https://api.pushover.net/1/receipts/{receipt}/cancel.json"
    _group_url = "https://api.pushover.net/1/groups/{group_key}"
    _group_info_url = _group_url + ".json"
    _group_add_user_url = _group_url + "/add_user.json"
    _group_del_user_url = _group_url + "/delete_user.json"
    _group_dis_user_url = _group_url + "/disable_user.json"
    _group_ena_user_url = _group_url + "/enable_user.json"
    _group_ren_url = _group_url + "/rename.json"

    def __init__(self, app_token, client_key=None):
        """

        :param str app_token: Application token generated from PushOver site
        :param str client_key: User or Group key generated from PushOver site
        """
        self._app_token = app_token
        self._client_key = client_key  # Can be a user or group key
        self.latest_response = None
        self._latest_json_response = None

    def push_message(self, message, **kwargs):
        """
        Send message to selected user/group/device.

        :param str message: your message
        :param str client: user or group id to send the message to
        :param str title: your message's title, otherwise your app's name is used
        :param str device: your user's device name to send the message directly to that device
        :param list device: your user's devices names to send the message directly to that device
        :param str url: a supplementary URL to show with your message
        :param str url_title: a title for your supplementary URL, otherwise just the URL is shown
        :param int priority: message priority (Use the Priority class to select)
        :param int retry: how often (in seconds) the Pushover servers will retry the notification to the user (required
                          only with priority level of Emergency)
        :param int expire: how many seconds your notification will continue to be retried (required only with priority
                           level of Emergency)
        :param int timestamp: a Unix timestamp of your message's date and time to display to the user
        :param str sound: the name of the sound to override the user's default sound choice
                          (Use the Sounds class to select)
        """

        # determine if client key has already been saved.  If not then get argument
        client_key = self._client_key
        if 'client' in kwargs:
            client_key = kwargs['client']

        # client key required to push message
        if client_key is None:
            raise ValueError('`client` argument must be set to the group or user id')

        data_out = {
            'token': self._app_token,
            'user': client_key,  # can be a user or group key
            'message': message
        }

        # Support for non-required parameters of PushOver
        if 'title' in kwargs:
            data_out['title'] = kwargs['title']
        if 'device' in kwargs:
            temp = kwargs['device']
            if type(temp) == list:
                data_out['device'] = ','.join(temp)
            else:
                data_out['device'] = temp
            data_out['device'] = kwargs['device']
        if 'url' in kwargs:
            data_out['url'] = kwargs['url']
        if 'url_title' in kwargs:
            data_out['url_title'] = kwargs['url_title']
        if 'priority' in kwargs:
            data_out['priority'] = kwargs['priority']

            # Emergency prioritized messages require 'retry' and 'expire' to be defined
            if data_out['priority'] == Priority.Emergency:
                if 'retry' not in kwargs:
                    raise TypeError('Missing `retry` argument required for message priority of Emergency')
                else:
                    retry_val = kwargs['retry']

                    # 'retry' val must be a minimum of _MIN_RETRY and max of _MAX_EXPIRE
                    if _MAX_EXPIRE < retry_val < _MIN_RETRY:
                        raise ValueError('`retry` argument must be at a minimum of {} and a maximum of {}'.format(
                            _MIN_RETRY, _MAX_EXPIRE
                        ))

                    data_out['retry'] = retry_val
                if 'expire' not in kwargs:
                    raise TypeError('Missing `expire` arguemnt required for message priority of Emergency')
                else:
                    expire_val = kwargs['expire']

                    # 'expire' val must be a minimum of _MIN_RETRY and max of _MAX_EXPIRE
                    if _MAX_EXPIRE < expire_val < _MIN_RETRY:
                        raise ValueError('`expire` argument must be at a minimum of {} and a maximum of {}'.format(
                            _MIN_RETRY, _MAX_EXPIRE
                        ))

                    data_out['expire'] = expire_val

        if 'timestamp' in kwargs:
            data_out['timestamp'] = kwargs['timestamp']
        if 'sound' in kwargs:
            data_out['sound'] = kwargs['sound']

        self._send(self._push_url, data_out)

    def check_receipt(self, receipt=None):
        """
        Gets the receipt status of the selected notificiation.  Returns a dictionary of the results

        see also https://pushover.net/api#receipt
        :param string receipt: the notification receipt to check
        :return dict:
        """
        receipt_to_check = None

        # check to see if previous response had a `receipt`
        if 'receipt' in self._latest_json_response:
            receipt_to_check = self._latest_json_response['receipt']

        # function `receipt` argument takes precedence
        if receipt:
            receipt_to_check = receipt

        # no receipt supplied from either last call or function argument.  Raise error
        if receipt_to_check is None:
            raise TypeError('Missing required `receipt` argument')

        url_to_send = self._receipt_url.format(receipt=receipt_to_check, app_token=self._app_token)
        self._send(url_to_send)
        return self._latest_json_response

    def cancel_retries(self, receipt=None):
        """
        Cancel an emergency-priority notification early.
        :param string receipt:
        """
        receipt_to_check = None

        # check to see if previous response had a `receipt`
        if 'receipt' in self._latest_json_response:
            receipt_to_check = self._latest_json_response['receipt']

        # function `receipt` argument takes precedence
        if receipt:
            receipt_to_check = receipt

        # no receipt supplied from either last call or function argument.  Raise error
        if receipt_to_check is None:
            raise TypeError('Missing required `receipt` argument')

        url_to_send = self._cancel_receipt_url.format(receipt=receipt_to_check)
        self._send(url_to_send, data_out={'token': self._app_token})

    def validate_user(self, user_id, device=None):
        """
        Validates whether a userID is a valid id and returns a Boolean as a result

        :param user_id:
        :return bool:
        """
        return self.validate_group(user_id, device)

    def validate_group(self, group_id, device=None):
        """
        Validates whether a groupID is a valid ID and returns a Boolean as a result

        :param group_id:
        :return bool:
        """
        param_data = {
            'token': self._app_token,
            'user': group_id
        }

        if device:
            param_data['device'] = device

        self._send(self._validate_url, param_data, check_response=False)

        if self._latest_json_response['status'] == 1:
            return True
        else:
            return False

    def group_info(self):
        """

        required params: token
        :return:
        """

        raise NotImplementedError

    def group_add_user(self):
        """

        required params: token, user
        optional params: device, memo
        :return:
        """
        raise NotImplementedError

    def group_remove_user(self):
        """

        required params: token, user
        :return:
        """
        raise NotImplementedError

    def group_disable_user(self):
        """

        required params: token, user
        :return:
        """
        raise NotImplementedError

    def group_enable_user(self):
        """

        required params: token, user
        :return:
        """
        raise NotImplementedError

    def group_rename(self):
        """

        required params: token, name
        :return:
        """
        raise NotImplementedError

    def _send(self, url, data_out=None, check_response=True):
        """
        Sends a formatted request to the supplied url.  If data_out is present, then the data is encoded and sent as
        well.  A check_response value of False the HTTP response code is checked.  A customized HTTPError is raised if
        an error is detected.

        :param string url: url of the site to send the request to (http://www.site.com)
        :param dict data_out: data to be encoded with the url (?token=<app_token>&user=<user_id>)
        :param bool check_response: check http response and raise exception if an error is detected
        """
        if data_out:
            param_data = urllib_encode(data_out)
            if PYTHON_VER == 3:
                param_data = param_data.encode("utf-8")
        else:
            param_data = ''
        req = urllib_request.Request(url, param_data)

        try:
            self.latest_response = urllib_request.urlopen(req)
        except urllib_request.HTTPError as req:
            self.latest_response = req

        if PYTHON_VER == 3:
            self._latest_json_response = json.loads(self.latest_response.readall().decode('utf-8'))
        else:
            self._latest_json_response = json.loads(self.latest_response.read())

        if check_response:
            self._response_check(self.latest_response)

    def _response_check(self, response):
        """
        Checks the HTTP Response code and raises a customized HTTPError based on the Pushover 'errors' response.

        :param Request response: response from server
        """
        if response.code == 200:
            return

        elif 400 <= response.code < 500:
            error = self._latest_json_response['errors']
            self.latest_response.msg = error
            raise self.latest_response

        else:
            raise self.latest_response