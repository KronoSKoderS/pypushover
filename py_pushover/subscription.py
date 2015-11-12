from py_pushover import BaseManager, send

_subscription_url = "https://pushover.net/subscribe/"


class SubscriptionManager(object):
    def __init__(self, sub_code):
        if sub_code.startswith('https://'):
            self._sub_code = sub_code
        else:
            self._sub_code = _subscription_url + sub_code

    def subscribe(self, sucess, failure):
        subscribe(self._sub_code, sucess, failure)


def subscribe(url, success, failure):
    params = {
        'success': success,
        'failure': failure
    }
    send(url, data_out=params)