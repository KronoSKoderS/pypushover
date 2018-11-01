import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import pypushover as pypo

from tests import APP_TOKEN, USER_KEY

class TestBasic(unittest.TestCase):
    def test_inv_app_token(self):
        inv_pm = pypo.message.MessageManager('invalid app token', 'invalid user key')
        with self.assertRaises(pypo.PushoverError):
            with mock.patch('pypushover._base.requests.post') as mock_post:
                mock_post.return_value = mock_response = mock.Mock()
                mock_response.status_code = 400
                mock_response.json.return_value = {
                    'token': 'invalid',
                    'errors': ['application token is invalid'],
                    'status': 0,
                    'request': '116f0a10-7ca7-42c2-b521-f4ba3ed6b0de'
                }
                inv_pm.push_message('This will never work')

            with mock.patch('pypushover._base.requests.post') as mock_post:
                mock_post.return_value = mock_response = mock.Mock()
                mock_response.status_code = 400
                mock_response.json.return_value = {
                    'token': 'invalid',
                    'errors': ['application token is invalid'],
                    'status': 0,
                    'request': '116f0a10-7ca7-42c2-b521-f4ba3ed6b0de'
                }
                pypo.message.push_message('invalid app token', 'invalid user key', 'This will never work')