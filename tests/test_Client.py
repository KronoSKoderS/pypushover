import unittest

import pypushover as pypo

class TestClient(unittest.TestCase):
    def setUp(self):
        self.pm = pypo.message.MessageManager(app_key, user_key)
        self.cm = pypo.client.ClientManager(app_key, device_id=device_id)
        self.cm.login(email, pw)
        self.cm.retrieve_messages()
        self.cm.clear_server_messages()

    def tearDown(self):
        self.cm.stop_listening()

    def test_rec_msg(self):
        msg_to_snd = 'Simple Message Sent'
        self.pm.push_message(msg_to_snd, device='test_device')
        self.cm.retrieve_messages()
        self.assertEqual(msg_to_snd, self.cm.messages[0]['message'])

    def test_ack_msg(self):
        msg_to_snd = 'Emergency Message to Ack'
        self.pm.push_message(
            msg_to_snd,
            device='test_device',
            priority=pypo.PRIORITIES.EMERGENCY,
            retry=30,
            expire=30
        )
        self.cm.retrieve_messages()
        msg = self.cm.messages[0]
        self.assertEqual(msg['acked'], 0)
        self.cm.acknowledge_message(msg['receipt'])
        self.cm.retrieve_messages()
        self.assertEqual(msg['id'], self.cm.messages[0]['id'])
        msg = self.cm.messages[0]
        self.assertEqual(msg['acked'], 1)

    @staticmethod
    def callback(messages):
        test_msg = "callback test message"
        assert(test_msg == messages[0]['message'])
        cm = pypo.client.ClientManager(app_key, secret, device_id)
        cm.clear_server_messages()

    def test_listen(self):
        test_msg = "test_listen message"
        self.cm.listen_async(TestClient.callback)
        self.pm.push_message(test_msg, device='test_device')