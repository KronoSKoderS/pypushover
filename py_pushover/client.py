"""
============================================
client - Client Manager for the Pushover API
============================================

This module defines classes and functions necessary to act as a Client to the Pushover servers.  For more details about
the Pushover API for clients visit [their site](https://pushover.net/api/client)

Creating a client:
------------------

For the first time, creating a client requires the following steps:

1. Create an object of class type ClientManager and pass in your app token
2. Have the user login to the Pushover service with their email and password
3. Register your client service as a new device

While doing these steps, you'll receive a 'secret' and 'device_id'.  These are return with the `ClientManager.login`
and `ClientManager.register_device` methods.  They are also stored in the `secret` and `device_id` properties.  This
secret and device id MUST be stored in a safe location if stored at all.

Here is an example:

    >>> import py_pushover as py_po
    >>> cm = py_po.client.ClientManager('<app token>')
    >>> secret = cm.login('user email', 'user pass')
    >>> device_id = cm.register_device('device_name')

If you already have a secret and device id, then you can pass those into the ClientManager upon creation:

    >>> import py_pushover as py_po
    >>> cm = py_po.client.ClientManager('<app token>', secret='<user secret>', device_id='<device id>')

Retrieving Messages:
--------------------
Messages are retrieved from the Pushover Server by using the `retrieve_message` method.  Once called, all messages
stored on the Pushover servers are then stored into the `messages` property.  These messages are a list of
dictionaries with items as [defined in the Pushover API](https://pushover.net/api/client#download).

    >>> cm.retrieve_message()
    >>> for msg in cm.messages:
    ...     print(msg['message'])

Clearing Messages from Pushover Server:
---------------------------------------
Messages stored on the Pushover Server should be cleared after being presented to the user.  This is done using the
`clear_server_messages` method.  Note: This only clears out the messages on Pushover's servers and not the local
copy stored in the objects `messages` property.

    >>> cm.clear_server_messages()

Acknowledge an Emergency Message:
---------------------------------
If an emergency priority message is received, the Pushover Server should be acknowledged of that receipt per [their
API guidelines](https://pushover.net/api/client#p2).  Once the user has acknowledged the message, using the
`acknowledge_message` method passing in the emergency messages `receipt`.

    >>> cm.retrieve_message()
    >>> for msg in cm.messages:
    ...     print(msg['message'])
    ...     if msg['priority'] == py_po.PRIORITIES.EMERGENCY:
    ...         cm.acknowledge_message(msg['receipt'])

Listening Servers:
------------------
You can call the `listen` or `listen_async` method to constantly listen and respond to messages.  Pass in a function
to these methods that accepts a single input for the received message(s).

Using the `listen` method is a Blocking method that will continually run until interrupted either manually (Ctrl+c)
or through and unrecoverable loss in connection to the Pushover Servers.

    >>> def print_msg(messages):
    ...     for msg in messages:
    ...         print(msg['message'])
    >>> cm.listen(print_msg)

Using the `listen_async` method is a non-blocking method that will continually run until interrupted using the
`stop_listening` method.

    >>> cm.listen_async(print_msg)
    >>> time.sleep(30)
    >>> cm.stop_listening
"""
import websocket
import logging
from multiprocessing import Process, Pipe

from py_pushover import BaseManager, send, base_url


