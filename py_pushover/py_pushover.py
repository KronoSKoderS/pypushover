import json

try:  # Python 3
    import urllib.request as urllib_request
    from urllib.parse import urlencode as urllib_encode

except ImportError:  # Python 2
    import urllib2 as urllib_request
    from urllib import urlencode as urllib_encode


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


    Methods:
    --------
    push_notification - pushes a notification to a device, user or group.
    """
    _push_url = "https://api.pushover.net/1/messages.json"
    _user_verify_url = "https://api.pushover.net/1/users/validate.json"
    _receipt_url = "https://api.pushover.net/1/receipts/{receipt}.json?token={app_token}"

    def __init__(self, app_token, client_key):
        """

        :param str app_token: Application token generated from PushOver site
        :param str client_key: User or Group key generated from PushOver site
        :return:
        """
        self._app_token = app_token
        self._client_key = client_key  # Can be a user or group key
        self.latest_response = None
        self._latest_json_response = None

    def push_message(self, message, **kwargs):
        """
        Send message to selected user/group/device.

        :param str message: your message
        :param str title: your message's title, otherwise your app's name is used
        :param str device: your user's device name to send the message directly to that device
        :param list device: your user's devices names to send the message directly to that device
        :param str url: a supplementary URL to show with your message
        :param str url_title: a title for your supplementary URL, otherwise just the URL is shown
        :param int priority: message priority (Use the Priority class to select)
        :param int timestamp: a Unix timestamp of your message's date and time to display to the user
        :param str sound: the name of the sound to override the user's default sound choice
                          (Use the Sounds class to select)
        """
        json_out = {
            'token': self._app_token,
            'user': self._client_key,  # can be a user or group key
            'message': message
        }

        # Support for non-required parameters of PushOver
        if 'title' in kwargs:
            json_out['title'] = kwargs['title']
        if 'device' in kwargs:
            temp = kwargs['device']
            if type(temp) == list:
                json_out['device'] = ','.join(temp)
            else:
                json_out['device'] = temp
            json_out['device'] = kwargs['device']
        if 'url' in kwargs:
            json_out['url'] = kwargs['url']
        if 'url_title' in kwargs:
            json_out['url_title'] = kwargs['url_title']
        if 'priority' in kwargs:
            json_out['priority'] = kwargs['priority']
        if 'timestamp' in kwargs:
            json_out['timestamp'] = kwargs['timestamp']
        if 'sound' in kwargs:
            json_out['sound'] = kwargs['sound']

        data = urllib_encode(json_out)
        req = urllib_request.Request(self._push_url, data)

        try:
            self.latest_response = urllib_request.urlopen(req)
        except urllib_request.HTTPError as req:
            self.latest_response = req

        self._latest_json_response = json.loads(self.latest_response.read())

        self._response_check(self.latest_response)

    def check_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        return self.check_group(user_id)

    def check_group(self, group_id):
        """
        TODO: Implement
        :param group_id:
        :return:
        """
        return False

    def _response_check(self, response):
        """
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