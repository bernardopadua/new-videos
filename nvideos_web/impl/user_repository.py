# BUILT-IN
from hashlib import scrypt

# TYPING
from typing import Type

# CONFIG
from nvideos_web.config import getPasswordConstants, PasswordConstantsCrypt

# ENTITY
from nvideos_web.core.entity.base_entity import AuditData
from nvideos_web.core.entity.user import User, UserInput, UserMetadata

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# SQL BUILDER
from nvideos_web.impl.base.sql_builder import NvSql

# REPOSITORY
from nvideos_web.core.repository.user import (
    UserPasswordHasher,
    UserRepository
)

# IMPL
from nvideos_web.impl.base.row_factory import ModelRowFactory
from nvideos_web.impl.base_repository import PgRepositoryBase

# ERRORS
from nvideos_web.impl.error.base import PgRepositoryMissingParameter

class PasswordHasher(UserPasswordHasher):
    def __init__(self) -> None:
        self._constants:PasswordConstantsCrypt = getPasswordConstants()
    
    def hashPassword(self, password: str) -> str:
        return scrypt(
            bytes(password.encode('utf-8')),
            salt=bytes(self._constants.SALT_CONSTANT.encode('utf-8')),
            n=self._constants.N_CONSTANT,
            r=self._constants.R_CONSTANT,
            p=self._constants.P_CONSTANT
        ).hex()

class PgUserRepository(PgRepositoryBase, UserRepository):
    def __init__(self, dbContext: Type[NewVideosDBContext]) -> None:
        super().__init__(dbContext=dbContext)
    
    def create(self, userInputData: UserInput, auditInputData: AuditData) -> User:
        if not userInputData or not auditInputData:
            raise PgRepositoryMissingParameter(
                "Missing parameter. InputData or AuditData."
            )

        sqlFields, fieldsOrder = NvSql.selectOder(
            UserMetadata.userName, UserMetadata.userSurname,
            UserMetadata.userEmail, UserMetadata.userPassword,
            UserMetadata.userAvatarUrl, UserMetadata.userPermission,
            UserMetadata.userIsActive,
            #Audit
            UserMetadata.createdAt, UserMetadata.createdBy,
            UserMetadata.updatedAt, UserMetadata.updatedBy
        )
        stmt = NvSql.formatStmt("""
                insert into {table_name}
                (
                    {sql_fields}
                )
                values
                (
                    %(userName)s, %(userSurname)s, %(userEmail)s, 
                    %(userPassword)s, %(userAvatarUrl)s, %(userPermission)s, 
                    %(userIsActive)s, %(createdAt)s, %(createdBy)s,
                    %(updatedAt)s, %(updatedBy)s
                )
                returning {sql_fields};
            """,
            table_name=UserMetadata.tableName(), 
            sql_fields=sqlFields 
        )
        parsedParams = NvSql.parseSqlParams(stmt, userInputData, auditObject=auditInputData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory.getRowFactory(fieldsOrder))
            cur.execute(stmt, params=parsedParams)
            result = cur.fetchone()
            conn.commit()
            return UserMetadata.row(result)

    def updateById(self, userId: int, newUserData: UserInput, auditData: AuditData) -> User:
        if newUserData.isNone():
            raise Exception("You cant update a record with an empty input.")
        fieldsAudit = NvSql.updateFields(UserMetadata, inputData=auditData)
        fieldsTable = NvSql.updateFields(UserMetadata, inputData=newUserData)

        stmt = """update {table_name} 
            set {fieldsTable}, {fieldsAudit}
          where {userIdField} = {userId}
          returning {returningFields};
        """
        ff = NvSql.selectOder(UserMetadata.all)
        stmt = NvSql.formatStmt(stmt, 
            table_name=UserMetadata.tableName(),
            fieldsTable=fieldsTable,
            fieldsAudit=fieldsAudit,
            userIdField=UserMetadata.userId.field,
            userId=userId
        )
        paramsUpdate: dict = NvSql.parseSqlParams(stmt, inputObject=newUserData, auditObject=auditData)
        with self._db.getConn() as conn:
            pass

        raise NotImplementedError()
        return

    def delete(self, userId: int) -> None:
        raise NotImplementedError()

    def perfGetUserById(self, seconds: int) -> list:
        #self._db.initConn()
        with self._db.getConn() as conn:
            cur = conn.cursor()
            cur.execute(f"select * from testing_for_now; select pg_sleep({seconds})")
            r = cur.fetchall()
            r.append(id(conn))
            return r

