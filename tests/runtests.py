import unittest
import time
import requests
import datetime
import re

try:
    import unittest.mock as mock
except ImportError as e:
    import mock

import pypushover as pypo

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
        self.pm = pypo.message.MessageManager(app_key, user_key)

    def client_message_receieved(self, messages):
        self.stored_messages = messages

    def test_val_simple_msg(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'app_remaining': '7188',
                'app_reset': '1467349200',
                'app_limit': '7500',
                'request': '1f210d80a55f643d1cc84d2ece548010',
                'status': 1
            }

            # Testing a normal push message
            send_message = 'Testing normal push'
            self.pm.push_message(send_message)
            self.assertEquals(self.pm.latest_response_dict['status'], 1)
            mock_post.assert_called_once_with(
                pypo.message._push_url,
                params={'token':app_key, 'user':user_key, 'message':send_message}
            )

    def test_val_cmplx_msg(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'app_remaining': '7188',
                'app_reset': '1467349200',
                'app_limit': '7500',
                'request': '1f210d80a55f643d1cc84d2ece548010',
                'status': 1
            }

            send_message = 'Testing complex normal push'

            cur_time = datetime.datetime.now()
            payload = {
                'title': 'Simple Title',
                'device': ['device-1', 'device-2'],
                'url': 'http://pushover.net/',
                'url_title': 'Pushover',
                'timestamp': cur_time,
                'sound': pypo.SOUNDS.SHORT_CLASSICAL,
                'html': True
            }

            expected_payload = payload.copy()
            expected_payload.update({
                'token':app_key,
                'user':user_key,
                'message':send_message,
                'timestamp': int(time.mktime(cur_time.timetuple()))
            })

            self.pm.push_message(
                send_message,
                **payload
            )
            self.assertEquals(mock_response.json(), self.pm.latest_response_dict)
            mock_post.assert_called_once_with(
                pypo.message._push_url,
                params=expected_payload
            )

    def test_inv_emergency_msg(self):
        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing retry and expire', priority=pypo.PRIORITIES.EMERGENCY)
        with self.assertRaises(TypeError):
            pypo.message.push_message(app_key, user_key, 'Emergency: missing retry and expire', priority=pypo.PRIORITIES.EMERGENCY)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing expire', priority=pypo.PRIORITIES.EMERGENCY, retry=30)
        with self.assertRaises(TypeError):
            pypo.message.push_message(app_key, user_key, 'Emergency: missing expire', priority=pypo.PRIORITIES.EMERGENCY, retry=30)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing retry', priority=pypo.PRIORITIES.EMERGENCY, expire=3600)
        with self.assertRaises(TypeError):
            pypo.message.push_message(app_key, user_key, 'Emergency: missing retry', priority=pypo.PRIORITIES.EMERGENCY, expire=3600)

        with self.assertRaises(ValueError):
            self.pm.push_message('Invalid expire', priority=pypo.PRIORITIES.EMERGENCY, expire=86500, retry=30)
        with self.assertRaises(ValueError):
            pypo.message.push_message(app_key, user_key, 'Invalid retry', priority=pypo.PRIORITIES.EMERGENCY, expire=3600, retry=20)

    def test_emergency_msg(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'app_reset': '1467349200',
                'app_remaining': '7180',
                'receipt': 'rntc332738nkc4hsyytctis6sa97bj',
                'app_limit': '7500',
                'request': 'c35df522c4f4a1a4182eb740d70430d4',
                'status': 1
            }

            send_message = "Emergency: Valid"
            payload = {
                'priority':pypo.PRIORITIES.EMERGENCY,
                'retry':30,
                'expire':3600,
                'device':'test_device'
            }

            expected_payload = payload.copy()
            expected_payload.update({'token':app_key, 'user':user_key, 'message':send_message})

            self.pm.push_message(
                send_message,
                **payload
            )

            self.assertEquals(mock_response.json(), self.pm.latest_response_dict)
            mock_post.assert_called_with(
                pypo.message._push_url,
                params=expected_payload
            )

    def test_check_receipt(self):
        with mock.patch('pypushover._base.requests.get') as mock_get:
            mock_get.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'called_back': 0,
                'expired': 0,
                'called_back_at': 0,
                'expires_at': 1465192994,
                'acknowledged_by_device': 'KronoPhone6',
                'request': '8c69616b0418697725ed41e3f3dfa22b',
                'acknowledged_by': user_key,
                'acknowledged_at': 1465189414,
                'status': 1,
                'acknowledged': 1,
                'last_delivered_at': 1465189394
            }

            receipt = 'r7zt2yk86qhzdk34mqywvgtt3z9kqy'

            self.pm.latest_response_dict = {
                'app_reset': '1467349200',
                'app_remaining': '7162',
                'receipt': receipt,
                'app_limit': '7500',
                'request': 'f9a2648343cdf3c5336bd6e1f8d95b37',
                'status': 1
            }

            self.pm.check_receipt(receipt=receipt)

            self.assertEquals(mock_response.json(), self.pm.latest_response_dict)
            mock_get.assert_called_once_with(
                pypo.message._receipt_url.format(receipt=receipt),
                params={'token':app_key}
            )

    def test_cancel_retry(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'request': '6af7c78e85c1edcb2f1426214eb6ec48', 'status': 1
            }

            # 'fake' latest response
            self.pm.latest_response_dict = {
                'app_reset': '1467349200',
                'app_remaining': '7172',
                'receipt': 'ryd8w31fydoo19ipjysa4cwc9eh87h',
                'app_limit': '7500',
                'request': '0219487621ddc7718a0eb71961d9c6f9',
                'status': 1
            }

            receipt = 'ryd8w31fydoo19ipjysa4cwc9eh87h'

            self.pm.cancel_retries(receipt=receipt)

            self.assertEquals(mock_response.json(), self.pm.latest_response_dict)
            mock_post.assert_called_once_with(
                pypo.message._cancel_receipt_url.format(receipt=receipt),
                params={'token':app_key}
            )

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
        self.valid_gm = pypo.groups.GroupManager(app_key, group_key)

        # clean up any previously failed test
        if len(self.valid_gm.group.users) > 0:
            self.valid_gm.remove_user(user_key)

    def test_group_info(self):
        info = self.valid_gm.info()
        self.assertEqual(info['name'], 'KronoTestGroup')
        info = pypo.groups.info(app_key, group_key)
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
        self.valid_vm = pypo.verification.VerificationManager(app_key)
        self.valid_gm = pypo.groups.GroupManager(app_key, group_key)
        time.sleep(10)

    def test_val_user(self):
        self.assertTrue(self.valid_vm.verify_user(user_key, device='test_device'))
        time.sleep(10)
        self.assertTrue(pypo.verification.verify_user(app_key, user_key, device='test_device'))

    def test_inv_user(self):
        inv_user_key = "justabunchofjunk"
        with self.assertRaises(pypo.PushoverError):
            self.valid_vm.verify_user(inv_user_key)

    def test_val_group(self):
        self.assertTrue(self.valid_vm.verify_group(group_key))
        time.sleep(10)
        self.assertTrue(pypo.verification.verify_group(app_key, group_key))
        time.sleep(10)
        self.assertTrue(self.valid_vm.verify_group(group_key))
        time.sleep(10)
        self.assertTrue(pypo.verification.verify_group(app_key, group_key))

    def test_inv_group(self):
        inv_group_key = "justabunchofjunk"
        with self.assertRaises(pypo.PushoverError):
            self.valid_vm.verify_group(inv_group_key)
        time.sleep(10)
        with self.assertRaises(pypo.PushoverError):
            pypo.verification.verify_group(app_key, inv_group_key)
        time.sleep(10)
        with self.assertRaises(pypo.PushoverError):
            self.valid_vm.verify_user(inv_group_key)
        time.sleep(10)
        with self.assertRaises(pypo.PushoverError):
            pypo.verification.verify_user(app_key, inv_group_key)
        time.sleep(10)
        with self.assertRaises(pypo.PushoverError):
            self.valid_vm.verify_user(user_key, device='junk')
        time.sleep(10)
        with self.assertRaises(pypo.PushoverError):
            pypo.verification.verify_user(app_key, user_key, device='junk')


