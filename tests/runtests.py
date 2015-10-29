import unittest
import time
import requests
import py_pushover as py_po

try:
    from tests.helpers.keys import user_key, group_key, app_key
except ImportError:  # support for Travis CI
    import os
    app_key = os.environ['app_key']
    group_key = os.environ['group_key']
    user_key = os.environ['user_key']


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.valid_pm = py_po.message.MessageManager(app_key, user_key)

    def test_val_msg(self):
        self.valid_pm.push_message('Testing normal push (Manager method)')
        py_po.message.push_message(app_key, user_key, 'Testing normal message push (static function)')

        val_pm = py_po.message.MessageManager(app_key)
        val_pm.push_message('Testing Title and manual user_key', title='Success!', user=user_key)

        self.valid_pm.push_message("Valid message with 'device' param", device='KronoDroid')

        self.valid_pm.push_message("Valid message with 'url', and 'url_title' params",
            url="https://pushover.net/api#urls",
            url_title="Pushover Api URLS"
        )

    def test_inv_msg(self):
        inv_pm = py_po.message.MessageManager(app_key)
        with self.assertRaises(ValueError):
            inv_pm.push_message('Missin User Key')

    def test_inv_emergency_msg(self):
        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency!', priority=py_po.PRIORITIES.EMERGENCY)
            py_po.message.push_message(app_key, user_key, 'Emergency', priority=py_po.PRIORITIES.EMERGENCY)

        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency', priority=py_po.PRIORITIES.EMERGENCY, retry=30)
            py_po.message.push_message('Emergency', priority=py_po.PRIORITIES.EMERGENCY, retry=30)

        with self.assertRaises(TypeError):
            self.valid_pm.push_message('Emergency', priority=py_po.PRIORITIES.EMERGENCY, expire=3600)
            py_po.message.push_message(app_key, user_key, 'Emergency', priority=py_po.PRIORITIES.EMERGENCY, expire=3600)

        with self.assertRaises(ValueError):
            self.valid_pm.push_message('Invalid expire', priority=py_po.PRIORITIES.EMERGENCY, expire=86500, retry=30)
            py_po.message.push_message(app_key, user_key, 'Invalid retry', expire=3600, retry=20)

    def test_emergency_msg(self):
        res = self.valid_pm.push_message("Emergency", priority=py_po.PRIORITIES.EMERGENCY, retry=30, expire=3600)
        time.sleep(0.5)
        self.assertEqual(self.valid_pm.check_receipt()['status'], 1)
        self.assertEqual(self.valid_pm.check_receipt(res['receipt'])['status'], 1)
        self.valid_pm.cancel_retries(res['receipt'])

        self.valid_pm.push_message("Valid Emergency: Last response Cancel", priority=py_po.PRIORITIES.EMERGENCY, retry=30, expire=3600)
        self.valid_pm.cancel_retries()

        res = py_po.message.push_message(app_key, user_key, 'Emergency', priority=py_po.PRIORITIES.EMERGENCY, retry=30, expire=3600)
        time.sleep(0.5)
        self.assertEqual(py_po.message.check_receipt(app_key, res['receipt'])['status'], 1)
        py_po.message.cancel_retries(app_key, res['receipt'])

    def test_inv_check_msg(self):
        self.valid_pm.push_message("Valid Message: no receipt")
        with self.assertRaises(TypeError):
            self.valid_pm.check_receipt()

    def test_inv_cancel_retry(self):
        self.valid_pm.push_message("Valid Message: no reciept")
        with self.assertRaises(TypeError):
            self.valid_pm.cancel_retries()


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.valid_pm = py_po.groups.GroupManager(app_key, group_key)

    def test_group_info(self):
        info = self.valid_pm.group_info()
        self.assertEqual(info['name'], 'KronoTestGroup')

        info = self.valid_pm.group_info(group_key=group_key)
        self.assertEqual(info['name'], 'KronoTestGroup')

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
        self.valid_pm.group_rename('KronoGroup')
        info = self.valid_pm.group_info()
        self.assertEqual(info['name'], 'KronoGroup')
        self.valid_pm.group_rename('KronoTestGroup')
        info = self.valid_pm.group_info()
        self.assertEqual(info['name'], 'KronoTestGroup')


class TestVerifcation(unittest.TestCase):
    def setUp(self):
        self.valid_pm = py_po.verification.VerificationManager(app_key)

    def test_val_user(self):
        self.assertTrue(self.valid_pm.verify_user(user_key))

    def test_inv_user(self):
        inv_user_key = "justabunchofjunk"
        with self.assertRaises(requests.HTTPError):
            self.valid_pm.verify_user(inv_user_key)

    def test_val_group(self):
        self.assertTrue(self.valid_pm.verify_group(group_key))

    def test_inv_group(self):
        inv_group_key = "justabunchofjunk"
        with self.assertRaises(requests.HTTPError):
            self.valid_pm.verify_group(inv_group_key)


class TestSubscription(unittest.TestCase):
    def setUp(self):
        raise NotImplementedError


class TestLicense(unittest.TestCase):
    def setUp(self):
        raise NotImplementedError


class TestClient(unittest.TestCase):
    def setUp(self):
        raise NotImplementedError


class TestBasic(unittest.TestCase):
    def test_inv_app_token(self):
        inv_pm = py_po.message.MessageManager(group_key, user_key)
        with self.assertRaises(requests.HTTPError):
            inv_pm.push_message('This will never work')
            py_po.message.push_message(group_key, app_key, 'This will never work')

if __name__ == "__main__":
    unittest.main()
