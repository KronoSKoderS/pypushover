import unittest
from py_pushover import py_pushover as py_po
from helpers import user_key, group_key, app_key

try:  # Python 3
    import urllib.request as urllib_request
    from urllib.parse import urlencode as urllib_encode

except ImportError:  # Python 2
    import urllib2 as urllib_request
    from urllib import urlencode as urllib_encode


class TestPushManager(unittest.TestCase):
    def setUp(self):
        self.valid_pm = py_po.PushOverManager(app_key, user_key)

    def test_inv_app_token(self):
        inv_pm = py_po.PushOverManager(group_key, user_key)
        with self.assertRaises(urllib_request.HTTPError):
            inv_pm.push_message('This should never work')

    def test_val_app_token(self):
        self.valid_pm.push_message('This should always work')

    def test_val_user(self):
        self.assertTrue(self.valid_pm.validate_user(user_key))

    def test_inv_user(self):
        inv_user_key = "justabunchofjunk"
        self.assertFalse(self.valid_pm.validate_user(inv_user_key))

if __name__ == "__main__":
    unittest.main()