# BUILT-IN
from hashlib import scrypt
from typing import TypeVar

# ENTITY / REPOSITORY
from nvideos_web.core.entity.user import User, NewUserInput
from nvideos_web.core.repository.user import (
    UserPasswordHasher,
    UserRepository
)

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

class PgUserRepository(UserRepository):
    _instance: PgUserRepository = None

    def __new__(cls, dbContext: NewVideosDBContext) -> PgUserRepository:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance

    def __init__(self, dbContext: NewVideosDBContext) -> None:
        self._db = dbContext

    def create(self, userData: NewUserInput) -> User:
        from psycopg import _queries
        sql = """
            insert into nvideos_user
            (
                user_name, user_surname, user_email,
                user_password, user_avatar_url, user_permission,
                user_is_active
            )
            values
            (
                %(user_name)s, %(user_surname)s, %(user_email)s, 
                %(user_password)s, %(user_avatar_url)s, %(user_permission)s, 
                %(user_is_active)s
            )
        """
        params = _queries._re_placeholder.finditer(
            bytes(sql.encode('ascii'))
        )
        # for m in _queries._re_placeholder.finditer(sql):
        #     print(m)

        pass
        #params = 

    def update(self, userData: User, newUserData: User) -> User:
        return super().update(userData, newUserData)

    def delete(self, userId: int) -> None:
        return super().delete(userId)

    def perfGetUserById(self, seconds: int) -> dict:
        self._db.initConn()
        with self._db.getConn() as conn:
            cur = conn.cursor()
            cur.execute(f"select * from testing_for_now; select pg_sleep({seconds})")
            r = cur.fetchall()
            r.append(id(conn))
            return r

