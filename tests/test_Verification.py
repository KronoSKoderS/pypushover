import unittest
import time

import pypushover as pypo

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