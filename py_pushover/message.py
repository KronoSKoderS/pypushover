from py_pushover import Priorities, _BaseManager, _send, _base_url

_MAX_EXPIRE = 86400
_MIN_RETRY = 30

_push_url = _base_url + "messages.json"
_base_receipt_url = _base_url + "receipts/{receipt}"
_receipt_url = _base_receipt_url + ".json"
_cancel_receipt_url = _base_receipt_url + "/cancel.json"


class MessageManager(_BaseManager):
    def __init__(self, app_token, receiver_key=None):
        super().__init__(app_token, user_key=receiver_key, group_key=receiver_key)
        raise NotImplementedError

    def push_message(self, message, **kwargs):

        ret_receipt = False

        # determine if client key has already been saved.  If not then get argument
        client_key = self._user_key
        if 'user' in kwargs:
            client_key = kwargs['client']

        # client key required to push message
        if client_key is None:
            raise ValueError('`user` argument must be set to the group or user id')

        self.latest_response_dict = push_message(self._app_token, client_key, message, **kwargs)

        if ret_receipt:
            return self.latest_response_dict['receipt']

    def check_receipt(self, receipt=None):
        """
        Gets the receipt status of the selected notificiation.  Returns a dictionary of the results

        see also https://pushover.net/api#receipt
        :param string receipt: the notification receipt to check
        :return dict:
        """
        receipt_to_check = None

        # check to see if previous response had a `receipt`
        if 'receipt' in self.latest_response_dict:
            receipt_to_check = self.latest_response_dict['receipt']

        # function `receipt` argument takes precedence
        if receipt:
            receipt_to_check = receipt

        # no receipt supplied from either last call or function argument.  Raise error
        if receipt_to_check is None:
            raise TypeError('Missing required `receipt` argument')

        url_to_send = self._receipt_url.format(receipt=receipt_to_check)
        self._send(url_to_send)
        return self.latest_response_dict

    def cancel_retries(self, receipt=None):
        """
        Cancel an emergency-priority notification early.
        :param string receipt:
        """
        receipt_to_check = None

        # check to see if previous response had a `receipt`
        if 'receipt' in self.latest_response_dict:
            receipt_to_check = self.latest_response_dict['receipt']

        # function `receipt` argument takes precedence
        if receipt:
            receipt_to_check = receipt

        # no receipt supplied from either last call or function argument.  Raise error
        if receipt_to_check is None:
            raise TypeError('Missing required `receipt` argument')

        url_to_send = self._cancel_receipt_url.format(receipt=receipt_to_check)
        self._send(url_to_send, data_out={'token': self._app_token})


def push_message(token, user, message, **kwargs):
    """
    Send message to selected user/group/device.

    :param str token: application token
    :param str user: user or group id to send the message to
    :param str message: your message
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
    :param str sound: the name of the sound to override the user's default sound choice (Use the Sounds consts to
                      select)
    """
    data_out = {
        'token': token,
        'user': user,  # can be a user or group key
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
        if data_out['priority'] == Priorities.Emergency:
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

            ret_receipt = True

    if 'timestamp' in kwargs:
        data_out['timestamp'] = kwargs['timestamp']
    if 'sound' in kwargs:
        data_out['sound'] = kwargs['sound']

    return _send(_push_url, data_out=data_out)


def check_receipt(token, receipt, **kwargs):
    raise NotImplementedError


def cancel_retries(token, receipt, **kwargs):
    raise NotImplementedError