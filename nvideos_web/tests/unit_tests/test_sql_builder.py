from unittest import TestCase
from nvideos_web.impl.base.sql_builder import NvSql

from nvideos_web.core.entity.user import UserMetadata, UserInput

class TestMainSqlBuilderUsage(TestCase):
    def setUp(self) -> None:
        super().setUp()
    
    def testUpdadeFields(self):
        userInput = UserInput(
            userName="Testing",
            userSurname="Unittest",
            userEmail="test@unittest.com"
        )
        upFields = NvSql.updateFields(
            UserMetadata,
            userInput
        )
        
        u = UserMetadata
        expectedReturn = f"{u.userName.field} = %({u.userName.attr})s, " \
            f"{u.userSurname.field} = %({u.userSurname.attr})s, " \
            f"{u.userEmail.field} = %({u.userEmail.attr})s"

        assert upFields == expectedReturn
