# PSYCOPG
from typing import override

from psycopg_pool import ConnectionPool
from psycopg import Connection

# CONFIG
from nvideos_web.config import getUrlDataBase, getConnectionPoolInfo

# CONTEXT DB
from nvideos_web.db.basecontext import BaseContext

# TYPING
from collections.abc import Generator

from contextlib import contextmanager

class NewVideosDBContext(BaseContext[Connection]):
    _connPool: ConnectionPool | None = None
    _dbConn: Connection | None = None
    
    @classmethod
    def getDbConn(cls) -> Connection:
        if cls._dbConn is None:
            cls.initDBContext()
        if cls._dbConn is None:
            raise Exception("DB connection cannot be None")
        return cls._dbConn

    @classmethod
    @override
    def initDBContext(cls) -> None:
        if cls._connPool is None:
            url = getUrlDataBase()
            poolInfo = getConnectionPoolInfo()
            cls._connPool = ConnectionPool(
                url, 
                open=poolInfo.OPEN, 
                min_size=poolInfo.MINSIZE, 
                max_size=poolInfo.MAXSIZE,
                timeout=poolInfo.TIMEOUT
            )
            cls._connPool.open(wait=True)

    # @classmethod
    # def initConn(cls) -> None:
    #     if cls.dbConn is None:
    #         url = getUrlDataBase()
    #         cls.dbConn = connect(url, row_factory=dict_row)

    @classmethod
    @contextmanager
    def getConn(cls) -> Generator[Connection, None, None]:
        # if not cls.connPool._opened:
        #     cls.connPool.open(wait=True)
        if cls._connPool is None:
            raise Exception("Connection pool cannot be null")

        try:
            with cls._connPool.connection() as conn:
                yield conn
        finally:
            pass
