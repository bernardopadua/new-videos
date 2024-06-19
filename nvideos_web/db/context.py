from psycopg_pool import ConnectionPool
from psycopg import Connection, connect
from psycopg.rows import dict_row

from nvideos_web.config import get_url_database, get_connection_pool_info

class NewVideosDBContext:
    connPool: ConnectionPool = None
    dbConn: Connection = None

    @classmethod
    def initPool(cls) -> None:
        if cls.connPool is None:
            url = get_url_database()
            poolInfo = get_connection_pool_info()
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
            url = get_url_database()
            cls.dbConn = connect(url, row_factory=dict_row)

    @classmethod
    def getConn(cls) -> Connection:
        # if not cls.connPool._opened:
        #     cls.connPool.open(wait=True)
        return cls.connPool.connection()
