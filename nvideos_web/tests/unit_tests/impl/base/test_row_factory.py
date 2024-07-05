import unittest

from nvideos_web.core.entity.user import UserMetadata, User
from nvideos_web.impl.base.row_factory import ModelRowFactory

class TestModelRowFactory(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._r: ModelRowFactory

    def test_Instantiation(self) -> None:
        someFields = [UserMetadata.userName, UserMetadata.userEmail]
        self._r = ModelRowFactory(someFields)
        
        self.assertEquals(self._r.fields, someFields)

        userName = "Testing"
        userEmail = "testing@test.test"

        resultUser = UserMetadata.row(self._r((userName, userEmail)))
        userAssert = User(userName=userName,userEmail=userEmail)

        self.assertTrue(isinstance(resultUser, User))
        self.assertEqual(resultUser, userAssert)

def suite_row_factory_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestModelRowFactory("test_Instantiation"))
    return suite
