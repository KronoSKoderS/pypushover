import unittest
from py_pushover import py_pushover as py_po
from helpers import user_key, group_key, app_key


class TestPushManager(unittest.TestCase):
    def setUp(self):
        self.valid_pm = py_po.PushOverManager(app_key, group_key)

    def test_push_msg(self):
        self.valid_pm.push_message('test', title='Hello', device='KronoDroid')


if __name__ == "__main__":
    unittest.main()