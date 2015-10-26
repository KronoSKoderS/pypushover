import unittest
import time
import requests
import py_pushover as py_po
from tests.helpers.keys import user_key, group_key, app_key


class TestPushManager(unittest.TestCase):
    def setUp(self):
        self.valid_pm = py_po.PushOverManager(app_key, user_key, group_key=group_key)

    def test_inv_app_token(self):
        inv_pm = py_po.PushOverManager(group_key, user_key)
        with self.assertRaises(requests.HTTPError):
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
            self.valid_pm.push_message('Emergency!', priority=py_po.Priorities.Emergency)

        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency', priority=py_po.Priorities.Emergency, retry=30)

        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency', priority=py_po.Priorities.Emergency, expire=3600)

    def test_val_emergency_msg(self):
        self.valid_pm.push_message("Emergency", priority=py_po.Priorities.Emergency, retry=30, expire=3600)
        time.sleep(5)
        self.valid_pm.cancel_retries()

    def test_group_info(self):
        info = self.valid_pm.group_info(group_key=group_key)
        self.assertEqual(info['name'], 'TestGroup')

        info = self.valid_pm.group_info()
        self.assertEqual(info['name'], 'TestGroup')

    def test_group_add_del_user(self):
        self.valid_pm.group_remove_user(user_key)
        info = self.valid_pm.group_info()
        self.assertEqual(len(info['users']), 0)
        self.valid_pm.group_add_user(user_key, device='KronoDroid', memo='Added using UnitTests')
        info = self.valid_pm.group_info()
        self.assertEqual(info['users'][0]['device'], 'KronoDroid')
        self.assertEqual(info['users'][0]['memo'], 'Added using UnitTests')

    def test_group_disable_enable_user(self):
        self.valid_pm.group_disable_user(user_key)
        info = self.valid_pm.group_info()
        self.assertEqual(info['users'][0]['disabled'], True)
        self.valid_pm.group_enable_user(user_key)
        info = self.valid_pm.group_info()
        self.assertEqual(info['users'][0]['disabled'], False)

    def test_group_rename(self):
        self.valid_pm.group_rename('KronoTestGroup')
        info = self.valid_pm.group_info()
        self.assertEqual(info['name'], 'KronoTestGroup')
        self.valid_pm.group_rename('TestGroup')
        info = self.valid_pm.group_info()
        self.assertEqual(info['name'], 'TestGroup')


if __name__ == "__main__":
    unittest.main()