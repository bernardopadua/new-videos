import unittest
from nvideos_web.impl.base.sql_builder import NvSql

from nvideos_web.core.entity.user import UserMetadata, UserInput

class TestSqlBuilder(unittest.TestCase):
    def test_insertFieldsOrder(self) -> None:
        userName = "Test"
        userEmail = "test@test.com"
        userSurname = "Surname"

        expFields = f"{UserMetadata.userName.field},{UserMetadata.userSurname.field},{UserMetadata.userEmail.field}"
        expParams = f"%({UserMetadata.userName.attr})s,%({UserMetadata.userSurname.attr})s,%({UserMetadata.userEmail.attr})s"
        expOrder = [UserMetadata.userName,UserMetadata.userSurname, UserMetadata.userEmail]

        _userInput = UserInput(
            userName=userName,
            userSurname=userSurname,
            userEmail=userEmail
        )
        resFields, resParams, resOrder = NvSql.insertFieldsOrder(UserMetadata, _userInput)

        self.assertEqual(resFields, expFields)
        self.assertEqual(resParams, expParams)
        self.assertEqual(resOrder, expOrder)
    
    def test_updadeFields(self) -> None:
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

        self.assertEqual(upFields, expectedReturn)

    def test_selectOrder(self) -> None:
        fields, fieldsOrder = NvSql.selectOder(UserMetadata.userName, UserMetadata.userId)

        fieldsTest = f"{UserMetadata.userName.field},{UserMetadata.userId.field}"
        fieldsOrderTest = [UserMetadata.userName, UserMetadata.userId]

        self.assertEqual(fields, fieldsTest)
        self.assertEqual(fieldsOrder, fieldsOrderTest)

    def test_formatStmt(self) -> None:
        table = UserMetadata.tableName()
        fields, _ = NvSql.selectOder(UserMetadata.userId, UserMetadata.userName)
        paramUsuId = UserMetadata.userId.field
        paramUsu = f"%({UserMetadata.userId.attr})s"
        
        stmt = "select {field} from {table} where {user_id} = {param_usu}"
        stmtCompare = NvSql.formatStmt(stmt,
            field=fields,
            table=table,
            user_id=paramUsuId,
            param_usu=paramUsu
        )

        correctStmt = f"select {fields} from {table} where {paramUsuId} = {paramUsu}"

        self.assertEqual(stmtCompare, correctStmt)

    def test_parseSqlParams(self) -> None:
        table = UserMetadata.tableName()
        fields, _ = NvSql.selectOder(UserMetadata.userEmail)
        userEmailField = UserMetadata.userEmail.field
        userEmailAttr = UserMetadata.userEmail.attr
        stmt = f"select {fields} from {table} where {userEmailField} = %({userEmailAttr})s"

        emailTest = "test@test.com"
        userInput = UserInput(
            userEmail=emailTest
        )

        params = NvSql.parseSqlParams(stmt, userInput)

        self.assertEqual(params, { f"{userEmailAttr}": emailTest })


def suite_sql_builder_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestSqlBuilder("test_insertFieldsOrder"))
    suite.addTest(TestSqlBuilder("test_selectOrder"))
    suite.addTest(TestSqlBuilder("test_updadeFields"))
    suite.addTest(TestSqlBuilder("test_formatStmt"))
    suite.addTest(TestSqlBuilder("test_parseSqlParams"))
    return suite