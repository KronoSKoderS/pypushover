import unittest
import time
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

    def test_val_group(self):
        self.assertTrue(self.valid_pm.validate_group(group_key))

    def test_inv_group(self):
        inv_group_key = "justabunchofjunk"
        self.assertFalse(self.valid_pm.validate_group(inv_group_key))

    def test_inv_emergency_msg(self):
        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency!', priority=py_po.Priority.Emergency)

        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency', priority=py_po.Priority.Emergency, retry=30)

        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency', priority=py_po.Priority.Emergency, expire=3600)

    def test_val_emergency_msg(self):
        self.valid_pm.push_message("Emergency", priority=py_po.Priority.Emergency, retry=30, expire=3600)
        time.sleep(5)
        self.valid_pm.cancel_retries()





if __name__ == "__main__":
    unittest.main()