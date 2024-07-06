# BUILT-IN
from hashlib import scrypt

# TYPING
from typing import Type

# CONFIG
from nvideos_web.config import getPasswordConstants, PasswordConstantsCrypt

# ENTITY
from nvideos_web.core.entity.base.base_entity import AuditData
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
        inputFields, inputParams, _ = NvSql.insertFieldsOrder(UserMetadata, userInputData)
        auditFields, auditParams, _ = NvSql.insertFieldsOrder(UserMetadata, auditInputData)
        _, allFieldsOrder = NvSql.selectOder(UserMetadata.all)

        stmt = NvSql.formatStmt(
            """
            insert into {table_name}
            ({input_fields},{audit_fields})
            values
            ({input_params},{audit_params})
            returning *;
            """,
            table_name=UserMetadata.tableName(),
            input_fields=inputFields,
            audit_fields=auditFields,
            input_params=inputParams,
            audit_params=auditParams
        )
        paramsInsert = NvSql.parseSqlParams(stmt, inputObject=userInputData, auditObject=auditInputData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory.getRowFactory(allFieldsOrder))
            cur.execute(stmt, params=paramsInsert)
            result = cur.fetchone()
            conn.commit()
            return UserMetadata.row(result)

    def checkIdExists(self, userId: int) -> bool:
        stmt = NvSql.formatStmt(
            "select 1 from {table_name} where {user_id} = {user_id_value};",
            table_name=UserMetadata.tableName(),
            user_id=UserMetadata.userId.field,
            user_id_value=userId
        )
        with self._db.getConn() as conn:
            r = conn.execute(stmt)
            return r.rowcount > 0

    def updateById(self, userId: int, newUserData: UserInput, auditData: AuditData) -> User:
        if newUserData.isNone():
            raise Exception("You cant update a record with an empty input.")

        fieldsAudit = NvSql.updateFields(UserMetadata, inputData=auditData)
        fieldsTable = NvSql.updateFields(UserMetadata, inputData=newUserData)

        allFields, allFieldsOrder = NvSql.selectOder(UserMetadata.all, usePrefix=True)
        stmt = NvSql.formatStmt(
            """
            update {table_name} 
               set {fields_table}, {fields_audit}
             where {userId_field} = {user_id}
            returning {returning_fields};
            """, 
            table_name=UserMetadata.tableName(),
            fields_table=fieldsTable,
            fields_audit=fieldsAudit,
            userId_field=UserMetadata.userId.field,
            user_id=userId,
            returning_fields=allFields
        )
        paramsUpdate: dict = NvSql.parseSqlParams(stmt, inputObject=newUserData, auditObject=auditData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(allFieldsOrder))
            cur.execute(stmt, params=paramsUpdate)
            result = cur.fetchone()
            conn.commit()
        return UserMetadata.row(result)

    def delete(self, userId: int, auditData: AuditData) -> User:
        auditFields = NvSql.updateFields(UserMetadata, auditData)
        fieldsStr, fieldsOder = NvSql.selectOder(UserMetadata.all)
        stmt = NvSql.formatStmt(
            """
            update {table_name} set {active_field} = false, {audit_fields} where {user_id_field} = {user_id_value}
            returning {fields_str};
            """,
            table_name=UserMetadata.tableName(),
            active_field=UserMetadata.userIsActive.field,
            audit_fields=auditFields,
            user_id_field=UserMetadata.userId.field,
            user_id_value=userId,
            fields_str=fieldsStr
        )
        paramsUpdate = NvSql.parseSqlParams(stmt, auditData)
        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory(fieldsOder))
            cur.execute(stmt, params=paramsUpdate)
            result = cur.fetchone()
            conn.commit()
            return UserMetadata.row(result)