class ClientManager(BaseManager):
    """
    Manages the interface between the Pushover Servers and user.  This can be instantiated with or without the user
    secret and device id.  If no secret is provided, the user MUST login before interfacing with the Pushover servers.
    If no device id is provided, the user MUST register this client as a device before interfacing with the Pushover
    servers.
    """
    _login_url = base_url + "users/login.json"
    _register_device_url = base_url + "devices.json"
    _message_url = base_url + "messages.json"
    _del_message_url = base_url + "devices/{device_id}/update_highest_message.json"
    _ack_message_url = base_url + "receipts/{receipt_id}/acknowledge.json"
    _ws_connect_url = "wss://client.pushover.net/push"
    _ws_login = "login:{device_id}:{secret}\n"

    def __init__(self, app_token, secret=None, device_id=None):
        """
        :param str app_token: application id from Pushover API
        :param str secret: (Optional) user secret given after validation of login
        :param str device_id: (Optional) device id of this client
        :return:
        """
        super(ClientManager, self).__init__(app_token)
        self.__secret__ = secret
        self.__device_id__ = device_id
        self.messages = []
        self._ws_app = websocket.WebSocketApp(
            self._ws_connect_url,
            on_open=self._on_ws_open,
            on_message=self._on_ws_message,
            on_error=self._on_ws_error,
            on_close=self._on_ws_close
        )
        self.__on_msg_receipt__ = None
        self.__p__ = Process()
        self.__parent_conn__, self.__child_conn__ = Pipe(False)

        self.__logger__ = logging.basicConfig(filename='client.log')

    @property
    def secret(self):
        return self.__secret__

    @property
    def device_id(self):
        return self.__device_id__

    def login(self, email, password):
        """
        Logs into the Pushover server with the user's email and password.  Retrieves a secret key, stores it, and then
        returns it.

        :param email: the users email
        :param password: the users password
        :return:
        """
        params = {
            'email': email,
            'password': password
        }
        self.latest_response_dict = send(self._login_url, data_out=params)
        self.__secret__ = self.latest_response_dict['secret']
        return self.__secret__

    def register_device(self, name):
        """
        Registers the device (this client) with the name of `name`.  The devices id is then stored and returned.

        :param str name: Name of the device to register
        :return string: device_id of the device registered
        """
        params = {
            'secret': self.__secret__,
            'name': name,
            'os': 'O'
        }

        self.latest_response_dict = send(self._register_device_url, data_out=params)
        self.__device_id__ = self.latest_response_dict['id']
        return self.__device_id__

    def retrieve_message(self):
        """
        Retrieves messages stored on the Pushover servers and saves them into the `messages` property.
        """
        params = {
            'secret': self.__secret__,
            'device_id': self.__device_id__
        }

        self.latest_response_dict = send(self._message_url, data_out=params, get_method=True)
        self.messages = self.latest_response_dict['messages']

    def clear_server_messages(self):
        """
        Clears the messages stored on Pushover servers.
        """
        if self.messages:
            params = {
                'secret': self.__secret__,
                'message': max([i['id'] for i in self.messages])
            }

            self.latest_response_dict = send(self._del_message_url.format(device_id=self.__device_id__), params)

    def acknowledge_message(self, receipt):
        """
        Sends an acknowledgement to the server that the message was read.

        :param receipt: receipt of the message to ack
        """
        params = {
            'secret': self.__secret__
        }

        self.latest_response_dict = send(self._ack_message_url.format(receipt_id=receipt), params)

    def listen(self, on_msg_receipt):
        """
        Listens for messages from the server.  When a message is received, a call to the on_msg_receipt function with a
          single parameter representing the messages received.

        :param on_msg_receipt: function to call when a message is received
        """
        self.__on_msg_receipt__ = on_msg_receipt
        self._ws_app.run_forever()

    def listen_async(self, on_msg_receipt):
        """
        Creates a Process for listening to the Pushover server for new messages.  This process then listens for messages
          from the server.  When a message is received, a call to the on_msg_receipt function with a single parameter
          representing the messages received.

        :param on_msg_receipt: function to call when a message is received
        """
        self.__child_conn__, self.__parent_conn__ = Pipe(False)
        self.__p__ = Process(target=self.listen, args=(on_msg_receipt,))
        self.__p__.start()
        return self.__child_conn__

    def stop_listening(self):
        """
        Stops the listening process from accepting any more messages.
        """
        if self.__p__:
            self.__p__.terminate()
            self.__p__ = None

        if self.__parent_conn__:
            self.__parent_conn__.close()
            self.__parent_conn__ = None

    def _on_ws_open(self, ws):
        """
        Function used when the websocket is opened for the first time.

        :param ws: the websocket
        """
        self.__logger__.info("Opening connection to Pushover server...")
        ws.send(self._ws_login.format(device_id=self.__device_id__, secret=self.__secret__))
        self.__logger__.info("----Server Connection Established----")

    def _on_ws_message(self, ws, message):
        """
        Function used for when the websocket recieves a message.  Per the Pushover API guidelines 1 of 4 responses
        will be sent:

            1. `#` - Keep-alive packet, no response needed.
            2. `!` - A new message has arrived; you should perform a sync.
            3. `R` - Reload request; you should drop your connection and re-connect.
            4. `E` - Error; a permanent problem occured and you should not automatically re-connect.
                     Prompt the user to login again or re-enable the device.

        :param ws: the websocket
        :param message: message received from remote server
        """
        message = message.decode("utf-8")
        self.__logger__.debug("Message received: " + message)
        if message == "#":
            pass

        elif message == "!":
            self.retrieve_message()
            if self.__on_msg_receipt__:
                self.__on_msg_receipt__(self.messages)

            self.__parent_conn__.send(self.messages)

        elif message == "R":
            self.__logger__.info("Reconnecting to server (requested from server)...")
            ws.close()
            self.listen(self.__on_msg_receipt__)

        elif message == "E":
            self.__logger__.error("Server connection failure!")

        else:  # message isn't of the type expected.  Raise an error.
            raise NotImplementedError  #todo Implement an appropriate exception

    def _on_ws_error(self, ws, error):
        """
        Function used when the websocket encounters an error.  The error is logged

        :param ws: the websocket
        :param error: the error encountered
        """
        self.__logger__.error('Error: ' + error)

    def _on_ws_close(self, ws):
        """
        Function used when the websocket closes the connection to the remote server.

        :param ws: the websocket
        """
        self.__logger__.info("----Server Connection Closed----")
        self._ws_app = None

