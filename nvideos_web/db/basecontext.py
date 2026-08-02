# TYPING
from typing import Protocol, TypeVar
from collections.abc import Generator

from contextlib import contextmanager

BaseConnection = TypeVar('BaseConnection', covariant=True)

class BaseContext(Protocol[BaseConnection]):
    @classmethod
    def initDBContext(cls) -> None:
        ...

    @classmethod
    @contextmanager
    #def getConn(cls) -> Iterator[BaseConnection]:
    def getConn(cls) -> Generator[BaseConnection, None, None]:
        ...