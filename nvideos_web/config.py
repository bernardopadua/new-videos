from os import environ
from io import TextIOWrapper

from dataclasses import dataclass

@dataclass(frozen=True)
class DBPoolInfo:
    MINSIZE: int
    MAXSIZE: int
    OPEN: bool
    TIMEOUT: int

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

def loadDotEnv(filename: TextIOWrapper) -> dict:
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