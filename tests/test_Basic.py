import unittest

import pypushover as pypo


class TestBasic(unittest.TestCase):
    def test_inv_app_token(self):
        inv_pm = pypo.message.MessageManager(group_key, user_key)
        with self.assertRaises(pypo.PushoverError):
            inv_pm.push_message('This will never work')
            pypo.message.push_message(group_key, app_key, 'This will never work')