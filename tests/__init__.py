import unittest


def get_tests():
    return full_suite()


def full_suite():
    from .runtests import TestBasic, TestClient, TestGroup, TestLicense, TestMessage, TestSubscription, TestVerifcation

    return unittest.TestSuite([
#        unittest.TestLoader().loadTestsFromTestCase(TestBasic),
#        unittest.TestLoader().loadTestsFromTestCase(TestClient),
#        unittest.TestLoader().loadTestsFromTestCase(TestGroup),
#        unittest.TestLoader().loadTestsFromTestCase(TestLicense),
        unittest.TestLoader().loadTestsFromTestCase(TestMessage),
#        unittest.TestLoader().loadTestsFromTestCase(TestSubscription),
#        unittest.TestLoader().loadTestsFromTestCase(TestVerifcation)
    ])
