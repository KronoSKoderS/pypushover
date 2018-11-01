import unittest

import pypushover as pypo

class TestGroup(unittest.TestCase):
    def setUp(self):
        self.valid_gm = pypo.groups.GroupManager(app_key, group_key)

        # clean up any previously failed test
        if len(self.valid_gm.group.users) > 0:
            self.valid_gm.remove_user(user_key)

    def test_group_info(self):
        info = self.valid_gm.info()
        self.assertEqual(info['name'], 'KronoTestGroup')
        info = pypo.groups.info(app_key, group_key)
        self.assertEqual(info['name'], 'KronoTestGroup')

        self.valid_gm.add_user(user_key, device='test_device', memo='group info test')

        self.assertEquals(self.valid_gm.group.name, 'KronoTestGroup')
        self.assertEquals(self.valid_gm.group.users[0].device, 'test_device')

        self.valid_gm.remove_user(user_key)

    def test_group_add_del_user(self):

        self.valid_gm.add_user(user_key, device='test_device', memo='Added using UnitTests')
        info = self.valid_gm.info()
        self.assertEqual(info['users'][0]['device'], 'test_device')
        self.assertEqual(info['users'][0]['memo'], 'Added using UnitTests')

        self.valid_gm.remove_user(user_key)
        info = self.valid_gm.info()
        self.assertEqual(len(info['users']), 0)

    def test_group_disable_enable_user(self):
        self.valid_gm.add_user(user_key, device='test_device', memo='dis/ena test')

        self.valid_gm.disable_user(user_key)
        info = self.valid_gm.info()
        self.assertEqual(info['users'][0]['disabled'], True)
        self.valid_gm.enable_user(user_key)
        info = self.valid_gm.info()
        self.assertEqual(info['users'][0]['disabled'], False)

        self.valid_gm.remove_user(user_key)

    def test_group_rename(self):
        self.valid_gm.rename('KronoGroup')
        info = self.valid_gm.info()
        self.assertEqual(info['name'], 'KronoGroup')
        self.valid_gm.rename('KronoTestGroup')
        info = self.valid_gm.info()
        self.assertEqual(info['name'], 'KronoTestGroup')