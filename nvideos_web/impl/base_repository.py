# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

#TYPING
from typing import Self

class PgRepositoryBase:
    _dbContext: type[NewVideosDBContext] | None = None
    _instance: Self | None = None

    def __new__(
        cls,
        dbContext: type[NewVideosDBContext]
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dbContext: type[NewVideosDBContext]) -> None:
        self._db: type[NewVideosDBContext] = dbContext

        #Guarantee that the connection started
        _ = self._db.getDbConn()
