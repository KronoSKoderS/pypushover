import unittest
import requests

import pypushover as pypo


class TestIssues(unittest.TestCase):
    def test_37_dash_support(self):
        """
        WARNING!  You will need to DELETE any devices created using this test manually or this test will no longer
        work.
        :return:
        """
        self._del_devices()
        cm = pypo.client.ClientManager(app_key)
        vm = pypo.verification.VerificationManager(app_key)

        cm.login(email, pw)
        device_id = cm.register_device('Example-2')
        vm.verify_user(user_key, 'Example-2')
        device_id = cm.register_device("name-with-multiple-dashes")
        vm.verify_user(user_key, 'name-with-multiple-dashes')

        self._del_devices()

    def test_39_clear_messages(self):
        cm = pypo.client.ClientManager(app_key, secret=secret, device_id=device_id)
        pm = pypo.message.MessageManager(app_key, user_key)

        cm.retrieve_messages()
        cm.clear_server_messages()
        pm.push_message('test1', device='test_device')
        pm.push_message('test2', device='test_device')

        cm.retrieve_messages()
        self.assertEquals(len(cm.messages), 2)

        cm.clear_server_messages()
        self.assertEquals(len(cm.messages), 0)

    def _del_devices(self):
        s = requests.session()
        r = s.post("https://pushover.net/login/login")
        matchme = 'meta content="(.*)" name="csrf-token" /'
        auth_token = re.search(matchme, str(r.text)).group(1)
        payload = {
            'user[email]': email,
            'user[password]': pw,
            'authenticity_token': auth_token
        }
        s.post("https://pushover.net/login/login", data=payload)
        payload = {'authenticity_token': auth_token}
        s.post("https://pushover.net/devices/destroy/Example-2", data=payload)
        s.post("https://pushover.net/devices/destroy/name-with-multiple-dashes", data=payload)