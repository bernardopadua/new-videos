from os import environ
from typing import IO, Mapping, Any, TextIO

from dataclasses import dataclass

@dataclass(frozen=True)
class DBPoolInfo:
    MINSIZE: int
    MAXSIZE: int
    OPEN: bool
    TIMEOUT: int

@dataclass(frozen=True)
class PasswordConstantsCrypt:
    N_CONSTANT: int
    R_CONSTANT: int
    P_CONSTANT: int
    SALT_CONSTANT: str

def getPasswordConstants() -> PasswordConstantsCrypt:
    return PasswordConstantsCrypt(
        int(environ["SCRYPT_CONSTANT_N"]),
        int(environ["SCRYPT_CONSTANT_R"]),
        int(environ["SCRYPT_CONSTANT_P"]),
        environ["SCRYPT_SECRET_SALT"]
    )

def getConnectionPoolInfo() -> DBPoolInfo:
    return DBPoolInfo(
        int(environ["POSTGRES_POOL_MINSIZE"]),
        int(environ["POSTGRES_POOL_MAXSIZE"]),
        bool(environ["POSTGRES_POOL_OPEN"].lower() == "true"),
        int(environ["POSTGRES_POOL_TIMEOUT"])
    )

def getUrlDataBase() -> str:
    postUser = environ["POSTGRES_USER"]
    postPassword = environ["POSTGRES_PASSWORD"]
    postDb = environ["POSTGRES_DB"]
    postHost = environ["POSTGRES_HOST"]
    postPort = environ["POSTGRES_PORT"]

    urlConn = f"postgresql://" + \
        f"{postUser}:{postPassword}" + \
        f"@{postHost}:{postPort}/{postDb}"

    return urlConn

def loadDotEnv(filename: IO[Any]) -> Mapping[str, Any]:
    configRet = {}
    line = filename.readline()
    while line:
        if "=" not in line:
            line = filename.readline()
            continue
        k, v = line.strip().split("=")
        configRet[k] = v

        line = filename.readline()

    return configRet