from dataclasses import dataclass
from psycopg import Connection, connect

@dataclass(frozen=True)
class PgConnInfo:
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DB: str

class PgDBContext:
    _connection: Connection = None

    @classmethod
    def initDB(cls) -> None:
        from os import environ
        pgInfo = PgConnInfo(
            environ["POSTGRES_HOST"],
            int(environ["POSTGRES_PORT"]),
            environ["POSTGRES_USER"],
            environ["POSTGRES_PASSWORD"],
            environ["POSTGRES_DB"],
        )
        if cls._connection is None:
            cls._connection = connect(
                f"postgresql://" + \
                f"{pgInfo.PG_USER}:{pgInfo.PG_PASSWORD}" + \
                f"@{pgInfo.PG_HOST}:{pgInfo.PG_PORT}/{pgInfo.PG_DB}"
            )
    
    @classmethod
    def getConn(cls) -> Connection:
        return cls._connection
