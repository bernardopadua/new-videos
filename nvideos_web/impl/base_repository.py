# BUILT-IN
from typing import ( 
    Any, Type, Optional,
    Sequence
)

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

class PgRepositoryBase:
    _dbContext: Type[NewVideosDBContext]
    _instance: Optional["PgRepositoryBase"] = None

    def __new__(
        cls: Type["PgRepositoryBase"], 
        *args: Sequence[Any], 
        **kwargs: dict[str, Any]
    ) -> "PgRepositoryBase":
        if cls._instance is None:
            cls._instance = super(PgRepositoryBase, cls).__new__(cls)
        return cls._instance

    def __init__(self, dbContext: Type[NewVideosDBContext]) -> None:
        self._db = dbContext

        #Guarantee that the connection started
        if self._db._dbConn is None:
            self._db.initDBContext()
