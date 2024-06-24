from dataclasses import dataclass
from psycopg import Connection, connect
from psycopg.errors import UndefinedTable

@dataclass(frozen=True)
class PgConnInfo:
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DB: str

class PgDBContext:
    _connection: Connection = None
    _pgInfo: PgConnInfo = None

    @classmethod
    def initDB(cls) -> None:
        from os import environ
        if not cls._pgInfo:
            cls._pgInfo = PgConnInfo(
                environ["POSTGRES_HOST"],
                int(environ["POSTGRES_PORT"]),
                environ["POSTGRES_USER"],
                environ["POSTGRES_PASSWORD"],
                environ["POSTGRES_DB"],
            )
        pgInfo = cls._pgInfo
        if cls._connection is None:
            cls._connection = connect(
                f"postgresql://" + \
                f"{pgInfo.PG_USER}:{pgInfo.PG_PASSWORD}" + \
                f"@{pgInfo.PG_HOST}:{pgInfo.PG_PORT}/{pgInfo.PG_DB}",
            )
    
    @classmethod
    def getConn(cls) -> Connection:
        return cls._connection

    @classmethod
    def closeConn(cls) -> None:
        cls._connection.close()
        cls._connection = None
