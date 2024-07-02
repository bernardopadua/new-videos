# BUILT-IN
from hashlib import scrypt
from typing import Type

# CONFIG
from nvideos_web.config import getPasswordConstants, PasswordConstantsCrypt

# ENTITY
from nvideos_web.core.entity.base_entity import AuditData
from nvideos_web.core.entity.user import User, UserInput, UserMetadata
from nvideos_web.core.entity.user_permission import UserPermissionMetadata

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
        from time import perf_counter

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
        sql = """
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
            );
        """.format(**{ 
            "table_name": UserMetadata.tableName(), 
            "sql_fields": sqlFields 
        })
        parsedParams = NvSql.parseSqlParams(sql, userInputData, auditObject=auditInputData)

        sqlFields, fieldsOrder = NvSql.selectOder(
            UserMetadata.userId, UserMetadata.userName,
            UserMetadata.userEmail, UserMetadata.userPermission,
            UserPermissionMetadata.permissionDescription
        )
        # stmt = NvSql().select(
        #     UserMetadata.userId, UserMetadata.userName,
        #     UserMetadata.userEmail, UserMetadata.userPermission,
        #     UserPermissionMetadata.permissionDescription
        # )
        # tt = UserMetadata.as_(newPrefix='pp')
        
        # nSql = """
        #     select a.user_id, a.user_name, a.user_email , p.permission_description
        #     from nvideo_user a, user_permission p 
        #     where a.user_id = 1
        #     and   a.user_permission = p.user_permission;
        # """
        # nSql = """
        #     select 
        #         uu.user_id, uu.user_name, uu.user_email, uu.user_permission, up.permission_description
        #     from nvideo_user uu, user_permission up 
        #     where uu.user_id = 1
        #       and uu.user_permission = up.user_permission
        # """
        ini = perf_counter()
        subU = UserMetadata.as_(newPrefix='us')
        sqlFields, fieldsOrder = NvSql.selectOder(
            UserMetadata.userName, subU.userName, subU.userEmail
        )
        nSql = """
            select 
                --nu.user_name, ch.channel_name, s.subscriber_id, nu2.user_name, nu2.user_email 
                nu.user_name, nu2.user_name, nu2.user_email
              from nvideo_user nu, channel ch, subscriber s, nvideo_user nu2
            where nu.user_id = 10
              and ch.user_id  = nu.user_id
              and s.channel_id = ch.channel_id 
              and s.user_id  = nu2.user_id 
        """
        #nParsedParms = self.parseSqlParams(nSql, userInputData)

        #nSql = "select * from user_permission where user_permission = %(userPermission)s;"
        #nParsedParms = self.parseSqlParams(nSql, userInputData)

        with self._db.getConn() as conn:
            cur = conn.cursor(row_factory=ModelRowFactory.getRowFactory(fieldsOrder))
            #cur = conn.cursor()
            cur.execute(nSql)
            rr = cur.fetchall()
            a = UserMetadata.getRow(rr[0])
            b = subU.getRow(rr[0])
            conn.rollback()
            raise NotImplementedError()

    def update(self, userData: User, newUserData: UserInput) -> User:
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

