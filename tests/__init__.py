import unittest


def get_tests():
    return full_suite()


def full_suite():
    from .test_Basic import TestBasic
    from .test_Client import TestClient
    from .test_Groups import TestGroup
    from .test_Issues import TestIssues
    from .test_Messages import TestMessages
    # from .test_Verification import TestVerification

    return unittest.TestSuite([
        # unittest.TestLoader().loadTestsFromTestCase(TestBasic),
        # unittest.TestLoader().loadTestsFromTestCase(TestClient),
        # unittest.TestLoader().loadTestsFromTestCase(TestGroup),
        unittest.TestLoader().loadTestsFromTestCase(TestMessages),
        # unittest.TestLoader().loadTestsFromTestCase(TestVerifcation),
        # unittest.TestLoader().loadTestsFromTestCase(TestIssues)
    ])

if __name__ == "__main__":
    unittest.main()
