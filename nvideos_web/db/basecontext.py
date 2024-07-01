# TYPING
from typing import Protocol, TypeVar, Iterator, Generator, Any

from contextlib import contextmanager

BaseConnection = TypeVar('BaseConnection', covariant=True)

class BaseContext(Protocol[BaseConnection]):
    @classmethod
    def initDBContext(cls) -> None:
        raise NotImplementedError()

    @classmethod
    @contextmanager
    #def getConn(cls) -> Iterator[BaseConnection]:
    def getConn(cls) -> Generator[BaseConnection, Any, Any]:
        raise NotImplementedError()