import unittest
import json

try:
    import unittest.mock as mock
except ImportError as e:
    import mock

import pypushover as pypo

from tests import APP_TOKEN, USER_KEY

GROUP_KEY = USER_KEY

class TestGroup(unittest.TestCase):
    def setUp(self):
        # Mock the response from the server
        with mock.patch('pypushover._base.requests.get') as mock_get:
            mock_get.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_response.json', 'r') as reader:
                res = json.load(reader)
            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            self.valid_gm = pypo.groups.GroupManager(APP_TOKEN, GROUP_KEY)

    def test_group_info(self):
        with mock.patch('pypushover._base.requests.get') as mock_get:
            mock_get.return_value = mock_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_response.json', 'r') as reader:
                res = json.load(reader)

            mock_response.status_code = res['status_code']
            mock_response.json.return_value = res['json']
            mock_response.headers = res['headers']

            info = self.valid_gm.info()
            self.assertEqual(info['name'], 'KronoTestGroup')
            
            info = pypo.groups.info(APP_TOKEN, GROUP_KEY)
            self.assertEqual(info['name'], 'KronoTestGroup')


    def test_group_add_del_user(self):
        with mock.patch('pypushover._base.requests.post') as mock_post, mock.patch('pypushover._base.requests.get') as mock_get:
            mock_post.return_value = mock_post_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_response.json', 'r') as reader:
                res = json.load(reader)

            mock_post_response.status_code = res['status_code']
            mock_post_response.json.return_value = res['json']
            mock_post_response.headers = res['headers']

            mock_get.return_value = mock_get_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_add_user_response.json', 'r') as reader:
                res = json.load(reader)

            mock_get_response.status_code = res['status_code']
            mock_get_response.json.return_value = res['json']
            mock_get_response.headers = res['headers']

            self.valid_gm.add_user(USER_KEY, device='test_device', memo='Added using UnitTests')

            info = self.valid_gm.info()
            self.assertEqual(info['users'][0]['device'], 'test_device')
            self.assertEqual(info['users'][0]['memo'], 'Added using UnitTests')

        with mock.patch('pypushover._base.requests.post') as mock_post, mock.patch('pypushover._base.requests.get') as mock_get:
            mock_post.return_value = mock_post_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_response.json', 'r') as reader:
                res = json.load(reader)

            mock_post_response.status_code = res['status_code']
            mock_post_response.json.return_value = res['json']
            mock_post_response.headers = res['headers']

            mock_get.return_value = mock_get_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_response.json', 'r') as reader:
                res = json.load(reader)

            mock_get_response.status_code = res['status_code']
            mock_get_response.json.return_value = res['json']
            mock_get_response.headers = res['headers']

            self.valid_gm.remove_user(USER_KEY)

            info = self.valid_gm.info()
            self.assertEqual(len(info['users']), 0)

    def test_group_disable_enable_user(self):

        with mock.patch('pypushover._base.requests.post') as mock_post, mock.patch('pypushover._base.requests.get') as mock_get:
            mock_post.return_value = mock_post_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_response.json', 'r') as reader:
                res = json.load(reader)

            mock_post_response.status_code = res['status_code']
            mock_post_response.json.return_value = res['json']
            mock_post_response.headers = res['headers']

            mock_get.return_value = mock_get_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_disabled_user_response.json', 'r') as reader:
                res = json.load(reader)

            mock_get_response.status_code = res['status_code']
            mock_get_response.json.return_value = res['json']
            mock_get_response.headers = res['headers']

            self.valid_gm.disable_user(USER_KEY)
            info = self.valid_gm.info()
            self.assertEqual(info['users'][0]['disabled'], True)

        with mock.patch('pypushover._base.requests.post') as mock_post, mock.patch('pypushover._base.requests.get') as mock_get:
            mock_post.return_value = mock_post_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_response.json', 'r') as reader:
                res = json.load(reader)

            mock_post_response.status_code = res['status_code']
            mock_post_response.json.return_value = res['json']
            mock_post_response.headers = res['headers']

            mock_get.return_value = mock_get_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_enabled_user_response.json', 'r') as reader:
                res = json.load(reader)

            mock_get_response.status_code = res['status_code']
            mock_get_response.json.return_value = res['json']
            mock_get_response.headers = res['headers']

            self.valid_gm.enable_user(USER_KEY)
            info = self.valid_gm.info()
            self.assertEqual(info['users'][0]['disabled'], False)

    def test_group_rename(self):
        with mock.patch('pypushover._base.requests.post') as mock_post, mock.patch('pypushover._base.requests.get') as mock_get:
            mock_post.return_value = mock_post_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_response.json', 'r') as reader:
                res = json.load(reader)

            mock_post_response.status_code = res['status_code']
            mock_post_response.json.return_value = res['json']
            mock_post_response.headers = res['headers']

            mock_get.return_value = mock_get_response = mock.Mock()

            # load a real response from the pickle_jar and use it for the
            # mocked response
            with open('tests/responses/test_good_group_info_rename_response.json', 'r') as reader:
                res = json.load(reader)

            mock_get_response.status_code = res['status_code']
            mock_get_response.json.return_value = res['json']
            mock_get_response.headers = res['headers']

            self.valid_gm.rename('KronoGroup')
            info = self.valid_gm.info()
            self.assertEqual(info['name'], 'KronoGroup')
