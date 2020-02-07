"""
===============================================
message.py - Message handling for the Pushover API
===============================================

This module defines functions and classes used for handling messages sent to the Pushover servers.  Messages can be sent
using either the MessageManager class or calling the functions directly.  Using the MessageManager class reduces the
need to send the app_token and group/user key for each sending of a message.

Sending messages can be done using the ``send_message`` method of the ``MessageManager`` class or the ``send_message``
function found within this module.  There are API `restrictions <https://pushover.net/api#limits>`_ that are required
by Pushover but are NOT handled by ``py_pushover``. It is intended that the user will maintain all of these
requirements.

Sending Basic Messages
----------------------

Sending a basic message requires the following:

* an application token
* a group or user key
* the message text

Examples using the ``MessageManager`` class and the ``push_message`` function are as follows:

Using the ``MessageManager`` class:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create an object of the ``MessageManager`` class
2. Call the ``send_message`` method

    >>> import pypushover as pypo
    >>> pm = pypo.message.MessageManager('<app_token>', '<group/user key>')
    >>> pm.push_message('Message Body')

Using the function call:
^^^^^^^^^^^^^^^^^^^^^^^^

    >>> pypo.message.push_message('<app_token>', '<group/user key>', 'Message Body')

Sending Emergency Priority Messages
-----------------------------------

Emergency Priority messages are messages that are intended to be read by the user immediately and require an
acknowledgement for dismissal.  When passing in a ``priority`` of Emergency (``pypushover.PRIORITIES.EMERGENCY``), two
additional parameters are required:

* ``retry`` - how often (in seconds) the Pushover servers will retry the notification to the user
* ``expire`` - how many seconds your notification will continue to be retried

Below is an example:

    >>> res = pm.send_message('Emergency Message!', priority=pypo.PRIORITIES.EMERGENCY, retry=30, expire=3600)
    >>> res = pypo.message.push_message(
    ...     '<app_token>',
    ...     '<group/user key>',
    ...     'Emergency Message!',
    ...     priority=pypo.PRIORITES.EMERGENCY,
    ...     retry=30,
    ...     expire=3600
    ... )

After an emergency message is sent, it's status can be queried using ``check_receipt``.  The parameter passed in, is the
emergency messages response receipt parameter.

    >>> pm.check_receipt(res['receipt'])
    >>> pypo.message.check_receipt('app_token', res['receipt'])

If you decide to cancel Pushover's repeated tries to send an Emergency Priority message, use the ``cancel_retries`` with
the ``receipt`` parameter passed in.

    >>> pm.cancel_retries(res['receipt'])
    >>> pypo.message.cancel_retries('app_token', res['receipt'])

Other Supported Parameters
--------------------------------

* ``user`` (string): user or group id to send the message to
* ``title`` (string): your message's title, otherwise your app's name is used
* ``device`` (string): your user's device name to send the message directly to that device
* ``device`` (list of strings): your user's devices names to send the message directly to that device
* ``url`` (string): a supplementary URL to show with your message
* ``url_title`` (string): a title for your supplementary URL, otherwise just the URL is shown
* ``priority`` (string): message priority (Use the `Priorities` constants to select)
* ``timestamp`` (string): a Unix timestamp of your message's date and time to display to the user
* ``sound`` (string): the name of the sound to override the user's default sound choice (Use the ``Sounds`` constants to
select)
"""

__all__ = ('MessageManager', 'push_message', 'check_receipt', 'cancel_retries')

import time

from pypushover import PRIORITIES, BaseManager, base_url, send


_MAX_EXPIRE = 86400
_MIN_RETRY = 30

_push_url = base_url + "messages.json"
_base_receipt_url = base_url + "receipts/{receipt}"
_receipt_url = _base_receipt_url + ".json"
_cancel_receipt_url = _base_receipt_url + "/cancel.json"


