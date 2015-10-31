import websocket
import logging
from multiprocessing import Process

from py_pushover import BaseManager, send, base_url


class ClientManager(BaseManager):
    """
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

        :param app_token:
        :param secret:
        :param device_id:
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
        self.__p__ = None

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

        :param email:
        :param password:
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
        Sends an acknowlegement to the server that the message was read.

        :param receipt: reciept of the message to ack
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
        self.__p__ = Process(target=self.listen, args=(on_msg_receipt,))
        self.__p__.start()

    def stop_listening(self):
        """
        Stops the listening process from accepting any more messages.
        """
        if self.__p__:
            self.__p__.terminate()
            self.__p__ = None

    def _on_ws_open(self, ws):
        """

        :param ws:
        :return:
        """
        self.__logger__.info("Opening connection to Pushover server...")
        ws.send(self._ws_login.format(device_id=self.__device_id__, secret=self.__secret__))
        self.__logger__.info("----Server Connection Established----")

    def _on_ws_message(self, ws, message):
        """
        # - Keep-alive packet, no response needed.
        ! - A new message has arrived; you should perform a sync.
        R - Reload request; you should drop your connection and re-connect.
        E - Error; a permanent problem occured and you should not automatically re-connect. Prompt the user to login again or re-enable the device.
        :param ws:
        :param message:
        :return:
        """
        message = message.decode("utf-8")
        self.__logger__.debug("Message received: " + message)
        if message == "#":
            pass
        elif message == "!":
            self.retrieve_message()
            self.__on_msg_receipt__(self.messages)

        elif message == "R":
            self.__logger__.info("Reconnecting to server (requested from server)...")
            ws.close()
            self.listen(self.__on_msg_receipt__)

        elif message == "E":
            self.__logger__.error("Server connection failure!")

        else:  # message isn't of the type expected.  Raise an error.
            raise NotImplementedError

    def _on_ws_error(self, ws, error):
        """

        :param ws:
        :param error:
        :return:
        """
        self.__logger__.error('Error: ' + error)

    def _on_ws_close(self, ws):
        """

        :param ws:
        :return:
        """
        self.__logger__.info("----Server Connection Closed----")
        self._ws_app = None

