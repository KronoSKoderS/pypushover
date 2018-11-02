"""Message Tests - A collection of tests to verify the functionality of the Message API
"""
import unittest
import datetime
import time
import json

try:
    import unittest.mock as mock
except ImportError as e:
    import mock

import pypushover as pypo

from tests import APP_TOKEN, USER_KEY


class TestMessages(unittest.TestCase):
    """
    Tests message related API's.
    """

    def setUp(self):
        self.pm = pypo.message.MessageManager(APP_TOKEN, USER_KEY)

    def client_message_receieved(self, messages):
        self.stored_messages = messages

    def test_val_simple_msg(self):
        # Mock the response from the server
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            # Testing a normal push message
            send_message = 'Testing normal push'
            self.pm.push_message(send_message)
            self.assertEqual(self.pm.latest_response_dict['status'], 1)
            mock_post.assert_called_once_with(
                pypo.message._push_url,
                params={'token': APP_TOKEN, 'user': USER_KEY,
                        'message': send_message}
            )

    def test_val_cmplx_msg(self):
        send_message = 'Testing complex normal push'

        cur_time = datetime.datetime.now()
        payload = {
            'title': 'Simple Title',
            'device': ['device-1', 'device-2'],
            'url': 'http://pushover.net/',
            'url_title': 'Pushover',
            'timestamp': cur_time,
            'sound': pypo.SOUNDS.SHORT_CLASSICAL,
            'html': True,
            'attachment': 'tests/carrier.jpg'
        }

        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.pm.push_message(
                send_message,
                **payload
            )

            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)

    def test_inv_emergency_msg(self):
        with self.assertRaises(TypeError):
            self.pm.push_message(
                'Emergency: missing retry and expire', priority=pypo.PRIORITIES.EMERGENCY)
        with self.assertRaises(TypeError):
            pypo.message.push_message(
                APP_TOKEN, USER_KEY, 'Emergency: missing retry and expire', priority=pypo.PRIORITIES.EMERGENCY)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing expire',
                                 priority=pypo.PRIORITIES.EMERGENCY, retry=30)
        with self.assertRaises(TypeError):
            pypo.message.push_message(
                APP_TOKEN, USER_KEY, 'Emergency: missing expire', priority=pypo.PRIORITIES.EMERGENCY, retry=30)

        with self.assertRaises(TypeError):
            self.pm.push_message('Emergency: missing retry',
                                 priority=pypo.PRIORITIES.EMERGENCY, expire=3600)
        with self.assertRaises(TypeError):
            pypo.message.push_message(
                APP_TOKEN, USER_KEY, 'Emergency: missing retry', priority=pypo.PRIORITIES.EMERGENCY, expire=3600)

        with self.assertRaises(ValueError):
            self.pm.push_message(
                'Invalid expire', priority=pypo.PRIORITIES.EMERGENCY, expire=86500, retry=30)
        with self.assertRaises(ValueError):
            pypo.message.push_message(APP_TOKEN, USER_KEY, 'Invalid retry',
                                      priority=pypo.PRIORITIES.EMERGENCY, expire=3600, retry=20)

    def test_emergency_msg(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_emergency_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            send_message = "Emergency: Valid"
            payload = {
                'priority': pypo.PRIORITIES.EMERGENCY,
                'retry': 30,
                'expire': 3600,
                'device': 'test_device'
            }

            expected_payload = payload.copy()
            expected_payload.update(
                {'token': APP_TOKEN, 'user': USER_KEY, 'message': send_message})

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
        # Setup the initial 'message' sent
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the json and use it for the
            # mocked response
            with open('tests/responses/test_good_emergency_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            receipt = res['json']['receipt']

            send_message = "Emergency: Valid"
            payload = {
                'priority': pypo.PRIORITIES.EMERGENCY,
                'retry': 30,
                'expire': 3600,
                'device': 'test_device'
            }

            self.pm.push_message(
                send_message,
                **payload
            )

        with mock.patch('pypushover._base.requests.get') as mock_get:
            mock_get.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_check_receipt_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.pm.check_receipt(receipt=receipt)

            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)
            mock_get.assert_called_once_with(
                pypo.message._receipt_url.format(receipt=receipt),
                params={'token': APP_TOKEN}
            )

    def test_cancel_retry(self):
        # Setup the initial 'message' sent
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the json and use it for the
            # mocked response
            with open('tests/responses/test_good_emergency_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            receipt = res['json']['receipt']

            send_message = "Emergency: Valid"
            payload = {
                'priority': pypo.PRIORITIES.EMERGENCY,
                'retry': 30,
                'expire': 3600,
                'device': 'test_device'
            }

            self.pm.push_message(
                send_message,
                **payload
            )

        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the json and use it for the
            # mocked response
            with open('tests/responses/test_good_check_receipt_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.pm.cancel_retries(receipt=receipt)

            self.assertEqual(mock_response.json(), self.pm.latest_response_dict)
            mock_post.assert_called_once_with(
                pypo.message._cancel_receipt_url.format(receipt=receipt),
                params={'token': APP_TOKEN}
            )

    def test_inv_check_msg(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'status': 1,
                'request': 'cbc6c03f-0667-43dc-b151-96971a5c4605'
            }

            self.pm.push_message(
                "Valid Message: no receipt", device="test_device")
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

            self.assertEqual(mock_response.json(),
                             self.pm.latest_response_dict)
            mock_post.assert_called_once_with(
                pypo.message._cancel_receipt_url.format(receipt=receipt),
                params={'token': APP_TOKEN}
            )

        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'status': 1,
                'request': 'cbc6c03f-0667-43dc-b151-96971a5c4605'
            }

            self.pm.push_message(
                "Valid Message: no reciept", device="test_device")
            with self.assertRaises(TypeError):
                self.pm.cancel_retries()
