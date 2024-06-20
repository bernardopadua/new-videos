from psycopg_pool import ConnectionPool
from psycopg import Connection, connect
from psycopg.rows import dict_row

from nvideos_web.config import getUrlDataBase, getConnectionPoolInfo

class NewVideosDBContext:
    connPool: ConnectionPool = None
    dbConn: Connection = None

    @classmethod
    def initPool(cls) -> None:
        if cls.connPool is None:
            url = getUrlDataBase()
            poolInfo = getConnectionPoolInfo()
            cls.connPool = ConnectionPool(
                url, 
                open=poolInfo.OPEN, 
                min_size=0, 
                max_size=poolInfo.MAXSIZE,
                timeout=poolInfo.TIMEOUT,
                max_idle=1,
                max_lifetime=1
            )
            cls.connPool.open(wait=True)

    @classmethod
    def initConn(cls) -> None:
        if cls.dbConn is None:
            url = getUrlDataBase()
            cls.dbConn = connect(url, row_factory=dict_row)

    @classmethod
    def getConn(cls) -> Connection:
        # if not cls.connPool._opened:
        #     cls.connPool.open(wait=True)
        return cls.connPool.connection()
