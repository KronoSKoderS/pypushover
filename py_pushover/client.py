import websocket
from multiprocessing import Process

from py_pushover import BaseManager, send, base_url


class ClientManager(BaseManager):
    _login_url = base_url + "users/login.json"
    _register_device_url = base_url + "devices.json"
    _message_url = base_url + "messages.json"
    _del_message_url = base_url + "devices/{device_id}/update_highest_message.json"
    _ack_message_url = base_url + "receipts/{receipt_id}/acknowledge.json"
    _ws_connect_url = "wss://client.pushover.net/push"
    _ws_login = "login:{device_id}:{secret}\n"

    def __init__(self, app_token, secret=None, device_id=None):
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

    @property
    def secret(self):
        return self.__secret__

    @property
    def device_id(self):
        return self.__device_id__

    def login(self, email, password):
        params = {
            'email': email,
            'password': password
        }
        self.latest_response_dict = send(self._login_url, data_out=params)
        self.__secret__ = self.latest_response_dict['secret']
        return self.__secret__

    def register_device(self, name):
        params = {
            'secret': self.__secret__,
            'name': name,
            'os': 'O'
        }

        self.latest_response_dict = send(self._register_device_url, data_out=params)
        self.__device_id__ = self.latest_response_dict['id']
        return self.__device_id__

    def retrieve_message(self):
        params = {
            'secret': self.__secret__,
            'device_id': self.__device_id__
        }

        self.latest_response_dict = send(self._message_url, data_out=params, get_method=True)
        self.messages = self.latest_response_dict['messages']

    def clear_server_messages(self):
        params = {
            'secret': self.__secret__,
            'message': max([i['id'] for i in self.messages])
        }

        self.latest_response_dict = send(self._del_message_url.format(device_id=self.__device_id__), params)

    def acknowledge_message(self, receipt):
        params = {
            'secret': self.__secret__
        }

        self.latest_response_dict = send(self._ack_message_url.format(receipt_id=receipt), params)

    def listen(self, on_msg_receipt):
        self.__on_msg_receipt__ = on_msg_receipt
        self._ws_app.run_forever()

    def listen_async(self, on_msg_receipt):
        self.__p__ = Process(target=self.listen, args=(on_msg_receipt,))
        self.__p__.start()

    def _on_ws_open(self, ws):
        print("Opening Connection to Pushover Server....")
        ws.send(self._ws_login.format(device_id=self.__device_id__, secret=self.__secret__))
        print("Success!")

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
        if message == "#":
            pass
        elif message == "!":
            self.retrieve_message()
            self.__on_msg_receipt__(self.messages)

        elif message == "R":
            print("Reconnecting to server...")
            ws.close()
            self.listen(self.__on_msg_receipt__)
        elif message == "E":
            raise NotImplementedError
        else:
            raise NotImplementedError

    def _on_ws_error(self, ws, error):
        print("Error: " + error)

    def _on_ws_close(self, ws):
        print("###Connection to Server Closed###")
        self._ws_app = None

