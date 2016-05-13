import unittest
import time
import requests
import datetime
import re

import pypushover as py_po

try:
    from tests.helpers.keys import user_key, group_key, app_key, device_id, email, pw, secret
except ImportError:  # support for Travis CI
    try:
        import os
        app_key = os.environ['app_key']
        group_key = os.environ['group_key']
        user_key = os.environ['user_key']
        device_id = os.environ['device_id']
        email = os.environ['email']
        pw = os.environ['pw']
        secret = os.environ['secret']
    except KeyError as e:
        raise ImportError(e)  # Environment var missing.  Raise an Import Error


class TestMessage(unittest.TestCase):
    """
    Tests message related API's.  
    """
    def setUp(self):
        self.pm = py_po.message.MessageManager(app_key, user_key)
        self.client = py_po.client.ClientManager(app_key, device_id=device_id)
        self.client.login(email, pw)
        self.cleanUpClient()
        # self.client.listen_async(self.client_message_receieved)

    def tearDown(self):
        # self.client.stop_listening()
        self.cleanUpClient()

    def cleanUpClient(self):
        self.client.retrieve_message()
        for msg in self.client.messages:
            if msg['priority'] >= py_po.PRIORITIES.EMERGENCY and msg['acked'] != 1:
                self.client.acknowledge_message(msg['receipt'])
        self.client.clear_server_messages()

        self.client.retrieve_message()
        self.assertEquals(len(self.client.messages), 0)

    def client_message_receieved(self, messages):
        self.stored_messages = messages

    def test_val_msg(self):

        # Testing a normal push message
        send_message = 'Testing normal push'
        self.pm.push_message(send_message, device='test_device')
        self.client.retrieve_message()

        self.assertEquals(send_message, self.client.messages[0]['message'])

        py_po.message.push_message(app_key, user_key, send_message, device='test_device')
        self.client.retrieve_message()

        self.assertEquals(send_message, self.client.messages[1]['message'])

        self.client.clear_server_messages()

        # Testing normal push message with Title

        val_pm = py_po.message.MessageManager(app_key)
        val_pm.push_message('Testing Title and manual user_key', title='Success!', user=user_key, device='test_device')


        self.pm.push_message("Valid message with 'device' param", device='test_device')

        self.pm.push_message("Valid message with 'url', and 'url_title' params",
            url="https://pushover.net/api#urls",
            url_title="Pushover Api URLS",
            device='test_device'
        )

        self.pm.push_message("Valid message with 'timestamp' param", timestamp=datetime.datetime.now(), device='test_device')

        self.pm.push_message("Valid message with 'sound' param", sound=py_po.SOUNDS.SHORT_BIKE, device='test_device')

    def test_inv_msg(self):
        inv_pm = py_po.message.MessageManager(app_key)
        with self.assertRaises(ValueError):
            inv_pm.push_message('Missing User Key')

    def test_inv_emergency_msg(self):
        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing retry and expire', priority=py_po.PRIORITIES.EMERGENCY)
        with self.assertRaises(TypeError):
            py_po.message.push_message(app_key, user_key, 'Emergency: missing retry and expire', priority=py_po.PRIORITIES.EMERGENCY)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing expire', priority=py_po.PRIORITIES.EMERGENCY, retry=30)
        with self.assertRaises(TypeError):
            py_po.message.push_message(app_key, user_key, 'Emergency: missing expire', priority=py_po.PRIORITIES.EMERGENCY, retry=30)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing retry', priority=py_po.PRIORITIES.EMERGENCY, expire=3600)
        with self.assertRaises(TypeError):
            py_po.message.push_message(app_key, user_key, 'Emergency: missing retry', priority=py_po.PRIORITIES.EMERGENCY, expire=3600)

        with self.assertRaises(ValueError):
            self.pm.push_message('Invalid expire', priority=py_po.PRIORITIES.EMERGENCY, expire=86500, retry=30)
        with self.assertRaises(ValueError):
            py_po.message.push_message(app_key, user_key, 'Invalid retry', priority=py_po.PRIORITIES.EMERGENCY, expire=3600, retry=20)

    def test_emergency_msg(self):
        res = self.pm.push_message(
            "Emergency: Valid",
            priority=py_po.PRIORITIES.EMERGENCY,
            retry=30,
            expire=3600,
            device='test_device'
        )
        self.assertEqual(self.pm.check_receipt()['status'], 1)
        self.assertEqual(self.pm.check_receipt(res['receipt'])['status'], 1)
        self.pm.cancel_retries(res['receipt'])

        self.pm.push_message(
            "Valid Emergency: Last response Cancel",
            priority=py_po.PRIORITIES.EMERGENCY,
            retry=30,
            expire=3600,
            device='test_device'
        )
        self.pm.cancel_retries()

        res = py_po.message.push_message(
            app_key,
            user_key,
            'Emergency Valid',
            priority=py_po.PRIORITIES.EMERGENCY,
            retry=30,
            expire=3600,
            device='test_device'
        )
        time.sleep(0.5)
        self.assertEqual(py_po.message.check_receipt(app_key, res['receipt'])['status'], 1)
        py_po.message.cancel_retries(app_key, res['receipt'])

    def test_inv_check_msg(self):
        self.pm.push_message("Valid Message: no receipt", device="test_device")
        with self.assertRaises(TypeError):
            self.pm.check_receipt()

    def test_inv_cancel_retry(self):
        self.pm.push_message("Valid Message: no reciept", device="test_device")
        with self.assertRaises(TypeError):
            self.pm.cancel_retries()


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.valid_gm = py_po.groups.GroupManager(app_key, group_key)

        # clean up any previously failed test
        if len(self.valid_gm.group.users) > 0:
            self.valid_gm.remove_user(user_key)

    def test_group_info(self):
        info = self.valid_gm.info()
        self.assertEqual(info['name'], 'KronoTestGroup')
        info = py_po.groups.info(app_key, group_key)
        self.assertEqual(info['name'], 'KronoTestGroup')

        self.valid_gm.add_user(user_key, device='test_device', memo='group info test')

        self.assertEquals(self.valid_gm.group.name, 'KronoTestGroup')
        self.assertEquals(self.valid_gm.group.users[0].device, 'test_device')

        self.valid_gm.remove_user(user_key)

    def test_group_add_del_user(self):

        self.valid_gm.add_user(user_key, device='test_device', memo='Added using UnitTests')
        info = self.valid_gm.info()
        self.assertEqual(info['users'][0]['device'], 'test_device')
        self.assertEqual(info['users'][0]['memo'], 'Added using UnitTests')

        self.valid_gm.remove_user(user_key)
        info = self.valid_gm.info()
        self.assertEqual(len(info['users']), 0)

    def test_group_disable_enable_user(self):
        self.valid_gm.add_user(user_key, device='test_device', memo='dis/ena test')

        self.valid_gm.disable_user(user_key)
        info = self.valid_gm.info()
        self.assertEqual(info['users'][0]['disabled'], True)
        self.valid_gm.enable_user(user_key)
        info = self.valid_gm.info()
        self.assertEqual(info['users'][0]['disabled'], False)

        self.valid_gm.remove_user(user_key)

    def test_group_rename(self):
        self.valid_gm.rename('KronoGroup')
        info = self.valid_gm.info()
        self.assertEqual(info['name'], 'KronoGroup')
        self.valid_gm.rename('KronoTestGroup')
        info = self.valid_gm.info()
        self.assertEqual(info['name'], 'KronoTestGroup')


