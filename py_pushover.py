import urllib

try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request


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
    Emergency = 2   # require confirmation from the user


class PushOverManager(object):
    """
    Push Over Manager - Class for interfacing with the Pushover API.

    Properties:
    -----------


    Methods:
    --------
    push_notificaiton - pushes a notification to a device, user or group.
    """
    _push_url = "https://api.pushover.net/1/messages.json"
    _user_verify_url = "https://api.pushover.net/1/users/validate.json"


    def __init__(self, app_token, group_key):
        self._app_token = app_token
        self._group_key = group_key

    def push_notification(self, message, **kwargs):
        """
        :param str message: your message
        :param str title: your message's title, otherwise your app's name is used
        :param str device: your user's device name to send the message directly to that device
        :param list device: your user's devices names to send the message directly to that device
        :param str url: a supplementary URL to show with your message
        :param str url_title: a title for your supplementary URL, otherwise just the URL is shown
        :param int priority: message priority
        :param int timestamp: a Unix timestamp of your message's date and time to display to the user
        :param str sound: the name of

        See also: https://pushover.net/api#messages
        """
        json_out = {
            'token': self._app_token,
            'user': self._group_key,
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

        data = urllib.urlencode(json_out)
        req = urllib_request.Request(self._push_url, data)

        if self._response_check(urllib_request.urlopen(req)) < 1:
            raise UserWarning("Notification did not succeed")

    @staticmethod
    def _response_check(response):
        """
        :param Request response: response from server
        :return:

        TODO: Make more robust
        """
        if response.code == 200:
            return 1

        elif 400 <= response.code < 500:
            print("Invalid input!  Potential issues are max quota reached, token invalid, user no longer active, etc,.")
            if 'errors' in response.headers.dict:
                print(response.headers.dict['errors'])
            return -1

        else:
            print("Unable to connect to API or not reply.  Please try again in 5 seconds")
            return 0