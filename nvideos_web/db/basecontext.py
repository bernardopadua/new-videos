from typing import Protocol, TypeVar

BaseConnection = TypeVar('BaseConnection')

class BaseContext(Protocol[BaseConnection]):
    @classmethod
    def initDBContext(cls) -> None:
        raise NotImplementedError()

    @classmethod
    def getConn(cls) -> BaseConnection:
        raise NotImplementedError()