class MessageManager(BaseManager):
    """
    Manager class used to send messages and check receipts.  Stores the given app_token for future use.  Also stores the
    latest response from the API.
    """
    def __init__(self, app_token, receiver_key=None):
        super(MessageManager, self).__init__(app_token, user_key=receiver_key, group_key=receiver_key)

    def push_message(self, message, **kwargs):
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
        :param datetime timestamp: a datetime object repr the timestamp of your message's date and time to display to the user
        :param str sound: the name of the sound to override the user's default sound choice (Use the Sounds consts to
                          select)
        :param bool html: Enable rendering message on user device using HTML
        """

        # determine if client key has already been saved.  If not then get argument.  Group key takes priority
        client_key = self._group_key if self._group_key else self._user_key
        if 'user' in kwargs:
            client_key = kwargs['user']
            kwargs.pop('user')

        # client key required to push message
        if client_key is None:
            raise ValueError('`user` argument must be set to the group or user id')

        self.latest_response_dict = push_message(self._app_token, client_key, message, **kwargs)
        return self.latest_response_dict

    def check_receipt(self, receipt=None):
        """
        Gets the receipt status of the selected notification.  Returns a dictionary of the results

        see also https://pushover.net/api#receipt

        :param string receipt: the notification receipt to check (if none given, the most recent response is used)
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

        self.latest_response_dict = check_receipt(self._app_token, receipt_to_check)
        return self.latest_response_dict

    def cancel_retries(self, receipt=None):
        """
        Cancel an emergency-priority notification early.

        :param string receipt: the notification receipt to cancel (if none given, the most recent response is used)
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

        self.latest_response_dict = cancel_retries(self._app_token, receipt_to_check)
        return self.latest_response_dict


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
    :param datetime timestamp: a datetime object repr the timestamp of your message's date and time to display to the user
    :param str sound: the name of the sound to override the user's default sound choice (Use the Sounds consts to
                      select)
    :param bool html: Enable rendering message on user device using HTML
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
        if data_out['priority'] == PRIORITIES.EMERGENCY:
            if 'retry' not in kwargs:
                raise TypeError('Missing `retry` argument required for message priority of Emergency')
            else:
                retry_val = kwargs['retry']

                # 'retry' val must be a minimum of _MIN_RETRY and max of _MAX_EXPIRE
                if not (_MIN_RETRY <= retry_val <= _MAX_EXPIRE):
                    raise ValueError('`retry` argument must be at a minimum of {} and a maximum of {}'.format(
                        _MIN_RETRY, _MAX_EXPIRE
                    ))

                data_out['retry'] = retry_val
            if 'expire' not in kwargs:
                raise TypeError('Missing `expire` arguemnt required for message priority of Emergency')
            else:
                expire_val = kwargs['expire']

                # 'expire' val must be a minimum of _MIN_RETRY and max of _MAX_EXPIRE
                if not(_MIN_RETRY <= expire_val <= _MAX_EXPIRE):
                    raise ValueError('`expire` argument must be at a minimum of {} and a maximum of {}'.format(
                        _MIN_RETRY, _MAX_EXPIRE
                    ))

                data_out['expire'] = expire_val

            # Optionally a callback url may be supplied for the Emergency Message
            if 'callback' in kwargs:
                data_out['callback'] = kwargs['callback']

    if 'timestamp' in kwargs:
        data_out['timestamp'] = int(time.mktime(kwargs['timestamp'].timetuple()))
    if 'sound' in kwargs:
        data_out['sound'] = kwargs['sound']
    if 'html' in kwargs:
        data_out['html'] = int(kwargs['html'])

    return send(_push_url, data_out=data_out)


def check_receipt(token, receipt):
    """
    Check to see if an Emergency Priority notification has been acknowledged.

    :param str token: the application token
    :param str receipt: the message receipt
    :return:
    """
    url_to_send = _receipt_url.format(receipt=receipt)
    return send(url_to_send, data_out={'token': token}, get_method=True)


def cancel_retries(token, receipt):
    """
    Ceases retrying to notify the user of an Emergency Priority notification.

    Cancel an emergency-priority notification early.
    :param str token: application token
    :param str receipt: receipt of the message
    """
    url_to_send = _cancel_receipt_url.format(receipt=receipt)
    return send(url_to_send, data_out={'token': token})