class TestVerifcation(unittest.TestCase):
    def setUp(self):
        self.valid_vm = py_po.verification.VerificationManager(app_key)
        self.valid_gm = py_po.groups.GroupManager(app_key, group_key)

    def test_val_user(self):
        self.assertTrue(self.valid_vm.verify_user(user_key, device='test_device'))
        self.assertTrue(py_po.verification.verify_user(app_key, user_key, device='test_device'))

    def test_inv_user(self):
        inv_user_key = "justabunchofjunk"
        with self.assertRaises(requests.HTTPError):
            self.valid_vm.verify_user(inv_user_key)

    def test_val_group(self):
        self.assertTrue(self.valid_vm.verify_group(group_key))
        self.assertTrue(py_po.verification.verify_group(app_key, group_key))

        self.assertTrue(self.valid_vm.verify_group(group_key))
        self.assertTrue(py_po.verification.verify_group(app_key, group_key))

    def test_inv_group(self):
        inv_group_key = "justabunchofjunk"
        with self.assertRaises(requests.HTTPError):
            self.valid_vm.verify_group(inv_group_key)
        with self.assertRaises(requests.HTTPError):
            py_po.verification.verify_group(app_key, inv_group_key)

        with self.assertRaises(requests.HTTPError):
            self.valid_vm.verify_user(inv_group_key)
        with self.assertRaises(requests.HTTPError):
            py_po.verification.verify_user(app_key, inv_group_key)

        with self.assertRaises(requests.HTTPError):
            self.valid_vm.verify_user(user_key, device='junk')
        with self.assertRaises(requests.HTTPError):
            py_po.verification.verify_user(app_key, user_key, device='junk')


