import unittest
import time
import json

try:
    import unittest.mock as mock
except ImportError as e:
    import mock

import pypushover as pypo

from tests import APP_TOKEN, USER_KEY

GROUP_KEY = USER_KEY

class TestVerification(unittest.TestCase):
    def setUp(self):
        self.valid_vm = pypo.verification.VerificationManager(APP_TOKEN)

        with mock.patch('pypushover._base.requests.get') as mock_get:
            mock_get.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_enabled_user_response.json', 'rb') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.valid_gm = pypo.groups.GroupManager(APP_TOKEN, GROUP_KEY)

    def test_val_user(self):
        # Mock the response from the server
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_verify_user_response.json', 'rb') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.assertTrue(self.valid_vm.verify_user(USER_KEY, device='test_device'))

        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_verify_user_response.json', 'rb') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.assertTrue(pypo.verification.verify_user(APP_TOKEN, USER_KEY, device='test_device'))

    def test_inv_user(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_bad_verify_user_response.json', 'rb') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            inv_USER_KEY = "justabunchofjunk"
            with self.assertRaises(pypo.PushoverError):
                self.valid_vm.verify_user(inv_USER_KEY)

    def test_val_group(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_verify_group_response.json', 'rb') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.assertTrue(self.valid_vm.verify_group(GROUP_KEY))
            self.assertTrue(pypo.verification.verify_group(APP_TOKEN, GROUP_KEY))

    def test_inv_group(self):
        with mock.patch('pypushover._base.requests.post') as mock_post:
            mock_post.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_bad_verify_user_response.json', 'rb') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            inv_GROUP_KEY = "justabunchofjunk"
            with self.assertRaises(pypo.PushoverError):
                pypo.verification.verify_group(APP_TOKEN, inv_GROUP_KEY)
            with self.assertRaises(pypo.PushoverError):
                pypo.verification.verify_user(APP_TOKEN, inv_GROUP_KEY)
