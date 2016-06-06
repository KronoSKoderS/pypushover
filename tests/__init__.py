import unittest


def get_tests():
    return full_suite()


def full_suite():
    from .runtests import TestBasic, TestClient, TestGroup, TestLicense, TestMessage, TestVerifcation, TestIssues

    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestBasic),
        # unittest.TestLoader().loadTestsFromTestCase(TestClient),
        # unittest.TestLoader().loadTestsFromTestCase(TestGroup),
        unittest.TestLoader().loadTestsFromTestCase(TestMessage),
        # unittest.TestLoader().loadTestsFromTestCase(TestVerifcation),
        # unittest.TestLoader().loadTestsFromTestCase(TestIssues)
    ])
