# PSYCOPG
from psycopg_pool import ConnectionPool
from psycopg import Connection, connect
from psycopg.rows import dict_row

# BUILT-IN
from contextlib import contextmanager

# CONFIG
from nvideos_web.config import getUrlDataBase

# CONTEXT DB
from nvideos_web.db.basecontext import BaseContext

# TYPING
from typing import Iterator, Generator, Any

class NewVideosDBContext(BaseContext[Connection]):
    connPool: ConnectionPool
    dbConn: Connection

    # @classmethod
    # def initDBContext(cls) -> None:
    #     if cls.connPool is None:
    #         url = getUrlDataBase()
    #         poolInfo = getConnectionPoolInfo()
    #         cls.connPool = ConnectionPool(
    #             url, 
    #             open=poolInfo.OPEN, 
    #             min_size=poolInfo.MINSIZE, 
    #             max_size=poolInfo.MAXSIZE,
    #             timeout=poolInfo.TIMEOUT,
    #         )
    #         cls.connPool.open(wait=True)

    @classmethod
    def initConn(cls) -> None:
        if cls.dbConn is None:
            url = getUrlDataBase()
            cls.dbConn = connect(url, row_factory=dict_row)

    @classmethod
    @contextmanager
    #def getConn(cls) -> Iterator[Connection]:
    def getConn(cls) -> Generator[Connection, Any, Any]:
        try:
            # if not cls.connPool._opened:
            #     cls.connPool.open(wait=True)
            yield cls.dbConn
            #return cls.connPool.connection()
        finally:
            pass
        