class TestLicense(unittest.TestCase):
    def setUp(self):
        raise NotImplementedError


class TestClient(unittest.TestCase):
    def setUp(self):
        self.pm = py_po.message.MessageManager(app_key, user_key)
        self.cm = py_po.client.ClientManager(app_key, device_id=device_id)
        self.cm.login(email, pw)
        self.cm.retrieve_message()
        self.cm.clear_server_messages()

    def tearDown(self):
        self.cm.stop_listening()

    def test_rec_msg(self):
        msg_to_snd = 'Simple Message Sent'
        self.pm.push_message(msg_to_snd, device='test_device')
        self.cm.retrieve_message()
        self.assertEqual(msg_to_snd, self.cm.messages[0]['message'])

    def test_ack_msg(self):
        msg_to_snd = 'Emergency Message to Ack'
        self.pm.push_message(
            msg_to_snd,
            device='test_device',
            priority=py_po.PRIORITIES.EMERGENCY,
            retry=30,
            expire=30
        )
        self.cm.retrieve_message()
        msg = self.cm.messages[0]
        self.assertEqual(msg['acked'], 0)
        self.cm.acknowledge_message(msg['receipt'])
        self.cm.retrieve_message()
        self.assertEqual(msg['id'], self.cm.messages[0]['id'])
        msg = self.cm.messages[0]
        self.assertEqual(msg['acked'], 1)

    @staticmethod
    def callback(messages):
        test_msg = "callback test message"
        assert(test_msg == messages[0]['message'])
        cm = py_po.client.ClientManager(app_key, secret, device_id)
        cm.clear_server_messages()

    def test_listen(self):
        test_msg = "test_listen message"
        self.cm.listen_async(TestClient.callback)
        self.pm.push_message(test_msg, device='test_device')


class TestBasic(unittest.TestCase):
    def test_inv_app_token(self):
        inv_pm = py_po.message.MessageManager(group_key, user_key)
        with self.assertRaises(requests.HTTPError):
            inv_pm.push_message('This will never work')
            py_po.message.push_message(group_key, app_key, 'This will never work')


class TestIssuesManual(unittest.TestCase):
    """
    These tests require manual setup or cleanup and therefore cannot be automated using Travis CI.  Run these manually
    before submitting to the rel branch.
    """
    def test_37_dash_support(self):
        """
        WARNING!  You will need to DELETE any devices created using this test manually or this test will no longer
        work.
        :return:
        """
        cm = py_po.client.ClientManager(app_key)
        vm = py_po.verification.VerificationManager(app_key)

        cm.login(email, pw)
        device_id = cm.register_device('Example-2')
        vm.verify_user(user_key, 'Example-2')
        device_id = cm.register_device("name-with-multiple-dashes")
        vm.verify_user(user_key, 'name-with-multiple-dashes')

        self._del_devices()

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


class TestIssues(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
