# PSYCOPG
from psycopg import Cursor

# BUILT-IN
from hashlib import scrypt
from typing import TypeVar, Sequence, Any

# ENTITY / REPOSITORY
from nvideos_web.core.entity.entity_base import AuditData
from nvideos_web.core.entity.user import User, UserInput, UserMetadata
from nvideos_web.core.repository.user import (
    UserPasswordHasher,
    UserRepository
)
from nvideos_web.impl.base_repository import (
    PgRepositoryBase,
    DictRowFactory
)

# ERRORS
from nvideos_web.impl.error.base import PgRepositoryMissingParameter

# CONFIG
from nvideos_web.config import getPasswordConstants, PasswordConstantsCrypt

# FOR TYPES
from nvideos_web.db.pgcontext import NewVideosDBContext

# Custom Type
PgUserRepository = TypeVar("PgUserRepository", bound="PgUserRepository")

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
    _instance: PgUserRepository = None

    def __new__(cls, dbContext: NewVideosDBContext) -> PgUserRepository:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance

    def __init__(self, dbContext: NewVideosDBContext) -> None:
        super().__init__()
        self._db = dbContext

    def create(self, userInputData: UserInput, auditInputData: AuditData) -> User:
        if not userInputData or not auditInputData:
            raise PgRepositoryMissingParameter(
                "Missing parameter. InputData or AuditData."
            )

        sqlFields, fieldsOrder = self.sqlFields(
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
            "table_name": UserMetadata.__table_name__, 
            "sql_fields": sqlFields 
        })
        parsedParams = self.parseSqlParams(sql, userInputData, auditObject=auditInputData)

        sqlFields, fieldsOrder = self.sqlFields(
            UserMetadata.userId, UserMetadata.userName,
            UserMetadata.userEmail
        )
        nSql = """
            select a.user_id, a.user_name, a.user_email 
            from nvideo_user a, user_permission p 
            where a.user_id = 1
              and a.user_permission = p.user_permission;
        """
        #nParsedParms = self.parseSqlParams(nSql, userInputData)

        #nSql = "select * from user_permission where user_permission = %(userPermission)s;"
        #nParsedParms = self.parseSqlParams(nSql, userInputData)

        with self._db.getConn() as conn:
            #cur = conn.cursor(row_factory=makeRowFactory(fieldsOrder))
            cur = conn.cursor(row_factory=DictRowFactory(fieldsOrder))
            #cur = conn.cursor()
            cur.execute(nSql)
            rr = cur.fetchall()
            conn.rollback()
            return
            # cur.execute(nSql, nParsedParms)
            # rr = cur.fetchall()
            cur.execute(
                sql, parsedParams
            )
            #cur.execute(nSql)
            #cur.execute(nSql, nParsedParms)
            #rr = cur.fetchall()
            #conn.rollback()
            conn.commit()

    def update(self, userData: User, newUserData: User) -> User:
        return super().update(userData, newUserData)

    def delete(self, userId: int) -> None:
        return super().delete(userId)

    def perfGetUserById(self, seconds: int) -> dict:
        #self._db.initConn()
        with self._db.getConn() as conn:
            cur = conn.cursor()
            cur.execute(f"select * from testing_for_now; select pg_sleep({seconds})")
            r = cur.fetchall()
            r.append(id(conn))
            return r

