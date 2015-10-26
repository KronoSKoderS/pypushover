import unittest


def get_tests():
    return full_suite()

def full_suite():
    from .runtests import TestPushManager

    pushmansuite = unittest.TestLoader().loadTestsFromTestCase(TestPushManager)

    return unittest.TestSuite([pushmansuite])