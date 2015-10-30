import websocket

from py_pushover import BaseManager, send, base_url


class ClientManager(BaseManager):
    _login_url = base_url + "users/login.json"
    _register_device_url = base_url + "devices.json"
    _message_url = base_url + "messages.json"
    _del_message_url = base_url + "devices/{device_id}/update_highest_message.json"
    _ack_message_url = base_url + "receipts/{receipt_id}/acknowledge.json"

    def __init__(self, app_token, secret=None, device_id=None):
        super(ClientManager, self).__init__(app_token)
        self.__secret = secret
        self.__device_id = device_id
        self.messages = []

    def login(self, email, password):
        params = {
            'email': email,
            'password': password
        }
        self.latest_response_dict = send(self._login_url, data_out=params)
        self.__secret = self.latest_response_dict['secret']

    def register_device(self, name):
        params = {
            'secret': self.__secret,
            'name': name,
            'os': 'O'
        }

        self.latest_response_dict = send(self._register_device_url, data_out=params)
        self.__device_id = self.latest_response_dict['id']

    def retrieve_message(self):
        params = {
            'secret': self.__secret,
            'device_id': self.__device_id
        }

        self.latest_response_dict = send(self._message_url, data_out=params, get_method=True)
        self.messages = self.latest_response_dict['messages']

    def clear_server_messages(self):
        params = {
            'secret': self.__secret,
            'message': max([i['id'] for i in self.messages])
        }

        self.latest_response_dict = send(self._del_message_url.format(device_id=self.__device_id), params)

    def acknowledge_message(self, receipt):
        params = {
            'secret': self.__secret
        }

        self.latest_response_dict = send(self._ack_message_url.format(receipt_id=receipt), params)

    def _on_ws_message(self, ws, message):
        pass

    def _on_ws_error(self, ws, error):
        pass

    def _on_ws_close(self, ws, error):
        pass

    def _on_ws_open(self, ws):
        pass

