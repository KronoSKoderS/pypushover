"""Message Tests - A collection of tests to verify the functionality of the Message API
"""
import unittest
import datetime
import time

try:
    import unittest.mock as mock
except ImportError as e:
    import mock

import pypushover as pypo


# The token and user key are taken from the online Pushover docs to help
# make this more real and won't work in real life.
APP_TOKEN = "KzGDORePKggMaC0QOYAMyEEuzJnyUi;"
USER_KEY = "e9e1495ec75826de5983cd1abc8031"


class TestMessages(unittest.TestCase):
    """
    Tests message related API's.
    """
    def setUp(self):
        self.pm = pypo.message.MessageManager(APP_TOKEN, USER_KEY)

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
            self.assertEqual(self.pm.latest_response_dict['status'], 1)
            mock_post.assert_called_once_with(
                pypo.message._push_url,
                params={'token':APP_TOKEN, 'user':USER_KEY, 'message':send_message}
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
                'token':APP_TOKEN,
                'user':USER_KEY,
                'message':send_message,
                'timestamp': int(time.mktime(cur_time.timetuple()))
            })

            self.pm.push_message(
                send_message,
                **payload
            )
            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)
            mock_post.assert_called_once_with(
                pypo.message._push_url,
                params=expected_payload
            )

    def test_inv_emergency_msg(self):
        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing retry and expire', priority=pypo.PRIORITIES.EMERGENCY)
        with self.assertRaises(TypeError):
            pypo.message.push_message(APP_TOKEN, USER_KEY, 'Emergency: missing retry and expire', priority=pypo.PRIORITIES.EMERGENCY)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing expire', priority=pypo.PRIORITIES.EMERGENCY, retry=30)
        with self.assertRaises(TypeError):
            pypo.message.push_message(APP_TOKEN, USER_KEY, 'Emergency: missing expire', priority=pypo.PRIORITIES.EMERGENCY, retry=30)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing retry', priority=pypo.PRIORITIES.EMERGENCY, expire=3600)
        with self.assertRaises(TypeError):
            pypo.message.push_message(APP_TOKEN, USER_KEY, 'Emergency: missing retry', priority=pypo.PRIORITIES.EMERGENCY, expire=3600)

        with self.assertRaises(ValueError):
            self.pm.push_message('Invalid expire', priority=pypo.PRIORITIES.EMERGENCY, expire=86500, retry=30)
        with self.assertRaises(ValueError):
            pypo.message.push_message(APP_TOKEN, USER_KEY, 'Invalid retry', priority=pypo.PRIORITIES.EMERGENCY, expire=3600, retry=20)

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
            expected_payload.update({'token':APP_TOKEN, 'user':USER_KEY, 'message':send_message})

            self.pm.push_message(
                send_message,
                **payload
            )

            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)
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
                'acknowledged_by': USER_KEY,
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

            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)
            mock_get.assert_called_once_with(
                pypo.message._receipt_url.format(receipt=receipt),
                params={'token':APP_TOKEN}
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

            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)
            mock_post.assert_called_once_with(
                pypo.message._cancel_receipt_url.format(receipt=receipt),
                params={'token':APP_TOKEN}
            )

    def test_inv_check_msg(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'status': 1, 
                'request': 'cbc6c03f-0667-43dc-b151-96971a5c4605'
            }

            self.pm.push_message("Valid Message: no receipt", device="test_device")
            with self.assertRaises(TypeError):
                self.pm.check_receipt()

    def test_inv_cancel_retry(self):
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

            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)
            mock_post.assert_called_once_with(
                pypo.message._cancel_receipt_url.format(receipt=receipt),
                params={'token':APP_TOKEN}
            )
        
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'status': 1, 
                'request': 'cbc6c03f-0667-43dc-b151-96971a5c4605'
            }
            
            self.pm.push_message("Valid Message: no reciept", device="test_device")
            with self.assertRaises(TypeError):
                self.pm.cancel_retries()