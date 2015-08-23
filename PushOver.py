import sys
#Making compatible for Python 3 and 2.
if sys.version_info < (3, 0, 0):
    import urllib
else:
    import urllib2.parse as urllib

import urllib2


class Sounds(object):
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
    Lowest = -2
    Low = -1
    Normal = 0
    High = 1
    Emergency = 2


class PushOverManager(object):
    _url = "https://api.pushover.net/1/messages.json"

    def __init__(self, app_token, group_key):
        self._app_token = app_token
        self._group_key = group_key

    def push_notification(self, title, message, **kwargs):
        json_out = {
            'token': self._app_token,
            'user': self._group_key,
            'title': title,
            'message': message
        }

        # Support for non-required parameters of PushOver
        if 'device' in kwargs:
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
        req = urllib2.Request(self._url, data)
        if self._response_check(urllib2.urlopen(req)) < 1:
            raise UserWarning("Notification did not succeed")

    @staticmethod
    def _response_check(response):
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