class TestLicense(unittest.TestCase):
    def setUp(self):
        raise NotImplementedError


class TestClient(unittest.TestCase):
    def setUp(self):
        self.pm = pypo.message.MessageManager(app_key, user_key)
        self.cm = pypo.client.ClientManager(app_key, device_id=device_id)
        self.cm.login(email, pw)
        self.cm.retrieve_messages()
        self.cm.clear_server_messages()

    def tearDown(self):
        self.cm.stop_listening()

    def test_rec_msg(self):
        msg_to_snd = 'Simple Message Sent'
        self.pm.push_message(msg_to_snd, device='test_device')
        self.cm.retrieve_messages()
        self.assertEqual(msg_to_snd, self.cm.messages[0]['message'])

    def test_ack_msg(self):
        msg_to_snd = 'Emergency Message to Ack'
        self.pm.push_message(
            msg_to_snd,
            device='test_device',
            priority=pypo.PRIORITIES.EMERGENCY,
            retry=30,
            expire=30
        )
        self.cm.retrieve_messages()
        msg = self.cm.messages[0]
        self.assertEqual(msg['acked'], 0)
        self.cm.acknowledge_message(msg['receipt'])
        self.cm.retrieve_messages()
        self.assertEqual(msg['id'], self.cm.messages[0]['id'])
        msg = self.cm.messages[0]
        self.assertEqual(msg['acked'], 1)

    @staticmethod
    def callback(messages):
        test_msg = "callback test message"
        assert(test_msg == messages[0]['message'])
        cm = pypo.client.ClientManager(app_key, secret, device_id)
        cm.clear_server_messages()

    def test_listen(self):
        test_msg = "test_listen message"
        self.cm.listen_async(TestClient.callback)
        self.pm.push_message(test_msg, device='test_device')


class TestBasic(unittest.TestCase):
    def test_inv_app_token(self):
        inv_pm = pypo.message.MessageManager(group_key, user_key)
        with self.assertRaises(pypo.PushoverError):
            inv_pm.push_message('This will never work')
            pypo.message.push_message(group_key, app_key, 'This will never work')


class TestIssuesManual(unittest.TestCase):
    """
    These tests require manual setup or cleanup and therefore cannot be automated using Travis CI.  Run these manually
    before submitting to the rel branch.
    """
    pass


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


if __name__ == "__main__":
    unittest.main()
